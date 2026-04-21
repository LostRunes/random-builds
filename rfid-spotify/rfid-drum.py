import serial
import time
import pygame

# ---------------- INIT ----------------
pygame.mixer.init()

ser = serial.Serial('COM8', 9600)
time.sleep(2)

# ---------------- LOAD SOUNDS ----------------
kick = pygame.mixer.Sound("kick.mp3")
snare = pygame.mixer.Sound("snare.mp3")

# Optional: adjust volume (0 to 1)
kick.set_volume(1.0)
snare.set_volume(1.0)

# ---------------- MAIN LOOP ----------------
while True:
    uid = ser.readline().decode().strip()
    print("Scanned:", uid)

    if uid == "C6 1D 7A F8":
        print("Kick 🥁")
        kick.play()

    elif uid == "AB 86 3D 0C":
        print("Snare 🥁")
        snare.play()