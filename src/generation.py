import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

def generate_answer(question, context):
    prompt = f"""
        تو یک دستیار آموزشی دانشگاه هستی.

        وظیفه تو پاسخ دادن به سؤالات دانشجویان
        فقط بر اساس متن آیین‌نامه است.

        قوانین:
        1. فقط از اطلاعات موجود در متن استفاده کن.
        2. هیچ اطلاعاتی از دانش خودت اضافه نکن.
        3. پاسخ را مستقیم و بدون مقدمه بنویس.
        4. از جمله‌بندی طبیعی و صحیح فارسی استفاده کن.
        5. اصطلاحات و اعداد موجود در آیین‌نامه را دقیق حفظ کن.
        6. اگر پاسخ در متن وجود ندارد، بگو:
        اطلاعات کافی در آیین‌نامه وجود ندارد.
        7. پاسخ را کوتاه و در یک یا دو جمله بنویس.

        متن آیین‌نامه:
        {context}

        سؤال دانشجو:
        {question}

        پاسخ:
        """

    data = {
        "model": "qwen2.5:7b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 128
        }
    }

    request = Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        print("Ollama API Error:")
        print(error.read().decode("utf-8"))
        raise

    return result["response"].strip()
