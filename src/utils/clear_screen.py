import os
import time


def clear_screen():
    time.sleep(0.5)
    if os.name == "nt":
        _ = os.system("cls")
    else:
        os.system("clear")
