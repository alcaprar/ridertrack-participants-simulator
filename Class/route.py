import API.events
import math


class Route:

    def __init__(self, event_id):
        self.event_id = event_id

        result = API.events.get_route(self.event_id)
        if result == (False, False):
            raise Exception('Error while getting the route. The event might not exist.')
        self.coordinates = result

    def get_starting_point(self):
        return self.coordinates[0]

    def get_last_point(self):
        return self.coordinates[len(self.coordinates) - 1]

    def calculate_distance_between_checkpoints(self, checkpoint):
        # calculate the distance in meters
        R = 6371000  # radius of Earth in meters
        lat1, lng1 = self.coordinates[checkpoint]
        lat2, lng2 = self.coordinates[checkpoint + 1]
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lng2 - lng1)

        a = math.sin(delta_phi / 2.0) ** 2 + \
            math.cos(phi_1) * math.cos(phi_2) * \
            math.sin(delta_lambda / 2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
