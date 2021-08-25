#!/usr/bin/env python3

from typing import List
import config
import requests
import time
from threading import Timer
import RPi.GPIO as GPIO

class PassTime:
    def __init__(self, risetime, duration) -> None:
        super().__init__()
        self.risetime = risetime
        self.duration = duration

class ISSDetector:
    def __init__(self) -> None:
        super().__init__()
        self.passtimes = self.request_passtimes(config.location)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(config.led["red"], GPIO.OUT)
        GPIO.setup(config.led["blue"], GPIO.OUT)

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
        minutes = 0
        while minutes*60 <= passtime.duration:
            if minutes*60 <= passtime.duration/3 and minutes*60 >= 2*passtime.duration/3:
                GPIO.output(config.led["blue"], GPIO.HIGH)
            else:
                GPIO.output(config.led["red"], GPIO.HIGH)
            minutes += 1
            time.sleep(60)
        GPIO.output(config.led["red"], GPIO.LOW)
        GPIO.output(config.led["blue"], GPIO.LOW)

if __name__ == "__main__":
    issdetector = ISSDetector()
    issdetector.schedule_next_pass()
