from utils import get_channel_stats, call_groq, save_report, load_report, update_employee


def run():
    update_employee("Checker", "working", "جاري مراجعة تقرير Writer مقابل بيانات حية جديدة...")
    writer_report = load_report("writer_report")
    live_stats = get_channel_stats()  # Refresh مستقل عن Writer لتفادي بيانات قديمة

    system = (
        "أنت مراجع دقيق جدًا (Fact Checker). مهمتك التأكد أن كل رقم أو ادعاء في التقرير "
        "يطابق تمامًا البيانات الحية المعطاة لك، وتصحيح أي خطأ إن وجد."
    )
    user = f"""التقرير المكتوب من Writer:
{writer_report['report_text']}

البيانات الحية الحالية (JSON) - هذه هي المرجع الوحيد للتحقق:
{live_stats}

المطلوب:
- إذا كانت كل الأرقام والادعاءات في التقرير مطابقة تمامًا للبيانات الحية: أعد كتابة التقرير كما هو،
  مع إضافة سطر في البداية بالضبط: "تم التحقق: التقرير مطابق للبيانات الحية."
- إذا وجدت أي رقم أو معلومة غير مطابقة: صحّحها، واكتب في البداية سطرًا بالضبط:
  "تم رصد خطأ وتصحيحه:" متبوعًا بشرح مختصر لما تم تصحيحه، ثم أعد كتابة التقرير كاملاً بعد التصحيح."""

    checked_text = call_groq(system, user)

    report = {"stats": live_stats, "report_text": checked_text}
    save_report("checker_report", report)
    update_employee("Checker", "done", "تمت المراجعة والتأكيد، تم التسليم لـ informations")
    return report


if __name__ == "__main__":
    run()
