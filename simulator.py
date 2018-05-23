import API.users
import API.events
from Class.route import Route
from Class.user import User
import time
import json
import random

wait_for_input = True
users_limit = 150
event_id = '5b0534241165520004ae93de'


def coordinates_noise():
    return -0.0001 + 0.0002 * random.random()


def main():

    # parse json to dict
    print('[User parsing][start]')
    users = []
    with open('users.json', 'r') as fp:
        json_parsed = json.load(fp)
    print('[User parsing][finished]')

    # login users
    print('[User login][start]')
    for index, user_json in enumerate(json_parsed):
        user_object = User(user_json['name'], user_json['surname'], user_json['email'], user_json['email'])
        result = API.users.login(user_object.email, user_object.password)

        if result == (False, False):
            raise Exception('Error while login')

        print('[User login] User: ', user_object.email, ' Token: ', result[1])
        user_object.id = result[0]
        user_object.jwt_token = result[1]

        users.append(user_object)
        print('[User login] users left: ', users_limit - index)
        if index == users_limit:
            break
    print('[User login][finished]')

    # recover route info
    print('[Route recovery][start]')
    event_route = Route(event_id)
    print('[Route recovery][finished]')

    if wait_for_input:
        input("Users logged in. Press Enter to start the simulator...")

    # send user position
    all_finished = False

    print('[Simulator][start]')
    while not all_finished:
        print('[New iteration]')
        all_finished = True

        for index, user in enumerate(users):
            # send the position for each user
            print(user.last_checkpoint, ' ----- ', len(event_route.coordinates))
            if user.last_checkpoint < (len(event_route.coordinates) - 1):

                all_finished = False

                last_checkpoint = event_route.coordinates[user.last_checkpoint]
                next_checkpoint = event_route.coordinates[user.last_checkpoint + 1]

                checkpoints_distance = event_route.calculate_distance_between_checkpoints(user.last_checkpoint)

                while user.distance_run > checkpoints_distance:
                    user.distance_run -= checkpoints_distance

                    user.last_checkpoint += 1

                    last_checkpoint = event_route.coordinates[user.last_checkpoint]
                    next_checkpoint = event_route.coordinates[user.last_checkpoint + 1]

                    checkpoints_distance = event_route.calculate_distance_between_checkpoints(user.last_checkpoint)


                print('[Simulator] User: ', user.email)
                print('------ LastCheck: ', user.last_checkpoint)
                print('------ DistRun: ', user.distance_run)
                print('------ CheckDist: ', checkpoints_distance)

                # calculate the position using the checkpoint and the distance run
                single_unit_in_distance = checkpoints_distance / 100
                percentage_run = user.distance_run / single_unit_in_distance / 100

                print('------ SingleUniDist: ', single_unit_in_distance)
                print('------ PercentRun: ', percentage_run)

                new_x = last_checkpoint[0] + percentage_run * (next_checkpoint[0] - last_checkpoint[0]) + coordinates_noise()
                new_y = last_checkpoint[1] + percentage_run * (next_checkpoint[1] - last_checkpoint[1]) + coordinates_noise()

                print('------ NewX: ', new_x)
                print('------ NewY: ', new_y)

                # send the position
                API.users.send_position(
                    event_id,
                    user,
                    new_x,
                    new_y
                )

                # update the distance run using the speed
                now = time.time()
                time_difference = int(now - user.timestamp_last_position)
                user.timestamp_last_position = now
                user.distance_run += time_difference * user.speed  # the speed is m/s
                print('------ UserSpeed: ', user.speed)
                print('------ TimeDiff: ', time_difference)
                print('------ NewDistRun: ', user.distance_run)

            else:
                print('[Simulator] User ', user.email, ' has finished.')

            if index == users_limit:
                break


if __name__ == "__main__":
    main()

