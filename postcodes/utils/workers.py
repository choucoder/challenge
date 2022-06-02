import asyncio
import time
from typing import List
import traceback
from threading import Thread
from multiprocessing import Process

from aiohttp import ClientSession
import psutil

from decouple import config


class WorkerThread(Thread):

    def __init__(self, parent, batches_queue: List):
        Thread.__init__(self)
        self.parent = parent
        self.batches_queue = batches_queue
        self._terminated = False
        self.n = 0

    @property
    def terminated(self):
        return self._terminated

    async def iter_all_coordinates(self):
        while True:
            try:
                coordinates = self.batches_queue.pop(0)
                for coordinate in coordinates:
                    self.n += 1
                    yield coordinate
            except:
                return

    async def fetch(self, session, semaphore, coordinate):
        lat, lon = coordinate
        url = f'https://api.postcodes.io/postcodes?lon={lon}&lat={lat}'

        async with semaphore:
            async with session.get(url) as response:
                data = await response.json()
                try:
                    postcode = data['result'][0]['postcode']
                except:
                    postcode = None
                if postcode:
                    data = {
                        'lat': lat,
                        'lon': lon,
                        'code': postcode
                    }
                    await session.post(f'http://{config("host")}:8000/api/postcodes', json=data)
                return postcode

    async def executor(self):
        semaphore = asyncio.Semaphore(250)
        tasks = []

        async with ClientSession() as session:
            async for coordinate in self.iter_all_coordinates():
                task = asyncio.create_task(
                    self.fetch(session, semaphore, coordinate)
                )
                tasks.append(task)

            return await asyncio.gather(*tasks)

    def run(self):
        print("[INFO] Starting WorkerThread for process data")
        s = time.time()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.executor())
        elapsed = time.time() - s
        print(f"[INFO] Finished WorkerThred in {elapsed} seg with: {self.n}")


class WorkerProcess(Process):

    def __init__(self, parent, batches_queue: List):
        Process.__init__(self)
        self.parent = parent
        self.batches_queue = batches_queue

        self.workers = {}
        self._terminated = False

    @property
    def terminated(self):
        return self._terminated

    def run(self):
        print("[INFO] Worker process started")
        threads_n = psutil.cpu_count()
        batches_n = int(len(self.batches_queue) / threads_n)

        for i in range(threads_n):
            if i == (threads_n - 1):
                thread = WorkerThread(
                    self, self.batches_queue[i*batches_n:]
                )
            else:
                thread = WorkerThread(
                    self, self.batches_queue[i*batches_n:(i+1)*batches_n])
            thread.daemon = True
            thread.start()
            self.workers[i] = thread

        while True:
            threadsAlive = 0

            for i in self.workers.keys():
                if self.workers[i].is_alive():
                    threadsAlive += 1

            if not threadsAlive:
                break

            time.sleep(1.5)

        self._terminated = True


class MainProcess:
    def __init__(self, coordinates, batch_size=100):
        self.coordinates = coordinates
        self.batch_size = batch_size
        self.batches_queue = asyncio.Queue(maxsize=2000000)
        self.batches = []
        self.workers = {}

    async def batching(self):
        batches_amount = int(len(self.coordinates) / self.batch_size)

        for i in range(batches_amount):
            self.batches.append(
                self.coordinates[i *
                                 self.batch_size: min((i+1)*self.batch_size, len(self.coordinates))]
            )
            await self.batches_queue.put(self.batches[i])

        print(f"Batches amount: {len(self.batches)}")
        print(f"Batch amount: {len(self.batches[0])}")

    async def run(self):
        await self.batching()
        workers_n = 1
        batches_n = int(len(self.batches) / workers_n)

        for i in range(workers_n):

            if i == (workers_n - 1):
                worker = WorkerProcess(self, self.batches[i*batches_n:])
            else:
                worker = WorkerProcess(
                    self, self.batches[i*batches_n: (i+1)*batches_n])
            worker.start()
            self.workers[i] = worker

        while True:
            workersAlive = 0

            for i in self.workers.keys():
                if not self.workers[i].is_alive():
                    workersAlive += 1

            if not workersAlive:
                break

            time.sleep(.5)
