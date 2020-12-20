#!/usr/bin/env python3

# MAC Address of LED Lamp
mac = "A1:B2:C3:D4:E5:F6"

# Location in degrees (-90 to 90, -180 to 180) to check ISS passing
location = {
    "lat": 19.5356,
    "lon": 115.6111,
    "alt": 280
}

# API url to get ISS passing data
apiurl = "http://api.open-notify.org/iss-pass.json"