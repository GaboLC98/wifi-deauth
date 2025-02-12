import os
from datetime import datetime
from optparse import *
from pwn import * 

def signal_handler(signal, frame):
  sys.exit(0)

def pwn_start():
    log.info('MAC finder')
    return log.progress('')

def read_files(file,type):
    progress.status(f'Reading file: {file}')
    file = open(file, "r")
    if type == 'set' or type == 'dictionary':
        set_dictionary = eval(file.read())
        file.close()
        if type == 'set':
            return set(set_dictionary)
        else:
            return set_dictionary
    else:
        arp_scan = file.read()
        file.close()
        return str(arp_scan).split('$')

def save_files(file,type):
    save = open(f"{file}", "w")
    save.write(str(type))
    save.close()
    return True

signal.signal(signal.SIGINT, signal_handler)    
progress = pwn_start()

#Set creation
set_file = "mac_set.txt" 
set = read_files('mac_set.txt','set')

#Dictionary creation
dictionary_file = "mac_dictionary.txt"
dictionary = read_files('mac_dictionary.txt','dictionary') 

#Seting current date for updates
current_date = datetime.now()

#ARP scan, save and read
progress.status('Scanning MAC addresses')
os.system("sudo arp-scan -l -N -g -F '\\${mac}\\$' > arp_scan.txt")
mac_array = read_files('arp_scan.txt','scan')

counter_new = 0
counter_update = 0
for i in range(1,len(mac_array)-1):
    if mac_array[i] not in set:
        if '\n' not in mac_array[i]:
            set.add(mac_array[i])
            dictionary.update({mac_array[i]:f'{current_date}'})
            progress.status(f'{mac_array[i]} added to the Set and Dictionary')
            counter_new += 1
    else:
        dictionary.update({mac_array[i]:f'{current_date}'})
        progress.status(f'{mac_array[i]} updated on the Dictionary')
        counter_update += 1

#Saving the data
save_files(dictionary_file,dictionary)
save_files(set_file,set)
progress.status('Finished')
print(f'{counter_new} new entries\n{counter_update} entries updated')
