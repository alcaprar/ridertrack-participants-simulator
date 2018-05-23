from API import config
import requests


def register(name, surname, email, password):
    r = requests.post(config.basic_url + '/auth/register', json={
        "name": name,
        "surname": surname,
        "email": email,
        "password": password
    })

    if r.status_code == 200:
        # user successfully registered
        return r.json()['userId'], r.json()['jwtToken']
    else:
        # user already registered
        return False, False


def login(email, password):
    r = requests.post(config.basic_url + '/auth/login', json={
        "email": email,
        "password": password
    })

    if r.status_code == 200:
        # user successfully registered
        return r.json()['userId'], r.json()['jwtToken']
    else:
        # user already registered
        return False, False

def send_position(event_id, user, lat, lng):
    r = requests.post(config.basic_url + '/events/' + event_id + '/participants/positions', json={
        "lat": lat,
        "lng": lng
    }, headers={
        'Authorization': 'JWT ' + user.jwt_token
    })

    # print('[API][users][send_position] User: ', user.email, ' Result: ', r.status_code, r.text)
    if r.status_code == 200:
        # positions successfully sent
        return True
    else:
        # error while sending position
        return False