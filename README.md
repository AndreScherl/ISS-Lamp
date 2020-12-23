# ISS Detector
Control a bluetooth LED bulb to show you that the International Space Station in above you.

## Requirements
* [Govee Bluetooth LED Package](https://github.com/chvolkmann/govee_btled) by [@cvolkmann](https://github.com/chvolkmann). You have to install it with `pip install -U git+https://github.com/Freemanium/govee_btled`.
* [Open Notify API](http://open-notify.org/Open-Notify-API/ISS-Location-Now/) by [@natronics](https://github.com/natronics)
* The right bulb, e.g. [this one from Amazon Germany](https://www.amazon.de/Govee-farbwechsel-mehrfarbige-Leuchtmittel-Dekoration/dp/B07CPP5LCP).

## Run script as system service
Create a file /etc/systemd/system/iss-lamp.service. Your paths to the python script could be different.
```
[Unit]
Description=Show the ISS visibility by using a bluetooth lamp.
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
