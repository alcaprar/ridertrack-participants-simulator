import API.users
import API.events
import json
from Class.user import User


def main():
    # TODO change event_id
    event_id = '5b0534241165520004ae93de'

    # parse json to dict
    users = []
    with open('users.json', 'r') as fp:
        json_parsed = json.load(fp)

    # register users
    for index, user in enumerate(json_parsed):
        user_object = User(user['name'], user['surname'], user['email'], user['email'])

        result = API.users.register(user_object.name, user_object.surname, user_object.email, user_object.password)

        if result == (False, False):
            # if already registered, login and get the token
            result = API.users.login(user_object.email, user_object.password)

        print('User: ', user_object.email, ' registration/login token: ', result[1])
        user_object.id = result[0]
        user_object.jwt_token = result[1]

        users.append(user_object)

    # enroll in the event
    for user in users:
        print('User ', user.email, 'Enrolled: ', API.events.enroll(event_id, user))


if __name__ == "__main__":
    main()

