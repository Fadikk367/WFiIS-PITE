import concurrent.futures
import logging
import threading
import time
import random
import math

from abc import ABC, abstractproperty


def setup_logger(logger):
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('file.log')

    format = logging.Formatter(   
        fmt='{asctime} - {message}',
        datefmt='%d-%m-%y %H:%M:%S',
        style='{'
    )

    console_handler.setFormatter(format)
    file_handler.setFormatter(format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


class Interval:
    def __init__(self, dt, action):
        self.dt = dt
        self.action = action
        self.cancel_interval = threading.Event()


    def set_interval(self):
        next_time = time.time() + self.dt
        while not self.cancel_interval.wait(next_time - time.time()):
            next_time += self.dt
            self.action()

    def start(self):
        thread = threading.Thread(target=self.set_interval)
        thread.start()

    def stop(self):
        self.cancel_interval.set()



class Event(ABC):

    def __init__(self, type):
        self.type = type

    @abstractproperty
    def value(self):
        pass


class Correction(Event):
    def __init__(self, value):
        super().__init__('correction')
        self.correction = value

    @property
    def value(self):
        return self.correction


class Turbulence(Event):
    def __init__(self, rate):
        super().__init__('turbulence')
        self.rate = rate

    @property
    def value(self):
        return random.gauss(0, 2*self.rate)


class Plane:

    def __init__(self, name: str, logger, initial_tilt=10):
        self.name = name
        self.logger = logger
        self.tilt = initial_tilt

    def handle_event(self, event: Event):
        value = event.value

        if event.type == 'turbulence':
            self.apply_turbulence(value)
        elif event.type == 'correction':
            self.apply_correction(value)

    def apply_correction(self, value):
        self.tilt += value
        self.logger.info(f'action: CORRECTION - value: {value}')

    def apply_turbulence(self, value):
        self.tilt += value
        #self.logger.info(f'action: TURBULENCE - value: {value}')
    
    @property
    def info(self):
        if self.tilt < -360:
            self.tilt += 360
        elif self.tilt > 360:
            self.tilt -= 360

        return f'name: {self.name} - tilt: {round(self.tilt, 4)}'


class PlaneSimulation:

    messages = ['simulation initializing ... ', 'turbulence generator started', 'logging procedure started']
    messages = {
        'welc': 'Available actions: \n  > a - correct tilt to the left (-5) \n  > d - correct tilt to the right (+5) \n  > q - quit simulation',
        'init': 'simulation initializing ... ',
        'turb': 'turbulence generator started',
        'log': 'logging procedure started'
    }

    def __init__(self, plane, logger, correction_rate=5, noise_interval=1, log_interval=1):
        self.plane = plane
        self.logger = logger
        self.noise_interval = Interval(noise_interval, self._generate_turbulence)
        self.log_interval = Interval(log_interval, self._log_state)
        self.correction_rate = correction_rate

        self.is_running = False


    def _generate_turbulence(self):
        turbulence = Turbulence(self.correction_rate)
        self.plane.handle_event(turbulence)

    def _log_state(self):
        self.logger.info(self.plane.info)       

    def start(self, interactive=False):
        yield PlaneSimulation.messages['welc']
        yield PlaneSimulation.messages['init']
        self.is_running = True
        self.noise_interval.start()
        yield PlaneSimulation.messages['turb']
        self.log_interval.start()
        yield PlaneSimulation.messages['log']
        while True:
            action = input()
            if action == 'a':
                correction = Correction(-self.correction_rate)
                self.plane.handle_event(correction)
            elif action == 'd':
                correction = Correction(self.correction_rate)
                self.plane.handle_event(correction)
            elif action == 'q':
                self.stop()
                break
            time.sleep(0.1)

    def stop(self):
        self.is_running = False
        self.noise_interval.stop()
        self.log_interval.stop()
        print('==== Simulation stopped ====')


def is_prime(n):
    sqrt_n = int(math.sqrt(n))
    for i in range(3, sqrt_n + 1):
        if n % i == 0:
            return False
    return True



if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    setup_logger(logger)

    jerry = Plane('Jerry the plane', logger, 10)
    simulation = PlaneSimulation(jerry, logger, 5, 1, 1)

    procedures = simulation.start()

    for msg in procedures:
        print(msg)
        time.sleep(0.7)

    # in general we use multiprocessing for calculations that require high cpu usage
    print('\n\nmultiprocessing power in a nutshell (checking if number is prime, 81 numbers 12 digits each):')
    time.sleep(3)

    primes = [
        889898989901,	889898989907,	889898989909,		
        889898989951,	889898989999,	889898990009,	
        889898990027,	889898990047,	889898990131,
        889898990173,	889898990213,	889898990273,	
        889898990329,	889898990339,	889898990341,		
        889898990359,	889898990381,	889898990423,
        889898990543,	889898990551,	889898990567,	
        889898990569,	889898990587,	889898990707,		
        889898990723,	889898990779,	889898990801,
        889898990821,	889898990857,	889898990873,	
        889898990881,	889898990899,	889898990927,		
        889898990969,	889898990977,	889898990983,
        889898991061,	889898991067,	889898991127,	
        889898991151,	889898991169,	889898991181,
        889898991251,	889898991257,	889898991269,
        889898991281,	889898991283,	889898991307,	
        889898991329,	889898991343,	889898991407,	
        889898991521,	889898991529,	889898991547,
        889898991581,	889898991601,	889898991607,	
        889898991623,	889898991671,	889898991677,
        889898991743,	889898991763,	889898991767,
        889898991829,	889898991833,	889898991851,	
        889898991869,	889898991911,	889898991967,	
        889898992019,	889898992043,	889898992057,
        889898992063,	889898992067,	889898992139,	
        889898992183,	889898992189,	889898992267,
        889898992313,	889898992337,	889898992357
    ]

    start = time.perf_counter()


    with concurrent.futures.ProcessPoolExecutor() as executor:

        results = [executor.submit(is_prime, prime) for prime in primes]

        for f in concurrent.futures.as_completed(results):
            f.result()


    finish = time.perf_counter()

    print(f'multiprocessing: {finish - start}s')

    start = time.perf_counter()

    for prime in primes:
        is_prime(prime)

    finish = time.perf_counter()

    print(f'normal: {finish - start}s')


    


