import pyperclip
import keyboard
import requests
import time
import re
import os

API_KEY = "AIzaSyCu8AgJwAnMLmkMBCdK5CEyjYx--OmX_HM"

last_answer = None
STOP = False
BUSY = False

# 🔥 CHANGE THIS TO YOUR SD CARD DRIVE LETTER
SD_PATH = "E:/answer.txt"


# 🛑 EMERGENCY STOP
def emergency_stop():
    global STOP
    STOP = True
    print("\n🚨 EMERGENCY STOP ACTIVATED")


keyboard.add_hotkey('ctrl+alt+x', emergency_stop)


# 🌐 GEMINI CALL (WITH RETRY)
def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    for _ in range(3):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            time.sleep(1)

    return "// Error getting response"


# 🧼 CLEAN OUTPUT
def clean_code(text):
    text = re.sub(r"```.*?\n", "", text)
    text = text.replace("```", "")
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text


# 📐 NORMALIZE
def normalize_indentation(text):
    lines = text.split('\n')
    return '\n'.join([line.rstrip() for line in lines])


# 💾 SAVE TO SD
def save_to_sd(text):
    try:
        with open(SD_PATH, "w", encoding="utf-8") as f:
            f.write(text)
        print("💾 Saved to SD")
    except:
        print("⚠️ SD write failed")


# 📂 LOAD FROM SD
def load_from_sd():
    try:
        if os.path.exists(SD_PATH):
            with open(SD_PATH, "r", encoding="utf-8") as f:
                return f.read()
    except:
        pass
    return None


# 🧹 DELETE FILE
def delete_sd():
    try:
        if os.path.exists(SD_PATH):
            os.remove(SD_PATH)
            print("🧹 SD cleaned")
    except:
        pass


# ⌨️ SAFE TYPING (YOUR STABLE VERSION)
def type_text(text):
    global STOP

    chunk_size = 1

    for i in range(0, len(text), chunk_size):

        if STOP:
            print("⛔ Typing stopped")
            return

        chunk = text[i:i+chunk_size]

        pyperclip.copy(chunk)
        keyboard.press_and_release('ctrl+v')

        time.sleep(0.1)


# 🟢 CAPTURE QUESTION
def capture_question():
    global last_answer, BUSY, STOP

    if BUSY:
        print("⚠️ Busy")
        return

    BUSY = True
    STOP = False

    print("\n📥 CAPTURE TRIGGERED")

    keyboard.press_and_release('ctrl+c')
    time.sleep(0.4)

    question = pyperclip.paste()

    print("Length:", len(question))

    if not question.strip() or len(question) < 50:
        print("⚠️ Invalid selection")
        BUSY = False
        return

    print("📡 Sending to Gemini...")

    response = call_gemini(
        "Give clean, properly formatted Java code only. No explanation:\n" + question
    )

    if response.startswith("// Error") or len(response) < 20:
        print("❌ API failed")
    else:
        last_answer = normalize_indentation(clean_code(response))
        save_to_sd(last_answer)
        print("✅ Answer ready & saved")

    BUSY = False


# 🔵 TYPE ANSWER
def type_answer():
    global last_answer, STOP, BUSY

    if BUSY:
        print("⚠️ Busy")
        return

    STOP = False

    print("\n⌨️ TYPE TRIGGERED")

    # 🔥 Try SD first (portable mode)
    sd_data = load_from_sd()

    if sd_data:
        print("📂 Loaded from SD")
        last_answer = sd_data

    if not last_answer:
        print("❌ No answer available")
        return

    print("⚠️ Typing starts (Ctrl+Alt+X to stop)")
    time.sleep(1)

    type_text(last_answer)

    print("✅ Done typing")

    # 🧹 Optional auto delete
    delete_sd()


# 🔥 HOTKEYS (MULTI TRIGGER)
keyboard.add_hotkey('ctrl+alt+c', capture_question)
keyboard.add_hotkey('ctrl+alt+t', type_answer)
keyboard.add_hotkey('ctrl+alt+x', emergency_stop)

print("🚀 Running...")
print("CTRL+ALT+C → Capture | CTRL+ALT+T → Type | CTRL+ALT+X → STOP")

keyboard.wait('esc')