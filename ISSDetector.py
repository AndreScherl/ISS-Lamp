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
                timer_visible_start = Timer(passtime.risetime - now, self.notify, [passtime])
                timer_visible_start.start()
                return
        self.passtimes = self.request_passtimes(config.location)
        self.schedule_next_pass()

    def notify(self, passtime) -> None:
        try:
            lamp = BluetoothLED(config.mac)
            lamp.set_state(True)
            lamp.set_color("purple")
            brightness = 0
            lamp.set_brightness(brightness)
            seconds = 0
            
            while seconds <= passtime.duration:
                if seconds <= passtime.duration/2:
                    brightness += 0.0031
                else:
                    brightness -= 0.0031
                lamp.set_brightness(min(1, brightness))
                seconds += 1
                time.sleep(1)
            
            lamp.set_state(False)
            self.schedule_next_pass()
			
        except ConnectionTimeout as err:
            print(err) 
        except KeyboardInterrupt:
            print('^C')
                
if __name__ == "__main__":
    issdetector = ISSDetector()
    issdetector.schedule_next_pass()
