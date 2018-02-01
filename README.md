# IDP_Feedbacklamp
This project is build upon Python with mainly Flask.<br><br>
<b>Dependencies</b>
<ul>
<li>Flask</li>
<li>PyAudio</li>
<li>Numpy</li>
<li>audioop</li>
<li>BeautifulSoup</li>
<li>MySql</li>
<li>hashlib</li>
</ul>
<br>This project assumes that you have 2 Raspberry Pis. One running the server(site) and one being the client(microphone).
<br>It also assumes that on your server you have your GPIOs setup(BOARD) with<br>
GPIO 7 being the red LED<br>
GPIO 11 the yellow LED<br> 
GPIO 22 the green LED<br><br>
How you run the application:<br>
1. Setup a wifi network on your client with the following settings in /etc/network/interfaces<br><br>
auto wlan0<br>
iface wlan0 inet static<br>
address 192.168.1.1<br>
netmask 255.255.255.0<br>
wireless-channel 1<br>
wireless-essid Pi<br>
wireless-mode ad-hoc<br><br>
2. On your server connect to this network with the following setting in again /etc/network/interfaces<br><br>
auto wlan0<br>
iface wlan0 inet static<br>
address 192.168.1.4<br>
netmask 255.255.255.0<br>
wireless-channel 1<br>
wireless-essid Pi<br>
wireless-mode ad-hoc<br><br>
The device you want to connect to the server can have any IP you choose<br>
<b>Attention, this doesn't setup a WPA2 secured connection! It is an open network so anyone can connect to the network and assign an IP</b><br><br>
3. Reboot both your pi's(first client then server)<br>
4. Run main.py on the client first, than run main.py on the server.<br><br>

NOTE: PyAudio will give a lot of errors when you try to run it with a microphone plugged in. Try editing your /usr/share/alsa/alsa.conf and comment the lines which are in error codes.<br>
<a href='https://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time' >This</a> post helped me a lot
