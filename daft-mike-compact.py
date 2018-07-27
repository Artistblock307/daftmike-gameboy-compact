import os
import psutil
import re
import serial
import socket
import subprocess
import time

procnames = ["retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
             "atari800", "xroar", "vice", "daphne", "reicast", "pifba", "osmose", "gpsp", "jzintv",
             "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
             "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
             "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
             "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
             "wolf4sdl", "solarus"]

emulators = ["amiga", "amstradcpc", "apple2", "arcade", "atari800", "atari2600", "atari5200", "atari7800",
             "atarilynx", "atarist", "c64", "coco", "dragon32", "dreamcast", "fba", "fds", "gamegear", "gb", "gba",
             "gbc", "intellivision", "macintosh", "mame-advmame", "mame-libretro", "mame-mame4all", "mastersystem",
             "megadrive", "msx", "n64", "neogeo", "nes", "ngp", "ngpc", "pc", "ports", "psp", "psx", "scummvm",
             "sega32x", "segacd", "sg-1000", "snes", "vectrex", "videopac", "wonderswan", "wonderswancolor",
             "zmachine", "zxspectrum"]

#Assume the cart is not valid until we've checked it in the main loop
cartok = False

# Setup the serial port and tell arduino we're ready (allows us to start with a cart already inserted at power-on)
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=None)
ser.write(b'ready')

# Main Loop
while True:
    try:
        line = ser.readline()
        if line != "":
            records = line[:-1].split(', ')  # incoming data looks like: "$$$, $$$, $$$, \n"

            uid = records[0]  # 'uid' is read from the NFC tag, also used for shutdown, reset and cart eject
            console = records[1]  # 'console' is NDEF Record #1
            rom = records[2]  # 'rom' is NDEF Record #2

    except IndexError:
        print("NDEF read error...\n")
        ser.write(b"bad")  # Tell the Arduino there was a cart read error

# Check serial data for a command message in the 1st field
    if uid == "shutdown":
        print("shutdown command received...\n")
        shutdown()

    if uid == "cart_eject":
        print("cart ejected...\n")
        cartok = False

    if uid == "reset":
        print("reset button pressed...\n")
        retroarch_command("RESET")

## Check the console and rom data for validity
    if console != "":
        if check_console(console):
            if check_rom(console, rom):
                emulatorpath = get_emulatorpath(console)
                rompath = get_rompath(console, rom)
                cartok = True

# Return the path of the emulator ready to be used later

def get_emulatorpath(console):
    path = "/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ " + console + " "
    return path

# Check that the rom is valid by looking for the file, tell the cart slot light green if good, red if bad

def check_rom(console, rom):
    # get full rom path and check if it's a file
    romfile = "/home/pi/RetroPie/roms/" + console + "/" + rom
    if os.path.isfile(romfile):
        print("Found \"" + rom + "\"\n")
        ser.write(b"ok")  # Tell Arduino the cart read was successful
        return True

    else:
        print("But couldn\'t find \"" + romfile + "\"")
        print("Check NDEF Record 2 contains a valid filename...\n")
        ser.write(b"bad")  # Tell Arduino there was a cart read error
        return False

# Return the full path of the rom read from NDEF record #2 on the NFC tag

def get_rompath(console, rom):
    # escape the spaces and brackets in rom filename
    rom = rom.replace(" ", "\ ")
    rom = rom.replace("(", "\(")
    rom = rom.replace(")", "\)")
    rom = rom.replace("'", "\\'")

    rompath = "/home/pi/RetroPie/roms/" + console + "/" + rom
    return rompath

def process_exists(proc_name):
    ps = subprocess.Popen("ps ax -o pid= -o args= ", shell=True, stdout=subprocess.PIPE)
    ps_pid = ps.pid
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    for line in output.split("\n"):
        res = re.findall("(\d+) (.*)", line)
        if res:
            pid = int(res[0][0])
            if proc_name in res[0][1] and pid != os.getpid() and pid != ps_pid:
                return True
    return False

# Kills the task of 'procnames', also forces Kodi to close if it's running

def killtasks(procnames):
    for proc in psutil.process_iter():
        if proc.name() in procnames:
            pid = str(proc.as_dict(attrs=['pid'])['pid'])
            name = proc.as_dict(attrs=['name'])['name']
            print("stopping... " + name + " (pid:" + pid + ")")
            subprocess.call(["sudo", "kill", "-15", pid])

    kodiproc = ["kodi", "kodi.bin"]  # kodi needs SIGKILL -9 to close
    for proc in psutil.process_iter():
        if proc.name() in kodiproc:
            pid = str(proc.as_dict(attrs=['pid'])['pid'])
            name = proc.as_dict(attrs=['name'])['name']
            print("stopping... " + name + " (pid:" + pid + ")")
            subprocess.call(["sudo", "kill", "-9", pid])

# Check if the console we read from NDEF Record #1 is valid, by checking against a list of supported emulators

def check_console(console):
    if console != "":
        if console in emulators:
            print("NDEF Record \"" + console + "\" is a valid system...\n")
            return True

        else:
            print("Could not find \"" + console + "\" in the supported systems list")
            print("Check NDEF Record 1 for a valid system name(all-lowercase)\n")
            ser.write(b"bad")  # Tell Arduino there was a cart read error
            return False

# If the cartridge is valid when the button is switched on then we can launch the rom

def button_on():
    if cartok:
        killtasks(procnames)
        killtasks("emulationstation")
        subprocess.call("sudo openvt -c 1 -s -f " + emulatorpath + rompath + "&", shell=True)
        subprocess.call("sudo chown pi -R /tmp", shell=True)  # ES needs permission as 'pi' to access this later
        time.sleep(1)
    else:
        print("no valid cartridge inserted...\n")

# Close the emulator when the button is pushed again ("off")

def button_off():
    ser.write(b"ready")
    if process_exists("emulationstation"):
        print("\nemulationstation is running...\n")
    else:
        killtasks(procnames)

#  I check if ES is running here because if it *is* then any running game was launched from within ES
#  and we don't want to quit it when the button is pressed. But if the game was launched from a cart
#  then ES will not be running in the background and we *do* want to quit the emulator.
