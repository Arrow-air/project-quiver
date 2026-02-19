---
title: Setup Note Quiver Ethernet
tags: dev-kit, PT3
---

# Setup Note Quiver Ethernet
Quiver Dev-Kit
Heavy-Lift Multipurpose UAV (<25 kg MTOW)

Table of content
[toc]

## 1. System Configuration
This document outlines the setup for the DroneCAN Ethernet Adapter (CubeNode ETH), the Flight Controller, and the Raspberry Pi.

### 1.1 Network Topology
:::info
This configuration is for testing. Some IP addresses might change in the final configuration.
:::

Drone Subnet: 192.168.144.x
Gateway (RPI): 192.168.144.20
CubeNode ETH Adapter: 192.168.144.10
Flight Controller: 192.168.144.11

### 1.2 Helpful Links
CubePilot CubeNode ETH configuration: https://ardupilot.org/copter/docs/common-cubepilot-cubenodeeth.html
Ardupilot Network: https://ardupilot.org/copter/docs/common-network.html#common-network

## 2. Ethernet switch installation

Installation of two GigaBlox Nano Ethernet switches. This is the basic requirement for using Ethernet on the drone.

### 2.1 Required materials
    - 2x GigaBlox Nano – 1 Inch GigaBit Ethernet Switch
    - 4x M2x6 stainless steel or plastic screw
    
### 2.2 Installation

