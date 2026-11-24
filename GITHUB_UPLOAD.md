# رفع مشروع "البئر التي تمنى فيها الجميع نفس الشيء" على GitHub

## 📋 ملخص

هذا المشروع جاهز للعمل على **GitHub Actions** — سيرسم الفيديو في السحابة مجاناً ويعطيك ملف `video.mp4` للتحميل.

---

## 🚀 الخطوات (5 دقائق)

### 1. اعمل Repository جديد على GitHub
- ادخل على **github.com** → زر **New repository** (الأخضر)
- الاسم: `well-wishes-cartoon` (أو أي اسم)
- **Public** أو **Private** — كلهم يمشوا
- **لا** تختار "Add README" ولا ".gitignore" ولا "License"
- اضغط **Create repository**

### 2. ارفع الملفات (طريقة الويب - أسهل)
في صفحة الريبو الجديد، اضغط **"uploading an existing file"** أو اسحب المجلد كاملاً:

```
اسحب المجلد: shorts/well-wishes/
```
**مهم:** تأكد إن `voice.mp3` موجود في `shorts/well-wishes/voice.mp3`

### 3. إذا `voice.mp3` كبير (>25 MB)
GitHub يرفض الملفات الكبيرة في الويب. حلول:
- **Git LFS** (أسهل): في الريبو، Settings → Actions → General → Allow Git LFS
- أو ارفعه يدوياً بعد ما تشتغل Actions مرة وتفشل، من صفحة Actions أضفه كـ artifact

### 4. شغّل الـ Workflow
- ادخل تبويب **Actions** في الريبو
- اختر **"Render Cartoon Short - Well Wishes"** من اليسار
- اضغط **Run workflow** (الأخضر يمين) → **Run workflow**
- استنِ 10–20 دقيقة

### 5. حمّل الفيديو
- لما يخلص (أخضر ✅)، اضغط على الـ run
- في الأسفل: **Artifacts** → حمل `cartoon-short-video`
- فك الضغط → لقي `video.mp4`

---

## 📁 هيكل المجلد اللي ترفعه

```
well-wishes-cartoon/          ← اسم الريبو
├── .github/
│   └── workflows/
│       └── render-video.yml
├── shorts/
│   └── well-wishes/
│       ├── voice.mp3              ← **مطلوب!** ضعه هنا
│       ├── script.txt
│       ├── audio.py
│       ├── timing.py
│       ├── render.mjs
│       ├── sheet.py
│       ├── mix.py
│       ├── finish.sh
│       ├── requirements.txt
│       ├── package.json
│       ├── package-lock.json     ← يتولد بعد npm install
│       ├── web/
│       │   ├── index.html
│       │   ├── main.js
│       │   ├── story.js
│       │   ├── toon.js
│       │   ├── roman.js
│       │   ├── paint.js
│       │   ├── motion.js
│       │   ├── lib/
│       │   │   └── three.module.js
│       │   └── fonts/
│       │       └── Lalezar-Regular.ttf
│       ├── work/                 ← يتولد
│       ├── stills/               ← يتولد
│       └── out/                  ← الفيديو النهائي هنا
```

---

## 🎙️ **تسجيل التعليق الصوتي (voice.mp3)**

سجل النص التالي في `script.txt` بصوتك (أو استخدم ElevenLabs v3 مع tags):

```
في قرية صغيرة، بئر قديمة. كل واحد يرمي عملة ويتمنى.

التاجر تمنى: "ربح وفير". الفلاح: "مطر غزير". العروس: "زوج وفيّ". الشيخ: "صحة وعافية".

لكن الغريب: كل عملة بتلمس المية، المية بتلمع.

لما نظروا لقوا كلهم تمنوا نفس الشيء — "جارهم يكون مبسوط".

القرية كلها سعدت. والبئر لسه لحد النهاردة بتلمع.
```

**نصائح التسجيل:**
- صوت راوٍ واحد، دافئ، ثابت
- سرعة طبيعية، وقفات طبيعية في نهاية الجمل
- بدون موسيقى في الخلفية
- MP3 أو WAV، 48kHz أو 44.1kHz
- المدة المتوقعة: ~27 ثانية

---

## ❗ مشاكل شائعة وحلولها

| المشكلة | الحل |
|----------|------|
| `voice.mp3 not found` | تأكد إن الملف في `shorts/well-wishes/voice.mp3` مش في الجذر |
| `npm ci` يفشل | امسح `package-lock.json` وارفع من جديد |
| `playwright install` يفشل | الـ workflow يثبت deps، جرب إعادة تشغيل |
| الفيديو ما طلع | شوف `qa_sheet.jpg` في artifacts — يبين لو في إطارات سوداء/متجمدة |
| ياخذ وقت طويل | الـ timeout 60 دقيقة، كافي لـ 810 إطار |
| توقيتات عربية غلط | تأكد إن `--lang ar` في أمر timing.py |

---

## 🎬 بعد ما تخلص

الفيديو النهائي: **1080×1920، 30fps، ~27 ثانية، H.264 + AAC**

شغّله على الموبايل — مصمم لـ **Shorts/Reels/TikTok** (عمودي).

---

## 🆘 محتاج مساعدة؟

إذا علقت في أي خطوة، قولي:
1. أي خطوة وصلت لها
2. أي رسالة خطأ طلعت
3. صورت شاشة لو تقدر

وساعدك تكمل!