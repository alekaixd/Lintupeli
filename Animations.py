import time
import platform
import os
# Animation player script

# bird idle animation

# bird fly animation

# title text


def idle():
    fg = "\u001b[38;5;159m"
    PlayAnimation(ReadFile("./Animations/idle.txt"), 1.0, 2, fg)
    return


def fly():
    fg = "\u001b[38;5;159m"
    PlayAnimation(ReadFile("./Animations/fly.txt"), 0.6, 2, fg)


def ReadFile(fileName: str):
    file = open(fileName, "r").read().split("\n\n")
    return file


# Uses ansi escape codes to move cursor around
def PlayAnimation(
        frames: list,
        animSpeed: float,
        animLoops: int = 1,
        ansiColor: str = "\u001b[39",
        ansiBackground: str = "\u001b[49"):

    lines = frames[0].split("\n")
    frameX = len(lines[0])
    frameY = len(lines)
    ansiReset = "\u001b[39m\u001b[49m"
    print(f"{ansiColor}{ansiBackground}", end="")
    for frame in frames:
        for line in frame.split("\n"):
            print(ansiBackground + ansiColor + line + ansiReset)
        time.sleep(animSpeed)
        print(f"\u001b[{frameY}A\u001b[{frameX}D", end="")
        # moves the cursor back
    print(f"\u001b[{frameY}B{ansiReset}", end="")
    # moves the cursor down so the stuff after prints properly
    return


def Clear():  # if for some reason clear command is different
    if platform.system() == "Linux":
        os.system('clear')
    elif platform.system() == "Windows":
        os.system('cls')
