from utils import get_channel_stats, call_groq, save_report, update_employee


def run():
    update_employee("Writer", "working", "جاري سحب إحصائيات القناة (Refresh)...")
    stats = get_channel_stats()

    system = (
        "أنت محلل إحصائيات يوتيوب دقيق جدًا ومحترف. "
        "اكتب تقارير مبنية فقط على البيانات المعطاة لك، ولا تختلق أي رقم غير موجود."
    )
    user = f"""اكتب تقريرًا يوميًا مفصلًا عن حالة القناة بناءً على هذه البيانات (JSON):

{stats}

التقرير يجب أن يغطي:
- المشتركين والمشاهدات الإجمالية
- أداء آخر الفيديوهات (مشاهدات، لايكات، تعليقات) بالتفصيل
- أي ملاحظات دقيقة على الأداء

اكتبه بالعربية، بأسلوب احترافي جدًا، منظم بعناوين فرعية واضحة."""

    report_text = call_groq(system, user)

    report = {"stats": stats, "report_text": report_text}
    save_report("writer_report", report)
    update_employee("Writer", "done", "تم إعداد التقرير اليومي، تم التسليم لـ Checker")
    return report


if __name__ == "__main__":
    run()
