import os
import gradio as gr
from groq import Groq

# ==================== جميع الموديلات الفابور اللي كتدعم العربية 2026 ====================
MODELS = [
    "allam-2-7b",                                      # 1- أحسن واحد للعربية - سعودي أصلي
    "openai/gpt-oss-120b",                             # 2- أقوى واحد - ذكاء عالي
    "openai/gpt-oss-20b",                              # 3- سريع وخفيف
    "qwen/qwen3-32b",                                  # 4- ممتاز فالدارجة المغربية
    "【entity-meta¦canonical_name=Meta】-llama/llama-4-scout-17b-16e-instruct",        # 5- جديد من 【entity-Meta¦canonical_name=Meta】 - فابور
]

SYSTEM_PROMPT = """أنت الأستاذ ديالي، أستاذ ذكاء اصطناعي مغربي من تامسينت.
تشرح المفاهيم بالدارجة المغربية البسيطة والعربية الفصحى المبسطة.
- إلا سولك المستخدم بالدارجة، جاوب بالدارجة
- إلا سولك بالفصحى، جاوب بالفصحى
- شرحك يكون بسيط، واضح، بأمثلة مغربية
- ديما خليك أستاذ محترم وكيشجع الطلاب
"""

def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise gr.Error("❌ GROQ_API_KEY ما كاينش! زيدو فـ Back4app Environment Variables")
    if not api_key.startswith("gsk_"):
        raise gr.Error("❌ المفتاح خاصو يبدا بـ gsk_")
    return Groq(api_key=api_key)

def bot_reply(message, history):
    print(f"[DEBUG] User: {message}")
    client = get_client()

    # بناء الرسائل
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for turn in history:
        if isinstance(turn, dict) and "role" in turn and "content" in turn:
            messages.append({"role": turn["role"], "content": turn["content"]})
    
    messages.append({"role": "user", "content": message})

    # جرب الموديلات واحد بواحد
    last_error = None
    for model_name in MODELS:
        try:
            print(f"[TRY] {model_name}...")
            completion = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
            )
            reply = completion.choices[0].message.content
            print(f"[OK] {model_name}")
            return reply
        except Exception as e:
            print(f"[FAIL] {model_name}: {e}")
            last_error = e
            continue

    raise gr.Error(f"❌ كل الموديلات واقفة دابا. آخر خطأ: {last_error}")

# ==================== الواجهة ====================
with gr.Blocks(title="الأستاذ ديالي", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🎓 الأستاذ ديالي
        ### أستاذ الذكاء الاصطناعي بالدارجة المغربية
        سولني أي حاجة على الذكاء الاصطناعي!
        """
    )
    gr.ChatInterface(
        fn=bot_reply,
        title=None,
        examples=[
            "شنو هو الذكاء الاصطناعي؟",
            "شرح ليا الشبكات العصبية بالدارجة",
            "شنو الفرق بين Machine Learning و Deep Learning؟",
            "كيفاش نتعلم البرمجة؟",
        ],
    )

# ضروري لـ Back4app
demo.queue().launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
)
