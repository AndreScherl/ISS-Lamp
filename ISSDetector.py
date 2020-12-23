#!/usr/bin/env python3

from typing import List
import config
import requests
import time
from threading import Timer
from govee_btled import BluetoothLED, ConnectionTimeout

class PassTime:
    def __init__(self, risetime, duration) -> None:
        super().__init__()
        self.risetime = risetime
        self.duration = duration

class ISSDetector:
    def __init__(self) -> None:
        super().__init__()
        self.passtimes = self.request_passtimes(config.location)
        try:
            lamp = BluetoothLED(config.mac)
            lamp.set_state(False)
        except ConnectionTimeout as err:
            print(err) 

    def request_passtimes(self, location) -> List[PassTime]:
        response = requests.get(config.apiurl, location).json()["response"]
        passtimes = []
        for item in response:
            passtimes.append(PassTime(item["risetime"], item["duration"]))
        return passtimes

    def schedule_next_pass(self) -> None:
        for passtime in self.passtimes:
            now = time.time()
            if passtime.risetime > now:
                timer_visible_start = Timer(passtime.risetime - now, self.notify, ["start"])
                timer_visible_start.start()
                timer_visible_end = Timer(passtime.risetime - now + passtime.duration, self.notify, ["end"])
                timer_visible_end.start()
                return
        self.passtimes = self.request_passtimes(config.location)
        self.schedule_next_pass()

    def notify(self, rise_event) -> None:
        try:
            lamp = BluetoothLED(config.mac)
			
            if rise_event == "start":
	            print("turn light on")
	            lamp.set_state(True)
	            lamp.set_color('blue')
	        
            if rise_event == "end":
	            print("turn light off")
	            lamp.set_state(False)
	            self.schedule_next_pass()
			
        except ConnectionTimeout as err:
            print(err) 
        except KeyboardInterrupt:
            print('^C')
                
if __name__ == "__main__":
    issdetector = ISSDetector()
    issdetector.schedule_next_pass()
