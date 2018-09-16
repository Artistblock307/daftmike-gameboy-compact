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

    romsearch = os.listdir(consolePath)
    consoleOk = checkConsole(consolePath, console)
    fuzzyRom = fuzzySelect(rom, romsearch)

    emulators = {"nes":"nestopia", "snes":"snes9x", "n64":"mupen64plus", "gb":"gambatte", "gbc":"gambatte", "gba":"mgba", "ps1":"mednafen_psx", "psp":"ppsspp"}

    emulateRun(console, consoleOk, consolePath, emulators, rom, fuzzyRom)

def emulateRun(console, consoleOk, consolePath, emulators, rom, fuzzyRom):
    if consoleOk == True:
        os.system("retroarch -L /usr/lib/libretro/" + emulators[console] + "_libretro.so " + consolePath + fuzzyRom)
        print(fuzzyRom)
    
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

def fuzzySelect(rom, romsearch):
    x = process.extract(rom, romsearch)

    a = []
    c = []

    x = list(sum(x, ())) 

    for i in range(len(x)):
        if i % 2 == 0:
            if ".zip" in x[i]:
                a.append(x[i])
                c.append(x[i + 1])

    fuzzyRom = "\'" + a[0] + "\'"
    print(a[0])
    print(a)
    print(c)
    
    return fuzzyRom

main()
