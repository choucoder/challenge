import asyncio
from fileinput import filename
from multiprocessing import Process
from threading import Thread
import time

import requests
from aiohttp import ClientSession
from decouple import config

from workers import MainProcess


class Manager(Process):
    def __init__(self, filename):
        Process.__init__(self)
        self.filename = filename
        self._terminated = False

    def extract_coordinates(self, filename):
        with open(filename, 'r') as f:
            start = False
            lines = f.readlines()
            coordinates = []

            for line in lines:
                if 'lat,lon' in line:
                    start = True

                if start:
                    line = line[:-1].split(',')
                    if len(line) == 2:
                        try:
                            lat, lon = [float(x) for x in line]
                            coordinates.append((lat, lon))
                        except:
                            pass
            return coordinates

    def run(self):
        filename = self.filename
        print("filename for processing: ", filename)
        coordinates = self.extract_coordinates(filename)
        mainProcess = MainProcess(coordinates, batch_size=100)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(mainProcess.run())
