import pyperclip
import keyboard
import pyautogui
import requests
import time
import re

API_KEY = "AIzaSyC4frbcIoE3u-0dJcG5DrJ85__aIAwaREE" #AIzaSyCu8AgJwAnMLmkMBCdK5CEyjYx--OmX_HM

last_answer = None
STOP = False
BUSY = False


# 🛑 EMERGENCY STOP
def emergency_stop():
    global STOP
    STOP = True
    print("\n🚨 EMERGENCY STOP ACTIVATED")


keyboard.add_hotkey('ctrl+alt+x', emergency_stop)


# 🌐 GEMINI CALL
def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "// Error getting response"


# 🧼 CLEAN OUTPUT
def clean_code(text):
    text = re.sub(r"```.*?\n", "", text)
    text = text.replace("```", "")
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text


# 📐 NORMALIZE INDENTATION
def normalize_indentation(text):
    lines = text.split('\n')
    cleaned = []

    for line in lines:
        cleaned.append(line.rstrip())

    return '\n'.join(cleaned)


# ⌨️ SAFE LINE-BY-LINE TYPING
def type_text(text):
    global STOP

    chunk_size = 1   #1 # number of chars per chunk

    for i in range(0, len(text), chunk_size):

        if STOP:
            print("⛔ Typing stopped")
            return

        chunk = text[i:i+chunk_size]

        pyperclip.copy(chunk)
        keyboard.press_and_release('ctrl+v')

        time.sleep(0.1)  #0.1# adjust speed  # 🔥 THIS controls smoothness

# 🧠 MAIN LOGIC
def solve():
    global last_answer, BUSY, STOP

    if BUSY:
        print("⚠️ Already processing")
        return

    BUSY = True
    STOP = False

    time.sleep(0.2)

    print("\n--- TRIGGERED ---")

    # 🔹 Copy selection
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.4)

    new_clip = pyperclip.paste()

    print("Clipboard content:")
    print(new_clip[:200])
    print("Length:", len(new_clip))

    # 🔥 CASE 1: QUESTION MODE
    if new_clip.strip() and len(new_clip) > 50:
        print("\n📡 Sending to Gemini...")

        last_answer = call_gemini(
            "Give clean, properly formatted code only. No explanation, use java:\n" + new_clip
        )

        # 🧼 CLEAN + FORMAT
        last_answer = clean_code(last_answer)
        last_answer = normalize_indentation(last_answer)

        print("\n✅ Answer ready")
        BUSY = False
        return

    # 🔥 CASE 2: TYPE MODE
    if last_answer:
        print("\n⚠️ About to type... (Ctrl+Alt+X to stop)")
        time.sleep(1)

        print("⌨️ Typing...")

        # Ensure focus
        # pyautogui.click()
        time.sleep(0.2)

        type_text(last_answer)

        print("\n✅ Done typing")

    BUSY = False


# 🔥 HOTKEY (Arduino triggers this)
keyboard.add_hotkey('ctrl+alt+g', solve)

print("🚀 Running... (Ctrl+Alt+G = trigger | Ctrl+Alt+X = STOP)")
keyboard.wait('esc')