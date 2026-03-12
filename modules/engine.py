import os

def get_high():
    if not os.path.exists("highscore.txt"): return 0
    try:
        with open("highscore.txt", "r") as f: return int(f.read())
    except: return 0

def save_high(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))