1. Plug each Ethernet switch into the designated connector on the main PCB. 
![ethernet](https://hackmd.io/_uploads/SkH0eREH-l.jpg)

2. Screw the Ethernet switches in place using 2 M2x6 screws each.  

:::warning
Note: Only the dev-kit PCBs already have the spacers soldered on. Older PCBs must be screwed on with a separate spacer and extra nut. To test the setup, the screw connection can also be omitted, as the Ethernet switches sit very securely on the connector.
:::

## 3. CubeNode ETH installation
This will assign an IP address to the flight controller using the cube node eth adapter. The parameter settings of ardupilot can then be used to make a lot more data available in the network.

### 3.1 Required materials
    - 1x CubePilot CubeNode ETH
    - 1x 6 Pin UART connection cable (included in CubeNode ETH package)
    - 1x 5 Pin Ethernet connection cable (included in CubeNode ETH package)
    - 1x 4 Pin CAN connection cable (included in CubeNode ETH package)
    
### 3.2 Installation

#### Ardupilot with PPP Support
The CubeNode ETH adapter requires an ardupilot version with enabled PPP support. PPP allows an autopilot to communicate over Ethernet using a serial port.
:::warning
PPP is not included by default in the ArduPilot firmware. I have not build a firmware yet that includes PPP and the custom S2L integration.
:::

Use the custom firmware build server to build a firmware that includes PPP support: https://custom.ardupilot.org/

![image](https://hackmd.io/_uploads/rkI5tA4SZx.png)

#### Physical connection of the CubeNode ETH adapter
    For dev-kit PCB:
    - Connect all three cables to the CubeNode ETH
    - Connect the 6 Pin UART cable to J41 on the main PCB
    - Connect the 5 Pin Ethernet cable to J36 on the main PCB
    - Connect the 4 Pin CAN cable to J35 on the main PCB

For older versions of the main PCB it's just a little bit different:

    For the older version of the main PCB:
    - Modify the 6 Pin UART cable so that RX and TX are crossed
    - Modify the 4 Pin CAN cable so that CANL and CANH are crossed
    - Connect all three cables to the CubeNode ETH
    - Connect the 6 Pin UART cable to J41 on the main PCB
    - Connect the 5 Pin Ethernet cable to J36 on the main PCB
    - Connect the 4 Pin CAN cable to J35 on the main PCB
    
:::warning
The physical mounting of the CubeNode ETH adapter does not yet exist. Please secure it in a safe manner and ensure that it cannot cause any short circuits. The PCB of the CubeNode ETH adapter has exposed pins and pads.
:::

#### Ardupilot parameters
The CubeNode ETH adapter is connected to CAN1 (***CAN2 on the older PCB!***) and Serial 2 (UART5).

Ardupilot parameters for dev-kit:
    
    CAN_P1_DRIVER = 1 (First driver)
    CAN_P1_BITRATE = 1M
    CAN_D1_PROTOCOL = 1 (DroneCAN)
    NET_ENABLE = 1
    NET_P1_PORT = 5760
    NET_P1_PROTOCOL = 1
    SERIAL2_PROTOCOL = 48 (PPP)
    SERIAL2_BAUD = 12500000 (12.5MBaud)

Ardupilot parameters for old Main_PCB:
    
    CAN_P2_DRIVER = 2 (Second driver)
    CAN_P2_BITRATE = 1M
    CAN_D2_PROTOCOL = 1 (DroneCAN)
    NET_ENABLE = 1
    NET_P1_PORT = 5760
    NET_P1_PROTOCOL = 1
    SERIAL2_PROTOCOL = 48 (PPP)
    SERIAL2_BAUD = 12500000 (12.5MBaud)

:::info
Regarding the older PCB: Our default bitrate for CAN2 is 500 kbit. For the first setup the CubeNode ETH adapter is expecting 1 Mbit. You can later change the default bitrate of the CubeNode ETH adapter to 500 kbit via the DroneCAN/UAVCAN screen.
:::

With these parameters the CubeNode ETH adapter should appear on the CAN bus. Its accessible over the DroneCAN/UAVCAN screen.

#### CubeNode ETH parameters

We will now set the CubeNode ETH parameters. In the DroneCAN/UAVCAN screen connect to MAVLinkCAN1 or MAVLinkCAN2, depending on the CAN connection of the CubeNode ETH adapter.

Press the “Menu” button on the right side and select “Parameters”

![image](https://hackmd.io/_uploads/HJpoGNLSWx.png)

Set the following parameters and press the “Write” button
    
    NET_DHCP = 0
    NET_ENABLE = 1
    
    NET_GWADDR0 = 192
    NET_GWADDR1 = 168
    NET_GWADDR2 = 144
    NET_GWADDR3 = 1
    
    NET_IPADDR0 = 192
    NET_IPADDR1 = 168
    NET_IPADDR2 = 144
    NET_IPADDR3 = 10
    
    NET_NETMASK = 20
    NET_OPTIONS = 1
    
    NET_P1_TYPE = 0
    
With this configuration the CubeNode ETH adapter will have the static IP: 192.168.144.10. The FC will automatically receive the IP 192.168.144.11 from the adapter.

:::info
Here you can also change the CAN bitrate of the CubeNode ETH adapter. Adjust "CAN_BAUDRATE" to 500000 if you want to also use the Nanoradar devices on CAN2. Do not forget to change "CAN_P2_BITRATE" also to 500000 again after you saved CubeNode ETH parameters.
:::

## 4. Check connection

While connected over USB to the FC you can check if the FC receives the correct IP. During startup of the FC it will print the IP config in the "Messages" tab.

It should look like this:
NET: Gateway 192.168.144.10
NET: Mask 255.255.255.255
NET: IP 192.168.144.11

![Startup_FC_with_ETH](https://hackmd.io/_uploads/SJX0JSUrZx.png)

## 5. RPI Setup

### 5.1 Image preparation

Please use the Raspberry PI Imager to create the OS for the RPI: https://www.raspberrypi.com/software/
![image](https://hackmd.io/_uploads/rJdZfSLBbx.png)

It offers some features that will make a headless setup really easy.

1. Open Raspberry PI Imager
2. Choose you RPI
3. Select Raspberry Pi OS (other)
4. Select Raspberry Pi OS Lite (64-bit)
5. Choose your SD card
6. Choose your hostname (for example "quiver")
7. Choose your timezone and keyboard layout
8. Choose your user with password
9. Insert your WIFI credentials (its important you do this so you don't have to connect a monitor to the PI)
10. Activate SSH, select use password
11. In the next screen you can choose if you want to use RPI connect. I disabled it.
12. Double check your selected properties
13. Write the Image to the SD card
14. Insert the SD card into the RPI

### 5.2 Physical installation

- Place the RPI onto the 40 pin connector on the Main_PCB.
- You need a ethernet cable that you can cut off at one end. One side should be RJ-45 connector, the other side will be a 4-pin phoenix contact connector (fitting into J2).

:::info
The SIYI camera/HM30 comes with a RJ45 cable that only has 4 wires inside. I used that one.
:::

- We only need two wire pairs of the ethernet cable.
    - Transmit + and - (often white-green and green wire)
    - Receive + and - (often white-orange and orange wire)

![image](https://hackmd.io/_uploads/ryRV_BIS-e.png)

- After you prepared the cable store it and **do not connect it at this time**

![RPI_cable](https://hackmd.io/_uploads/B1JIxI8H-g.jpg)

:::warning
DO NOT CONNECT THE CABLE YET
:::

### 5.3 RPI configuration

- Power on the drone and wait for the RPI to boot (no eth cable attached!)
- Connect to the RPI over SSH and WIFI (lookup the RPI IP in your router)

Updates first:

    sudo apt update
    sudo apt full-upgrade
    sudo apt autoremove
    sudo apt clean

#### Setting a Static IP on eth0 (via NetworkManager)

We use NetworkManager (nmcli) to configure the Ethernet port. It is crucial to set a static IP so the Flight Controller and other attachments can always find this device.

Create a new connection for the ethernet port:
    
    sudo nmcli con add type ethernet con-name "Drone-Net" ifname eth0
    
Give a static ip to Drone-Net (eth0):

    sudo nmcli con modify "Drone-Net" ipv4.addresses 192.168.144.20/24
    
Turn off DHCP on Drone-Net:

    sudo nmcli con modify "Drone-Net" ipv4.method manual
    
We do not set a gateway for this connection. That will result in only traffic for 192.168.144.X will go over this connection. Everything else will go over WIFI or 4G/5G.

Start the connection:

    sudo nmcli con up "Drone-Net"
    
**You can now plug in the ethernet wire between RPI and main PCB.**

#### Check eth0 connection

    ip a show eth0

It should show: inet 192.168.144.20/24 ...

Do a ping test to the CubeNode ETH adapter:

    ping 192.168.144.10
    
Do a ping test to the FC:

    ping 192.168.144.11
    
:::info
We will stop here with the ethernet configuration. If you want to connect to the FC over WIFI, there are several options. I choose to use tailscale to include my computer into the "Drone-Net" network. Then you can just use the TCP connect option in mission planner with 192.168.144.11 and port 5760.
:::

## 6. Tattu battery protocol bridge setup

Install python and venv on the RPI:

    sudo apt install python3-pip python3-venv -y

Create the project folder:

    mkdir -p ~/tattu_can_bridge
    
Create the virtual environment (venv) in your home directory:

    python3 -m venv ~/venv
    
Activate venv and install can libraries

    source ~/venv/bin/activate
    pip install python-can dronecan
    deactivate

Over SFTP place the tattu_bridge.py script into the project folder (home/USER/tattu_can_bridge/tattu_bridge.py)

Discord link to file: https://discord.com/channels/853833144037277726/914195759216336947/1443547529374597121

Create service to automatically start can interface on startup:

    sudo nano /etc/systemd/system/can-setup.service
    
Write into that file:

    [Unit]
    Description=Setup CAN Interface
    After=sys-subsystem-net-devices-can0.device
    Requires=sys-subsystem-net-devices-can0.device
    
    [Service]
    Type=oneshot
    RemainAfterExit=yes
    ExecStart=/sbin/ip link set can0 type can bitrate 1000000
    ExecStart=/sbin/ip link set can0 txqueuelen 1000
    ExecStart=/sbin/ip link set can0 up
    ExecStop=/sbin/ip link set can0 down
    
    [Install]
    WantedBy=multi-user.target

Activate the service:

    sudo systemctl daemon-reload
    sudo systemctl enable can-setup
    
Create service to automatically start the tattu bridge on startup:

    sudo nano /etc/systemd/system/tattu-bridge.service
    
Write into that file (**please adjust the USER**):
    
    Description=Tattu Battery to DroneCAN Bridge
    # Wait for network and can
    After=network.target can-setup.service
    Requires=can-setup.service
    
    [Service]
    Type=simple
    User=USER
    WorkingDirectory=/home/USER/tattu_can_bridge
    
    # Start: Uses Python from venv, runs project script
    ExecStart=/home/USER/venv/bin/python /home/USER/tattu_can_bridge/tattu_bridge.py
    
    # Restart
    Restart=always
    RestartSec=5
    
    # Logging
    StandardOutput=journal
    StandardError=journal
    Environment=PYTHONUNBUFFERED=1
    
    [Install]
    WantedBy=multi-user.target
    
Activate the service:

    sudo systemctl daemon-reload
    sudo systemctl enable tattu-bridge
    sudo systemctl start tattu-bridge
    
Check status:

    systemctl status tattu-bridge
    
Check logs:

    journalctl -u tattu-bridge -f
    
Check can bus status (Bitrate & Errors):
    
    ip -details link show can0
    
:::success
The can bridge should be working now. Please select DroneCAN-BatteryInfo (Value 8) for the BATT_MONITOR parameter in ardupilot to test it. For testing please also deactivate all other BATT_MONITOR parameters like BATT_MONITOR1, BATT_MONITOR2 etc...
:::