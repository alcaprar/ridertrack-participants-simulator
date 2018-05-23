import random
import time

class User:

    def __init__(self, name, surname, email, password, _id=None, jwt_token=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.id = _id
        self.jwt_token = jwt_token
        self.last_checkpoint = 0
        self.distance_run = -75 + (70 * random.random())  # simulate the people waiting to start
        # speed in meter per second
        self.speed = (1.8 + 1.92 * random.random())  # random speed between 45mins/10km and 70mins/10km
        self.timestamp_last_position = time.time()

