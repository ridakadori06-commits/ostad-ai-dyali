import os
import gradio as gr
from groq import Groq

MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

SYSTEM = "أنت أستاذ ذكاء اصطناعي مغربي، تجاوب ديما بالدارجة المغربية البسيطة."

def reply(msg, hist):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    messages = [{"role":"system","content":SYSTEM}]
    for h in hist[-6:]:
        if isinstance(h, dict): messages.append(h)
    messages.append({"role":"user","content":msg})
    for m in MODELS:
        try:
            r = client.chat.completions.create(model=m, messages=messages, max_tokens=1024)
            return r.choices[0].message.content
        except: continue
    return "عاود سولني تاني"

demo = gr.ChatInterface(fn=reply, title="🎓 الأستاذ ديالي")
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
