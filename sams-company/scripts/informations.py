from utils import call_groq, save_report, load_report, update_employee


def run():
    update_employee("informations", "working", "جاري تلخيص التقرير المُتحقق منه واستخراج التوصيات...")
    checker_report = load_report("checker_report")

    system = (
        "أنت مستشار نمو قنوات يوتيوب محترف. مهمتك تلخيص التقرير برؤوس أقلام واضحة، "
        "ثم كتابة توصيات عملية قابلة للتنفيذ لتحسين الأداء، مبنية على البيانات فقط."
    )
    user = f"""هذا التقرير المُتحقق منه من Checker:
{checker_report['report_text']}

اكتب:
1) ملخص التقرير في نقاط قصيرة وواضحة (Bullet Points)
2) قائمة من 3 إلى 5 قرارات/إجراءات عملية لتحسين الإحصائيات بشكل إيجابي، كل واحدة بسطر أو سطرين."""

    summary_text = call_groq(system, user)

    report = {"summary_text": summary_text}
    save_report("informations_report", report)
    update_employee("informations", "done", "تم إعداد الملخص والتوصيات، تم التسليم لـ reporter")
    return report


if __name__ == "__main__":
    run()
