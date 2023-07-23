import socket
from time import sleep
from threading import Thread
from time import time

HOST = "mind-blank.ecsc23.hack.cert.pl"
PORT = 5001


def bits_to_str(bits: list) -> str:
    return ''.join([str(x) for x in bits])


def extract_time(time: str):
    return time[:time.index('can')].replace('>', '').strip()


class Storage:
    def __init__(self, q: int) -> None:
        self.q = q

    @staticmethod
    def add_bit(bit: int):
        open('bits', 'a').write(str(bit))

    @staticmethod
    def get_bits():
        return [int(x) for x in open('bits', 'r').read().strip()]

    @staticmethod
    def reset():
        open('bits', 'w').write('')
        open('queue', 'w').write('0')
        open('time_check', 'w').write('')

    @staticmethod
    def set_time_check(time: str):
        time = extract_time(time)
        open('time_check', 'w').write(time)

    @staticmethod
    def check_time(time: str):
        time = extract_time(time)
        time_check = open('time_check', 'r').read()
        return time_check == time

    def go_next(self):
        open('queue', 'w').write(str(self.q + 1))

    def check_queue(self):
        q = int(open('queue', 'r').read())
        return q == self.q


def thread(q: int):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        # read time the connection was established
        t = client_socket.recv(1024).decode("utf-8")

        storage = Storage(q)

        if q == 0:
            # if thread is the first one, reset the storage
            # and set the time check for the others
            storage.reset()
            storage.set_time_check(t)
        else:
            # check if the thread connection was established 
            # in the same second as the first one then wait for its turn
            if not storage.check_time(t):
                raise Exception('time check failed, run script again')
            while not storage.check_queue():
                sleep(0.1)

        bits = storage.get_bits()

        # once we got 48 bits, shut down the thread
        if len(bits) >= 48:
            storage.go_next()
            return

        print(bits_to_str(bits))

        i = 0

        while True:
            if i >= len(bits):
                # guess the next bit as 1, if it's correct add it to the storage
                # else append 0 and go to the next thread as this one was
                # closed by the server because of wrong guess
                client_socket.sendall('1\n'.encode("utf-8"))
                data = client_socket.recv(1024).decode("utf-8")

                if 'Correct!' in data:
                    storage.add_bit(1)
                    bits.append(1)

                    if len(data) > 20:
                        # if received data is long, it's probably the flag so
                        # print it out and shut down the thread
                        print(f'flag:', data.strip().replace('Correct!\n', ''))
                        print(f'bits:', bits_to_str(bits))
                        storage.go_next()
                        return
                elif 'Nope!' in data:
                    storage.add_bit(0)
                    storage.go_next()
                    break
            else:
                # this is for new threads, it has to send the known bits 
                # first in order to be able to guess the next ones
                client_socket.sendall(f'{bits[i]}\n'.encode("utf-8"))
                data = client_socket.recv(1024).decode("utf-8")

            i += 1

    except Exception as e:
        print(f"Error: {e}")
        storage.go_next()
    finally:
        client_socket.close()


if __name__ == "__main__":
    # start the threads at thevery beginning of the second
    # to make it all run in the same second in order to
    # get the same seed on the server
    t = time()
    sleep(t-int(t))

    for i in range(30):
        t = Thread(target=thread, args=(i,))
        t.start()
        sleep(0.01)
