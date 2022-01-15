#!/usr/bin/env python3

from typing import List
import config
import requests
import time
from threading import Timer
import os

class PassTime:
    def __init__(self, risetime, duration) -> None:
        super().__init__()
        self.risetime = risetime
        self.duration = duration

class ISSDetector:
    def __init__(self) -> None:
        super().__init__()
        self.passtimes = self.request_passtimes(config.location)
        self.bt_err_times = 0
        os.system('uhubctl -a off -l 1-1 > /dev/null')

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
            os.system('uhubctl -a on -l 1-1 > /dev/null')
            time.sleep(passtime.duration)
            os.system('uhubctl -a off -l 1-1 > /dev/null')
            self.schedule_next_pass()

        except KeyboardInterrupt:
            print('^C')
                
if __name__ == "__main__":
    issdetector = ISSDetector()
    issdetector.schedule_next_pass()
