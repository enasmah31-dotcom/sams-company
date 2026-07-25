import os
import json
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATUS_PATH = os.path.join(DATA_DIR, "status.json")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_status():
    if not os.path.exists(STATUS_PATH):
        return {}
    with open(STATUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_status(status):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def update_employee(employee, state, summary=""):
    """state: idle | working | done | alert"""
    status = load_status()
    status[employee] = {
        "state": state,
        "summary": summary,
        "updated_at": now_iso(),
    }
    save_status(status)
    print(f"[{employee}] {state}: {summary}")


def save_report(name, content):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = os.path.join(REPORTS_DIR, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)


def load_report(name):
    path = os.path.join(REPORTS_DIR, f"{name}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_channel_stats():
    """يسحب إحصائيات حية من يوتيوب في كل مرة تُستدعى فيها (Refresh)."""
    api_key = os.environ["YOUTUBE_API_KEY"]
    channel_id = os.environ["YOUTUBE_CHANNEL_ID"]

    r = requests.get(
        "https://www.googleapis.com/youtube/v3/channels",
        params={
            "part": "statistics,snippet,contentDetails",
            "id": channel_id,
            "key": api_key,
        },
        timeout=30,
    )
    r.raise_for_status()
    items = r.json().get("items", [])
    if not items:
        raise RuntimeError("لم يتم العثور على القناة - تأكد من YOUTUBE_CHANNEL_ID")
    data = items[0]
    uploads_playlist = data["contentDetails"]["relatedPlaylists"]["uploads"]

    r2 = requests.get(
        "https://www.googleapis.com/youtube/v3/playlistItems",
        params={
            "part": "snippet,contentDetails",
            "playlistId": uploads_playlist,
            "maxResults": 10,
            "key": api_key,
        },
        timeout=30,
    )
    r2.raise_for_status()
    playlist_items = r2.json().get("items", [])
    video_ids = [it["contentDetails"]["videoId"] for it in playlist_items]

    videos = []
    if video_ids:
        r3 = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "part": "statistics,snippet,status",
                "id": ",".join(video_ids),
                "key": api_key,
            },
            timeout=30,
        )
        r3.raise_for_status()
        videos = r3.json().get("items", [])

    return {
        "channel": {
            "title": data["snippet"]["title"],
            "subscribers": data["statistics"].get("subscriberCount"),
            "views": data["statistics"].get("viewCount"),
            "videoCount": data["statistics"].get("videoCount"),
        },
        "recent_videos": [
            {
                "id": v["id"],
                "title": v["snippet"]["title"],
                "views": v["statistics"].get("viewCount"),
                "likes": v["statistics"].get("likeCount"),
                "comments": v["statistics"].get("commentCount"),
                "privacyStatus": v["status"].get("privacyStatus"),
                "uploadStatus": v["status"].get("uploadStatus"),
            }
            for v in videos
        ],
        "fetched_at": now_iso(),
    }


def call_groq(system_prompt, user_prompt, model=None):
    api_key = os.environ["GROQ_API_KEY"]
    model = model or os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
        },
        timeout=60,
    )
    if r.status_code != 200:
        raise RuntimeError(f"خطأ من Groq ({r.status_code}): {r.text[:500]}")
    return r.json()["choices"][0]["message"]["content"]


def send_email(employee, subject, body, to_override=None):
    gmail_address = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = to_override or os.environ["RECIPIENT_EMAIL"]

    full_body = f"{body}\n\n---\nمرسل من: {employee}"
    msg = MIMEText(full_body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = f"Sams Company {employee} <{gmail_address}>"
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, app_password)
        server.sendmail(gmail_address, [recipient], msg.as_string())
