# مشروع استخراج وترجمة النصوص من الفيديوهات

### وصف المشروع

#### الجزء الأول: استخراج الصوت والنص من الفيديوهات (prosess_1.py)
- يقوم البرنامج بتحويل ملفات الفيديو بصيغة `.ts` إلى صوت بصيغة `.wav`.
- يستخدم مكتبة Whisper لاستخراج النصوص من الصوت وتحويلها إلى ملف نصي بصيغة `.srt`.
- يتطلب من المستخدم تحديد مجلد يحتوي على الفيديوهات ومجلد آخر لحفظ النتائج.
- يمكن للمستخدم رؤية تقدم العملية من خلال شريط التقدم، بالإضافة إلى سجل الأحداث.

#### الجزء الثاني: ترجمة النصوص (prosess_2.py)
- يقوم البرنامج بترجمة ملفات `.srt` باستخدام مكتبة GoogleTranslator.
- يقوم بحفظ الملفات المترجمة في مجلد آخر يحدده المستخدم.
- يدعم البرنامج تحديد اللغة المصدر واللغة الهدف (افتراضياً من الإنجليزية إلى العربية).

---

### خطوات تشغيل المشروع

#### 1. إعداد البيئة
1. **تثبيت مكتبات بايثون المطلوبة:**
   - استخدم الأمر التالي لتثبيت المكتبات:
     ```bash
     pip install openai-whisper PyQt6 deep-translator ffmpeg-python
     ```
2. **تثبيت FFmpeg:**
   - قم بتحميل FFmpeg وتثبيته على جهازك، ثم تأكد من إضافته إلى متغيرات البيئة (PATH).

#### 2. تشغيل الجزء الأول (prosess_1.py)
1. افتح الملف `prosess_1.py` باستخدام محرر النصوص.
2. شغل البرنامج لتحديد مجلد الفيديوهات ومجلد الإخراج.
3. اضغط على "Start Transcription" لبدء عملية تحويل الفيديوهات إلى نصوص بصيغة `.srt`.

#### 3. تشغيل الجزء الثاني (prosess_2.py)
1. افتح الملف `prosess_2.py`.
2. حدد مجلد ملفات `.srt` والمجلد الذي تريد حفظ النصوص المترجمة فيه.
3. اضغط على "Start Translation" لبدء عملية الترجمة.

---

### ملاحظات
1. **إعادة تسمية الملفات:** إذا كنت تحتاج إلى ترجمة النصوص وإضافتها إلى الفيديو، يجب عليك:
   - تعديل أسماء الملفات الناتجة لتتناسب مع أسماء الفيديوهات الأصلية.
   - استخدام أدوات تحرير الفيديو لإضافة ملفات `.srt` إلى الفيديو.

2. **مشاكل متوقعة:**
   - إذا ظهرت أخطاء أثناء الترجمة، يمكن أن تكون بسبب قيود مكتبة GoogleTranslator (مثل عدد الطلبات الكبير).
   - تأكد من توافق ترميز النصوص (UTF-8) في جميع الملفات.

---

### شرح باللغة الإنجليزية

#### Project Description
1. **Part 1 (prosess_1.py):**
   - Extracts audio from `.ts` video files and saves it as `.wav`.
   - Uses the Whisper library to transcribe audio and save subtitles in `.srt` format.
   - Users specify input/output folders, and progress is displayed in the GUI.

2. **Part 2 (prosess_2.py):**
   - Translates `.srt` files using the GoogleTranslator library.
   - Saves the translated subtitles in a new output folder.
   - Supports setting the source and target languages (default: English to Arabic).

---

### Steps to Run

1. **Environment Setup:**
   - Install required Python libraries:
     ```bash
     pip install openai-whisper PyQt6 deep-translator ffmpeg-python
     ```
   - Install FFmpeg and add it to the PATH.

2. **Running Part 1 (prosess_1.py):**
   - Open `prosess_1.py` and execute the script.
   - Select video and output folders in the GUI.
   - Click "Start Transcription" to process videos.

3. **Running Part 2 (prosess_2.py):**
   - Open `prosess_2.py` and execute the script.
   - Select input and output folders for `.srt` files in the GUI.
   - Click "Start Translation" to process subtitles.

---

### Notes
1. **Renaming Files:**
   - To merge translated subtitles with videos, ensure filenames match the original videos.
   - Use video editing tools to add `.srt` files to videos.

2. **Troubleshooting:**
   - Translation errors may occur due to rate limits in GoogleTranslator.
   - Ensure all files are UTF-8 encoded.

