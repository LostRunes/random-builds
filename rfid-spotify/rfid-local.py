import serial
import time
import pygame

# ---------------- INIT ----------------
pygame.mixer.init()

ser = serial.Serial('COM8', 9600)
time.sleep(2)

last_uid = ""

# ---------------- SONG PATHS ----------------
SONG_1 = "Lovers_spotdown.org.mp3"
SONG_2 = "Soda Pop_spotdown.org.mp3"

# ---------------- FUNCTION ----------------
def play_song(song):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

# ---------------- MAIN LOOP ----------------
while True:
    uid = ser.readline().decode().strip()

    if uid == last_uid:
        continue

    last_uid = uid
    print("Scanned:", uid)

    if uid == "C6 1D 7A F8":
        print("Playing lovers 🎵")
        play_song(SONG_1)

    elif uid == "AB 86 3D 0C":
        print("Playing sodapop 🎵")
        play_song(SONG_2)