import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def generate_answer(question, context):

    prompt = f"""
        تو یک دستیار آموزشی دانشگاه هستی.

        وظیفه تو پاسخ دادن به سؤالات دانشجویان
        فقط بر اساس متن آیین‌نامه است.

       
        قوانین پاسخ‌گویی:

        1. فقط بر اساس متن آیین‌نامه پاسخ بده.
        2. هیچ قانون، عدد، شرط یا تبصره‌ای را از دانش خودت اضافه نکن.
        3. قبل از پاسخ، تمام بخش‌های مرتبط متن را بررسی کن.
        4. تمام شرط‌های ذکرشده در متن را در پاسخ حفظ کن.
        5. اعداد، محدودیت‌ها و شماره مواد را دقیقاً مطابق متن بنویس.
        6. بین شرایط الزامی و اختیاری تفاوت قائل شو.
        7. اگر یک قانون مشروط به تأیید یا مجوز خاصی است،
        حتماً آن شرط را در پاسخ ذکر کن.
        8. اگر اطلاعات کافی برای پاسخ وجود ندارد، حدس نزن
        و بگو: اطلاعات کافی در آیین‌نامه وجود ندارد.
        9. پاسخ را متناسب با سؤال بنویس.
        10. اگر سؤال نیازمند بررسی کامل چند شرط است،
            تمام شرایط مرتبط را به صورت فهرست شماره‌گذاری‌شده بیان کن.
        11. هیچ‌گاه صرفاً به دلیل پیدا نکردن محدودیت در متن،
            نتیجه نگیر که انجام یک کار مجاز است.


        متن آیین‌نامه:
        {context}

        سؤال دانشجو:
        {question}

        پاسخ:
        """

    data = {
        "model": "qwen2.5:7b",
        "prompt": prompt,
        "stream": True,
        "keep_alive": "30m",
        "options": {
            "temperature": 0,
            "num_predict": 512
        }
    }

    request = Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urlopen(request) as response:

            for line in response:
                if line:
                    result = json.loads(line.decode("utf-8"))

                    token = result.get("response", "")

                    if token:
                        yield token

                    if result.get("done"):
                        break

    except HTTPError as error:
        print("Ollama API Error:")
        print(error.read().decode("utf-8"))
        raise
