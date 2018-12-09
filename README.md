SMS gateway api
===============
A little api in python for the ZTE  K4203-Z.

My UMTS stick is branded by Vodafone. If plugged in on a Linux bases system I could not get it up and running via the serial interface, so I had to come up with other options. This specific stick was detected as ethernet interface and with some reverse engineering I found the following.

the reverse engineering
-----------------------
Let's do some naive information gathering via *lsusb*:

```
> lsusb
Bus 001 Device 004: ID 19d2:1048 ZTE WCDMA Technologies MSM
```

Especially the vendor and product ID were something I could not find anywhere. Something was up with this specific model.

The stick is configurated as a ethernet interface with it's own DHCP server. Always in the ip range of 192.169.009.XXX
```
> ifconfig
usb0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.9.136  netmask 255.255.255.0  broadcast 192.168.9.255
        inet6 fe80::c:e7ff:fe0b:102  prefixlen 64  scopeid 0x20<link>
        ether 02:0c:e7:0b:01:02  txqueuelen 1000  (Ethernet)
        RX packets 3228797  bytes 432237232 (432.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 542430  bytes 75647757 (75.6 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Connecting onto the IP I was greeted with a webinterface. After some digging this (incomplete) code was the result. Messages can be sent but nothing else, since my specific configuration does not receive messages at all.

the usage
---------

Using the code is pretty straight forward. Just install *python* and the module *requests*.
There are many different flavors of systems. For Ubuntu or debian you do this via:

```
sudo apt-get install python3
sudo apt-get install python3-requests
```

Now you are good to go. The IP may change. 

additional info
---------------
* I would be happy if somebody could find out how to delete messages from the stick itself.
* This script is by far not complete but I wanted to make it public anyway, as learning exercise. If somebody could find out how to delete messages, please do and message me. I started a function but it does not work.
* The encoding of the sent messages is gsm-7 but for whatever reason the stick wants a strange padded encoding of utf-8. Have a look into the function *encodeISO88591Hex*.
* This is a reverse engineerd project, some strange things could happen!
* Further info for *_get_sms_from* can be found in the JS-scripts used by the webinterface. The function is called *GetSMSMessages*
