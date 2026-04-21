import os

for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    path = f"{drive}:/"
    if os.path.exists(path):
        print(path)