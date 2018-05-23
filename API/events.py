from API import config
import requests


def enroll(event_id, user):
    r = requests.post(config.basic_url + '/enrollments', json={
        "eventId": event_id
    }, headers={
        'Authorization': 'JWT ' + user.jwt_token
    })

    if r.status_code == 200:
        return True
    else:
        # enrollment failed
        return False

def get_route(event_id):
    r = requests.get(config.basic_url + '/events/' + event_id + '/route')

    if r.status_code == 200:
        # route exists
        c = []
        try:
            c = r.json()['coordinates']
        except Exception:
            raise Exception('Route not defined')

        coordinates = []
        for coordinate in c:
            coordinates.append((coordinate['lat'], coordinate['lng']))
        return coordinates
    else:
        # route does not exist
        return False, False
