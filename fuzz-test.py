from fuzzywuzzy import process
import time
import os

console = input("Enter console name: ")
rom = input("Enter rom name: ")

consolePath = "/home/john/Desktop/roms/" + console + "/"
romPath = "/home/john/Desktop/roms/" + console + "/" + rom

romsearch = os.listdir(consolePath)

if os.path.isfile(consolePath):
    print("ok")

else:
    print("Nope")
    print(process.extract(rom, romsearch))
