import asyncio
from multiprocessing import Process

import requests
from aiohttp import ClientSession
from decouple import config


class PostcodeAPI(Process):

    def __init__(self, filename, chunks=35):
        self.filename = filename
        self.chunks = chunks

    async def fetch(self, locations, session):
        for i, location in enumerate(locations):
            lat, lon = location
            url = f'https://api.postcodes.io/postcodes?lon={lon}&lat={lat}'

            async with session.get(url) as response:
                response = await response.json()
                try:
                    postcode = response['result'][0]['postcode']
                    data = {
                        'lat': lat,
                        'lon': lon,
                        'code': postcode,
                    }
                    response = requests.post(
                        f'http://{config("host")}:8000/api/postcodes', json=data)
                    print(f"Saved ({lat}, {lon}): {postcode}")
                except:
                    pass

    async def run(self, locations):
        tasks = []
        batch = []
        chunks = self.chunks
        size = int(len(locations) / chunks)

        if size > 0:
            for i in range(chunks):
                batch.append(
                    locations[i * size: min((i + 1) * size, len(locations) - 1)])
        else:
            batch.append(locations)

        async with ClientSession() as session:
            for chunk in batch:
                task = asyncio.ensure_future(
                    self.fetch(chunk, session))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            print("DONE!")

    def start(self):
        print(f"[INFO] Start processing the file {self.filename}")

        with open(self.filename, 'r') as f:
            start = False
            lines = f.readlines()
            locations = []

            for line in lines:
                if 'lat,lon' in line:
                    start = True

                if start:
                    line = line[:-1].split(',')
                    if len(line) == 2:
                        try:
                            lat, lon = [float(x) for x in line]
                            locations.append((lat, lon))
                        except:
                            pass

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(locations))
        loop.run_until_complete(future)

        print(f"[INFO] Finished for {self.filename}")
