import pyperclip
import keyboard
import pyautogui
import requests
import time

API_KEY = "AIzaSyDumgN64XAmigu8HmDoPCK457Ys3hn9cP8"  # ⚠️ regenerate your key later

last_answer = None


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


# 🔥 PROPER TYPING FUNCTION (no paste)
def type_text(text):
    for char in text:
        if char == '\n':
            keyboard.press_and_release('enter')
            time.sleep(0.05)
        else:
            keyboard.write(char)
            time.sleep(0.015)  # 🔧 adjust speed here


def solve():
    global last_answer

    time.sleep(0.2)

    # 🔹 Save old clipboard
    old_clip = pyperclip.paste()

    # 🔹 Try copying
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.4)

    new_clip = pyperclip.paste()

    # 🔥 CASE 1: Text selected → process
    if new_clip.strip() and new_clip != old_clip:
        question = new_clip

        last_answer = call_gemini(
            "Give only clean code answer without explanation:\n" + question
        )

        # 🔥 Clean formatting (important)
        last_answer = last_answer.replace("```", "")

        return

    # 🔥 CASE 2: No selection → type
    if last_answer:
        time.sleep(0.2)

        pyautogui.press('enter')
        time.sleep(0.4)

        type_text(last_answer)


# 🔥 Single hotkey (Arduino triggers this)
keyboard.add_hotkey('ctrl+alt+g', solve)

print("Running... Single trigger mode 😏 (ESC to exit)")
keyboard.wait('esc')