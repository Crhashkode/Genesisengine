# run.py

import subprocess

print("=== GENESIS ENGINE ONLINE ===")
print("Choose mode:")
print("1. Command Line")
print("2. Discord Bot (if available)")

mode = input("Enter option: ")

if mode == "1":
    subprocess.run(["python3", "main.py"])

elif mode == "2":
    subprocess.run(["python3", "flame_bot.py"])

else:
    print("Invalid option. Shutting down.")
