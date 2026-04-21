import serial
import time
import webbrowser

ser = serial.Serial('COM13', 9600)
time.sleep(2)

last_uid = ""

while True:
    uid = ser.readline().decode().strip()

    if uid == last_uid:
        continue

    last_uid = uid
    print("Scanned:", uid)

    if uid == "C6 1D 7A F8":
        print("Playing Song 1")
        webbrowser.open("https://open.spotify.com/track/6bZuZKR8hoyzZXNh1IW2Bu", new=0)

    elif uid == "AB 86 3D 0C":
        print("Playing Song 2")
        webbrowser.open("https://open.spotify.com/track/02sy7FAs8dkDNYsHp4Ul3f", new=0)