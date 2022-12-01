
<img src="autoDA.png" width="300" >

# Automated Domain Admin pwning tool.

The purpose of this tool is to automate specific procedures during Internal Penetration Test Engagements. (crackmapexec, responder, ntlmrelayx, sam and lsass dumping, pypykatz).<br> Depending on the target Active Directory Architecture and its policies, autoDA may not return DA credentials, but it will create and organize files containing captured hashes, users, IPs and sam dumps which will help you on your next moves during your Engagement.

Please note that the script must be executed from a **sudoer** user, since responder needs root privileges.

Feel free to tweak the script upon your needs, and change the **time.sleep()** commands depending on your networking latencies.

<u>**DISCLAIMER:**</u> This tool is focused on Internal PTs and is not recommended for Red Teaming Engagements, since it's too loud :P 

<br>

## Requirements
```
crackmapexec
responder
impacket
pyautogui
pypykatz
```
<br>

## Usage
```
python3 autoDA.py -i <interface> -s <subnet>
```
<br>

## autoDA in action!
![](autoDA.gif)
<br>

## Written By:<br>fastpistol & chrm4n
