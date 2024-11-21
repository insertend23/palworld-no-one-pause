import time


def wait_timer(message: str):
    wait_message = f"Waiting for the {message}" "... {time} seconds left"

    for sec in range(30, 10, -10):
        print(wait_message.format(time=sec))
        time.sleep(10)

    print(wait_message.format(time=10))
    time.sleep(5)

    for sec in range(5, 0, -1):
        print(wait_message.format(time=sec))
        time.sleep(1)
