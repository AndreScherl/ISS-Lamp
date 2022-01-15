# ISS Detector
Control LED's (or something else) connected to Raspi's USB Ports to show you that the International Space Station in above you.

## Requirements
* [uhubctl](https://github.com/mvp/uhubctl) by [@mvp](https://github.com/mvp)
* [Open Notify API](http://open-notify.org/Open-Notify-API/ISS-Location-Now/) by [@natronics](https://github.com/natronics)

## Run script as system service
Create a file /etc/systemd/system/iss-lamp.service. Your paths to the python script could be different.
```
[Unit]
Description=Show the ISS visibility by using something connected to Raspi's USB ports.
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ISS-Lamp
Environment=PYTHONPATH=/home/pi/ISS-Lamp
ExecStart=/home/pi/ISS-Lamp/env/bin/python ISSDetector.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
Alias=iss-lamp.service
```    
Reload the deamon `$ sudo systemctl daemon-reload`    
Enable the serivce `$ sudo systemctl enable iss-lamp.service`    
Start the service `$ systemctl start iss-lamp.service` or `service iss-lamp start`    
Get the status of the service `systemctl status iss-lamp.service` or `service iss-lamp status`    
