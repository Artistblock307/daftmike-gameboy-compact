import os
import time
import subprocess

def main():
    console = input("Enter console name: ")
    rom = input("Enter rom name: ")   

    procnames = ["retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
                 "atari800", "xroar", "vice", "daphne", "reicast", "pifba", "osmose", "gpsp", "jzintv",
                 "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
                 "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
                 "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
                 "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
                 "wolf4sdl", "solarus", "emulationstation"]
    
    print("CART READ BEGIN")
    
    #rompath = "/home/pi/RetroPie/roms/" + console + "/" + rom
    #consolePath = "/home/john/Desktop/roms/" + console + "/"

    romPath = "/home/john/Desktop/roms/" + console + "/" + rom
    consolePath = "/home/john/Desktop/roms/" + console + "/"

    consoleOk = checkConsole(consolePath, console)
    romOk = checkRom(romPath, rom)
    
def checkConsole(consolePath, console):
    if os.path.isdir(consolePath):
        consoleOk = True
        print(console.upper() + "? ...[OK]")
        return consoleOk
        
    elif console == "runScript":
        consoleOk = True
        print("run Script? ...[OK]\n")
        return consoleOk
            
    else:
        consoleOk = True
        print(console.upper() + "? ...[WHAT?]\n")
        return consoleOk

def checkRom(romPath, rom):
    if os.path.isfile(romPath):
        romOk = True
        print(rom + "? ...[VALID]")
        return romOk

    else:
        romOk = False
        print(rom + " ...[FILE ERROR]\n")
        return romOk

main()
