import os
from bluetooth import *
from wifi import Cell, Scheme
import subprocess
import time

#file to load the wifi settings
wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo "


def wifi_connect(ssid, psk):
    # write wifi config to file
    ssid = ssid.decode('utf-8')
    psk = psk.decode('utf-8')
    f = open('wifi.conf', 'w')
    f.write('country=GB\n')
    f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    f.write('update_config=1\n')
    f.write('\n')
    f.write('network={\n')
    f.write('       ssid="' + str(ssid) + '"\n')
    f.write('       psk="' + str(psk) + '"\n')
    f.write('}\n')
    f.close()

    cmd = 'mv wifi.conf ' + wpa_supplicant_conf
    cmd_result = ""
    cmd_result = os.system(cmd)
    print(cmd + " - " + str(cmd_result))
    # restart wifi adapter
    cmd = sudo_mode + 'sudo killall wpa_supplicant'
    cmd_result = os.system(cmd)
    print(cmd + " - " + str(cmd_result))
    time.sleep(3)
    cmd = sudo_mode + 'wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf'
    cmd_result = os.system(cmd)
    print(cmd + " - " + str(cmd_result))
    time.sleep(3)
    cmd = 'dhcpcd'
    cmd_result = os.system(cmd)
    print(cmd + " - " + str(cmd_result))
    time.sleep(10)






def ssid_discovered():
    Cells = list(Cell.all('wlan0'))  # Convert map object to list
    wifi_info = 'Found ssid : \n'

    for current in range(len(Cells)):
        wifi_info +=  Cells[current].ssid + "\n"

    wifi_info+="!"
    print(wifi_info)
    return wifi_info


def handle_client(client_sock) :
    # get ssid
    client_sock.send(ssid_discovered())
    print("Waiting for SSID...")

    #check = client_sock.recv(1024)
    #print(check)
    print("Configuring Wifi in progress")
    ssid = client_sock.recv(1024)

            
    print("ssid received")
    print(ssid)
    print(ssid.decode('utf-8'))
    # get psk
    client_sock.send("waiting-psk!")
    print("Waiting for PSK...")
    psk = client_sock.recv(1024)
    if psk == '' :
        return
            
        #ip_address =
    wifi_connect(ssid, psk)
        #print "ip address: " + ip_address
        #client_sock.send("ip-addres:" + ip_address + "!")

    return


if __name__=='__main__':
    try:
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        uuid = "815425a5-bfac-47bf-9321-c5ff980b5e11"
        advertise_service( server_sock, "RPi Wifi config",
                           service_id = uuid,
                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ])


        print("Waiting for connection on RFCOMM channel %d" % port)

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)

        handle_client(client_sock)

        client_sock.close()
        server_sock.close()

        # finished config
        print('Finished configuration\n')

    except (KeyboardInterrupt, SystemExit):
        print('\nExiting\n')
 
