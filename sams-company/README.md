# Sams Company

شركة يوتيوب افتراضية مكونة من موظفين ذكاء اصطناعي، تشتغل تلقائيًا يوميًا الساعة 1 ظهرًا
بتوقيت طرابلس، مجانًا 100٪ عبر GitHub Actions.

الموظفون:
- **Writer** — يسحب إحصائيات القناة ويكتب التقرير اليومي
- **Checker** — يراجع التقرير مقابل بيانات حية جديدة ويصحح أي خطأ
- **informations** — يلخص التقرير ويقترح قرارات لتحسين الأداء
- **Content** — يقترح أفكار فيديوهات جديدة بناءً على أسلوب القناة
- **reporter** — يرسل الملخص اليومي لصاحب القناة، ويبلغ فورًا عند رصد إشارة كوبي رايت

---

## خطوات الرفع على GitHub (مرة وحدة بس)

### 1) أنشئ Repository جديد
1. ادخل github.com وسجل دخول
2. اضغط **+** فوق يمين الصفحة ← **New repository**
3. اسمه مثلاً `sams-company`
4. خله **Public** (عشان GitHub Pages المجاني يشتغل بدون مشاكل)
5. اضغط **Create repository** (بدون ما تضيف README من عندهم)

### 2) ارفع هذي الملفات
أسهل طريقة: بصفحة الـ repo الفاضية، اضغط **uploading an existing file**،
واسحب عليها **كل الملفات والمجلدات** اللي بأسفل هذي الرسالة بنفس ترتيبها
(لازم يضل شكل المجلدات كما هو: `.github/workflows/daily.yml`, `scripts/...`, `data/...`).

### 3) أضف الأسرار (Secrets) — المفاتيح ما ينحطون بالكود أبدًا
روح لـ: **Settings** ← **Secrets and variables** ← **Actions** ← **New repository secret**،
وضيف كل واحد من هذول بالضبط بهذي الأسماء:

| اسم الـ Secret        | القيمة                                      |
|------------------------|----------------------------------------------|
| `YOUTUBE_API_KEY`      | المفتاح اللي أخذته من Google Cloud Console   |
| `YOUTUBE_CHANNEL_ID`   | معرف قناتك (يبدأ بـ UC...)                   |
| `GROQ_API_KEY`         | المفتاح من console.groq.com                  |
| `GMAIL_ADDRESS`        | vibng.me@gmail.com                           |
| `GMAIL_APP_PASSWORD`   | الكود المكون من 16 حرف (App Password)        |
| `RECIPIENT_EMAIL`      | hitc.ads@gmail.com                           |

> كيف تجيب `YOUTUBE_CHANNEL_ID`: روح لقناتك على يوتيوب ← Customize Channel ←
> Basic info، أو افتح studio.youtube.com وشوف الرابط، أو استخدم أداة مثل
> commentpicker.com/youtube-channel-id.html وحط رابط قناتك فيها.

### 4) فعّل GitHub Pages (عشان الداشبورد)
**Settings** ← **Pages** ← تحت Source اختر **Deploy from a branch** ←
Branch: **main** / **(root)** ← Save.
بعد دقيقة أو دقيقتين، الداشبورد يصير متاح على رابط شبيه بـ:
`https://اسم-حسابك.github.io/sams-company/`

### 5) جرب التشغيل يدويًا أول مرة (بدون انتظار الغد)
روح لتبويب **Actions** ← اختر **Sams Company Daily Run** من القائمة الجانبية ←
اضغط **Run workflow** ← **Run workflow**.
انتظر دقيقة أو دقيقتين، بعدها حدّث صفحة الداشبورد وبتشوف حالة كل موظف.

---

## ملاحظات مهمة
- التشغيل التلقائي مضبوط على `0 11 * * *` (11:00 UTC = 1:00 ظهرًا طرابلس، لأن ليبيا UTC+2
  طول السنة). لو حسّيت التوقيت طلع غلط بسبب تغيير رسمي مستقبلي، عدّل السطر بملف
  `.github/workflows/daily.yml`.
- لو Groq غيّر اسم الموديل مستقبلًا وصار فيه خطأ، غيّر القيمة الافتراضية داخل
  `scripts/utils.py` (متغير `GROQ_MODEL`) لأي موديل نشط من console.groq.com/docs/models.
- الكوبي رايت: يوتيوب ما تعطي تفاصيل Content ID الكاملة عبر الـ API العام، فموظف
  `reporter` يعتمد على "إشارات" (حالة الفيديو) كمؤشر أولي فقط، وليس تأكيدًا نهائيًا —
  لازم تتأكد يدويًا من YouTube Studio عند أي تنبيه.
- كل شي هنا مجاني 100٪: GitHub Actions (2000 دقيقة/شهر مجانًا)، GitHub Pages، Groq
  (باقة مجانية)، YouTube Data API (حصة مجانية يومية)، Gmail (مجاني).
