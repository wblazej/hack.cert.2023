import itertools
import binascii

CORRECT = "100001110100010011011010110111010111111100100011"
STATE = [int(x) for x in CORRECT[:21]]
FLAG = "12b4dd2f41ecb377c253596689877ae24a2e1c322bf17852bb452aa2fa2095ab8b7765e2a95099977b6ccd41b5c0979293"


def chunk(input_data, size):
    assert len(input_data) % size == 0, \
        "can't split data into chunks of equal size, try using chunk_with_remainder or pad data"
    return [input_data[i:i + size] for i in range(0, len(input_data), size)]


def long_to_bytes(data):
    if data == 0:
        return "\0"
    data = int(data)
    data = hex(data).rstrip('L').lstrip('0x')
    if len(data) % 2 == 1:
        data = '0' + data
    return bytes(bytearray(int(c, 16) for c in chunk(data, 2)))


class LFSR:
    def __init__(self, taps, seed):
        self.state = seed
        self.taps = taps

    def _new_bit(self):
        b = 0
        for t in self.taps:
            b = b ^ self.state[t]
        return b

    def next_bit(self):
        ret = self.state[0]
        self.state = self.state[1:] + [self._new_bit()]
        return ret


def calc_taps():
    for comb in list(itertools.combinations(range(20), 10)):
        taps = list(comb)
        lfsr = LFSR(taps, STATE)
        generated = ''.join([str(lfsr.next_bit()) for _ in range(48)])

        if generated == CORRECT:
            return taps

if __name__ == "__main__":
    taps = calc_taps()
    flag = binascii.unhexlify(FLAG)

    lfsr = LFSR(taps, STATE)

    [lfsr.next_bit() for _ in range(48)]

    bits = [lfsr.next_bit() for _ in range(len(flag) * 8)]
    keystream = long_to_bytes(int(''.join([str(b) for b in bits]), 2))

    decoded = bytes([c ^ k for c, k in zip(flag, keystream)]).decode()
    print(decoded)
