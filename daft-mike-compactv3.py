import os
import time
import subprocess
from fuzzywuzzy import process

def main():

    console = input("Enter console name: ")
    rom = input("Enter rom name: ")

    #rompath = "/home/pi/RetroPie/roms/" + console + "/" + rom
    #consolePath = "/home/pi/RetroPie/roms/" + console + "/"

    romPath = "/home/john/Desktop/roms/" + console + "/" + rom
    consolePath = "/home/john/Desktop/roms/" + console + "/"

    consoleOk = checkConsole(consolePath, console)
    romOk = checkRom(romPath, rom)

    emulators = {"nes":"nestopia", "snes":"snes9x", "n64":"mupen64plus", "gb":"gambatte", "gbc":"gambatte", "gba":"mgba", "ps1":"mednafen_psx", "psp":"ppsspp"}
    romsearch = os.listdir(consolePath)

    if consoleOk and romOk == True:
        os.system("retroarch -L /usr/lib/libretro/" + emulators[console] + "_libretro.so " + consolePath + "\'" + rom + ".zip\'")
        print(process.extract(rom, romsearch, limit=3))

def checkConsole(consolePath, console):
    if os.path.isdir(consolePath):
        consoleOk = True
        print(console.upper() + "? ... [OK]")
        time.sleep(1)
        return consoleOk
        
    elif console == "runScript":
        consoleOk = True
        print("run Script? ... [OK]\n")
        time.sleep(1)
        return consoleOk
            
    else:
        consoleOk = True
        print(console.upper() + "? ... [WHAT?]\n")
        time.sleep(1)
        return consoleOk

def checkRom(romPath, rom):
    if os.path.isfile(romPath):
        romOk = True
        print(rom + "? ... [VALID]")
        time.sleep(1)
        return romOk

    else:
        romOk = False
        print(rom + " ... [FILE ERROR]\n")
        time.sleep(1)
        return romOk

main()
