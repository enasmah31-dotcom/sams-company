from utils import call_groq, save_report, load_report, update_employee


def run():
    update_employee("Content", "working", "جاري تحليل أسلوب القناة واقتراح أفكار جديدة...")
    checker_report = load_report("checker_report")

    system = (
        "أنت خبير أفكار محتوى يوتيوب مبدع. اقترح أفكار فيديوهات جديدة مبنية فقط على "
        "أسلوب ومحتوى القناة الحالي المعطى لك، بدون افتراضات خارج نطاق القناة."
    )
    user = f"""بيانات آخر فيديوهات القناة:
{checker_report['stats'].get('recent_videos')}

اقترح 5 أفكار فيديوهات جديدة تتماشى مع نفس أسلوب القناة الحالي.
كل فكرة: عنوان مقترح + سطر يشرح الفكرة ولماذا تناسب الجمهور الحالي."""

    ideas_text = call_groq(system, user)
    save_report("content_report", {"ideas_text": ideas_text})
    update_employee("Content", "done", "تم إعداد اقتراحات محتوى جديدة")


if __name__ == "__main__":
    run()
