
from src.generation import generate_answer


question = "شرایط مشروط شدن دانشجو چیست؟"

context = """
مشروطی وضعیتی است که دانشجو در یک نیمسال،
میانگین کمتر از حد نصاب تعیین‌شده در دوره تحصیلی
کارشناسی را کسب کرده باشد.

ماده 16:
چنانچه میانگین نمرات دانشجو در هر نیمسال تحصیلی
کمتر از 12 باشد، آن نیمسال مشروط تلقی می‌شود.
"""

answer = generate_answer(question, context)

print("Question:")
print(question)

print("\nGenerated Answer:")
print(answer)
