from utils import load_report, save_report, update_employee, send_email


def check_copyright_signals(stats):
    """
    ملاحظة مهمة: YouTube Data API العام لا يعطي تفاصيل Content ID / Copyright Claims
    الكاملة (هذه خاصة بـ YouTube Studio لأصحاب القناة). هنا نكتفي برصد "إشارات" غير
    طبيعية مثل حالة الفيديو (خاص/محذوف/غير منشور) كمؤشر أولي فقط، وليس تأكيدًا كاملاً.
    """
    flags = []
    for v in stats.get("recent_videos", []):
        privacy = v.get("privacyStatus")
        upload = v.get("uploadStatus")
        if privacy != "public" or upload not in ("processed", "uploaded"):
            flags.append(v)
    return flags


def run():
    update_employee("reporter", "working", "جاري إعداد الرسالة النهائية لصاحب القناة...")
    checker_report = load_report("checker_report")
    informations_report = load_report("informations_report")

    flags = check_copyright_signals(checker_report["stats"])

    if flags:
        titles = "، ".join(v["title"] for v in flags)
        alert_body = (
            "تنبيه: تم رصد حالة غير طبيعية على أحد الفيديوهات قد تكون مرتبطة "
            "بمشكلة كوبي رايت أو مشكلة نشر.\n\n"
            f"الفيديوهات المتأثرة: {titles}\n\n"
            "يرجى المراجعة المباشرة من YouTube Studio للتأكد من التفاصيل الكاملة، "
            "لأن الواجهة البرمجية العامة لا تعطي تفاصيل الكوبي رايت الكاملة."
        )
        update_employee("Writer", "alert", f"تنبيه من reporter بخصوص: {titles}")
        send_email("reporter", "⚠️ تنبيه: مشكلة محتملة في أحد الفيديوهات", alert_body)

    subject = "التقرير اليومي لقناتك - Sams Company"
    send_email("reporter", subject, informations_report["summary_text"])

    save_report("reporter_report", {"flags": flags, "sent": True})
    state_summary = "تم إرسال التقرير اليومي لصاحب القناة"
    if flags:
        state_summary += " + تم إرسال تنبيه كوبي رايت"
    update_employee("reporter", "done", state_summary)


if __name__ == "__main__":
    run()
