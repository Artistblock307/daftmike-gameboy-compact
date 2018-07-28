import os
import time
import serial
import subprocess

def main():
    
    console = decodeInput()
    rom = decodeInput()

    procnames = ["retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
                 "atari800", "xroar", "vice", "daphne", "reicast", "pifba", "osmose", "gpsp", "jzintv",
                 "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
                 "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
                 "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
                 "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
                 "wolf4sdl", "solarus", "emulationstation"]
    
    print("CART READ BEGIN")
    
    #rompath = "/home/pi/RetroPie/roms/" + console + "/" + rom
    #consolePath = "/home/pi/RetroPie/roms/" + console + "/"

    romPath = "/home/john/Desktop/roms/" + console + "/" + rom
    consolePath = "/home/john/Desktop/roms/" + console + "/"

    consoleOk = checkConsole(consolePath, console)
    romOk = checkRom(romPath, rom)

def decodeInput():
    ser = serial.Serial("/dev/ttyACM0", 9600, timeout=5)

    while True:
    try:
        line = ser.readline()
        if line != "":
            records = line[:-1].split(', ')

            console = records[0]
            rom = records[1]

    except IndexError:
        print "NDEF read error...\n"
        ser.write("bad")

    return(console, rom) 

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
