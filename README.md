# wifi-deauth
## [ES] Pasos:
Script para desautenticar a todas las direcciones MAC en una red a la que estas conectado.

*Script unicamente probado en una red con pocos dispositivos.

1- Para escanear todas las direcciones MAC en una red: sudo python3 macfinder.py

2- Para desautenticar las direcciones MAC: sudo python3 deauth.py -f mac_dictionary.txt -i wlan1 -b "BSSID MAC" -c 6 -l True


## [EN] Steps:
Script to deauth every MAC address in a network you are connected to.

*Script only tested within a network with few devices.

1- To scan every MAC address in a network: sudo python3 macfinder.py

2- To deauth those MAC addresses: sudo python3 deauth.py -f mac_dictionary.txt -i wlan1 -b "BSSID MAC" -c 6 -l True

![image](https://github.com/user-attachments/assets/685d03d0-dc2e-4ef7-a5a4-5b1d58b782cb)

![image](https://github.com/user-attachments/assets/d46fe0a3-4447-4ecd-8bb2-111f03b2c5b1)

