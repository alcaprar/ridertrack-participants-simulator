import API.users
import API.events
from Class.route import Route
from Class.user import User
import time
import json
import random
import _thread
import threading
import queue

users = []
json_parsed = []

wait_for_input = True
users_limit = 150
event_id = '5b0534241165520004ae93de'

queueLock = threading.Lock()
loginQueue = queue.Queue(200)
loginsFinished = False

login_threads_number = 15


def coordinates_noise():
    return -0.0001 + 0.0002 * random.random()


def create_queue_and_initialize():
    queueLock.acquire()
    for i in range(0, users_limit - 1):
        loginQueue.put(i)
    queueLock.release()
    pass


def create_login_threads():
    for i in range(0, login_threads_number):
        _thread.start_new_thread(login, ())


def login():
    while not loginsFinished:
        queueLock.acquire()
        if not loginQueue.empty():
            user_index = loginQueue.get()
            queueLock.release()

            user_json = json_parsed[user_index]

            user_object = User(user_json['name'], user_json['surname'], user_json['email'], user_json['email'])
            result = API.users.login(user_object.email, user_object.password)

            if result == (False, False):
                raise Exception('Error while login')

            print('[User login] User: ', user_object.email, ' Token: ', result[1])
            user_object.id = result[0]
            user_object.jwt_token = result[1]

            users.append(user_object)
            print('[User login] users left: ', users_limit - user_index)
        else:
            queueLock.release()
            break


def send_positions(event_route, user):
    finished = False
    while not finished:
        print(user.last_checkpoint, ' ----- ', len(event_route.coordinates))
        if user.last_checkpoint < (len(event_route.coordinates) - 1):

            finished = False

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

            new_x = last_checkpoint[0] + percentage_run * (
                        next_checkpoint[0] - last_checkpoint[0]) + coordinates_noise()
            new_y = last_checkpoint[1] + percentage_run * (
                        next_checkpoint[1] - last_checkpoint[1]) + coordinates_noise()

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

            time.sleep(5 * random.random())
        else:
            print('[Simulator] User ', user.email, ' has finished.')
            finished = True


def main():

    # parse json to dict
    print('[User parsing][start]')
    global json_parsed
    with open('users.json', 'r') as fp:
        json_parsed = json.load(fp)
    print('[User parsing][finished]')

    create_queue_and_initialize()

    create_login_threads()

    # Wait for queue to empty
    while not loginQueue.empty():
        pass

    # Notify threads it's time to exit
    loginsFinished = True

    # recover route info
    print('[Route recovery][start]')
    event_route = Route(event_id)
    print('[Route recovery][finished]')

    time.sleep(3)

    if wait_for_input:
        input("Users logged in. Press Enter to start the simulator...")

    for user in users:
        # start a new thread for each user
        print('Starting thread for ', user.email)
        _thread.start_new_thread(send_positions, (event_route, user))
    print('[SIMULATOR] threads started')

    while 1:
        pass

if __name__ == "__main__":
    main()

