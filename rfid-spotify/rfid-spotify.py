import serial
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ---------------- SPOTIFY SETUP ----------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="0a8fdfdaf39a442d83f343edd80a4337",
    client_secret="0ff92cd7966c4620a9a82a658fc8986c",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-modify-playback-state user-read-playback-state"
))

# ---------------- ARDUINO SERIAL ----------------
ser = serial.Serial('COM13', 9600)
time.sleep(2)

# ---------------- GET DEVICE ----------------
devices = sp.devices()
DEVICE_ID = devices['devices'][0]['id']  # picks your active device

print("Using Device:", devices['devices'][0]['name'])

# ---------------- UID MEMORY ----------------
last_uid = ""

# ---------------- SONG IDS ----------------
SONG_1 = "spotify:track:6bZuZKR8hoyzZXNh1IW2Bu"
SONG_2 = "spotify:track:02sy7FAs8dkDNYsHp4Ul3f"

# ---------------- MAIN LOOP ----------------
while True:
    uid = ser.readline().decode().strip()

    if uid == last_uid:
        continue  # ignore repeats

    last_uid = uid
    print("Scanned:", uid)

    try:
        if uid == "C6 1D 7A F8":
            print("Playing Song 1")

            sp.transfer_playback(device_id=DEVICE_ID, force_play=True)
            time.sleep(0.2)

            sp.start_playback(device_id=DEVICE_ID, uris=[SONG_1])

        elif uid == "AB 86 3D 0C":
            print("Playing Song 2")

            sp.transfer_playback(device_id=DEVICE_ID, force_play=True)
            time.sleep(0.2)

            sp.start_playback(device_id=DEVICE_ID, uris=[SONG_2])

    except Exception as e:
        print("Error:", e)