import wave
import sys
import util
import random
import math

class Wav:

    def __init__(self, path: str = None):
        self.data: bytearray = bytearray(b'')
        self.params: tuple = ()
        self.psnr = 0
        if path:
            self.read(path)

    def read(self, path: str):
        wf = wave.open(path, 'rb')
        self.params = wf.getparams() 
        self.data = bytearray(wf.readframes(self.params[3]))
        wf.close()

    def write(self, path: str):
        wf = wave.open(path, 'wb')
        wf.setparams(self.params)
        wf.writeframes(self.data)
        wf.close()

    def info(self):
        nchannels = self.params[0]
        sampwidth = self.params[1]
        framerate = self.params[2]
        nframes = self.params[3]
        print('nchannels: ', nchannels)
        print('sampwidth: ', sampwidth)
        print('framerate: ', framerate)
        print('nframes  : ', nframes)
        print('framesize: ', nchannels * sampwidth)
        print('bytesize : ', nframes * nchannels * sampwidth)
        print(len(self.data))


    def checksize(self, size: int) -> bool:
        sampwidth = self.params[1]
        return len(self.data) >= size * 8 * sampwidth

    def embed(self, msg: bytes, randplace: bool = False) -> bool:
        rms = 0
        sampwidth = self.params[1]
        magic = b'\xff' if randplace else b'\x00' 
        _msg = magic + len(msg).to_bytes(8, byteorder='big') + msg
        if not self.checksize(len(_msg)):
            return False
        if not randplace:
            for i in range(len(_msg)):
                for j in range(8):
                    k = (i * 8 + j) * sampwidth
                    bit = (_msg[i] >> (7 - j)) & 1
                    cb = self.data[k]
                    ocb = cb
                    cb = (cb & 0xfe) | bit
                    self.data[k] = cb
                    rms += (ocb - cb) ** 2
        else:
            random.seed(0)
            idx = [0] + random.sample(range(1, len(self.data) // sampwidth), len(_msg) * 8 - 1)
            for i in range(len(_msg)):
                for j in range(8):
                    k = (i * 8 + j)
                    bit = (_msg[i] >> (7 - j)) & 1
                    cb = self.data[idx[k] * sampwidth]
                    ocb = cb
                    cb = (cb & 0xfe) | bit
                    self.data[idx[k] * sampwidth] = cb
                    rms += (ocb - cb) ** 2
        rms = math.sqrt(rms / (len(self.data) // sampwidth)) 
        self.psnr = 20 * math.log10((256 ** sampwidth - 1)/rms)
        return True

    
    def extract(self) -> bytes:
        sampwidth = self.params[1]
        di = 0
        mlen = 0
        cb = self.data[0]
        bit = cb & 1
        if bit == 0:
            # sequential
            for i in range(8):
                if self.data[di * sampwidth] & 1 == 1:
                    print('0 err')
                    return b''
                di += 1
            for i in range(64):
                cb = self.data[di * sampwidth]
                bit = cb & 1
                mlen = (mlen << 1) | bit
                di += 1
            data = bytearray([0 for i in range(mlen)])
            for i in range(mlen):
                mb = 0
                for j in range(8):
                    cb = self.data[di * sampwidth]
                    bit = cb & 1
                    mb = (mb << 1) | bit
                    di += 1
                data[i] = mb
            return bytes(data)
        else:
            # random
            random.seed(0)
            idx = [0] + random.sample(range(1, len(self.data) // sampwidth), 71)
            for i in range(8):
                if self.data[idx[di] * sampwidth] & 1 == 0:
                    print('1 err')
                    return b''
                di += 1
            for i in range(64):
                cb = self.data[idx[di] * sampwidth]
                bit = cb & 1
                mlen = (mlen << 1) | bit
                di += 1
            random.seed(0)
            idx = [0] + random.sample(range(1, len(self.data) //sampwidth), 71 + mlen * 8)
            data = bytearray([0 for i in range(mlen)])
            for i in range(mlen):
                mb = 0
                for j in range(8):
                    cb = self.data[idx[di] * sampwidth]
                    bit = cb & 1
                    mb = (mb << 1) | bit
                    di += 1
                data[i] = mb
            return bytes(data)
        

if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit(-1)
    wav = Wav(sys.argv[1])
    wav.info()
    print(wav.data[0:18])
    if sys.argv[2] == 'i':
        if len(sys.argv) < 5:
            exit(-1)
        msg = util.read_file_binary(sys.argv[3])
        wav.embed(msg)
        print('psnr:', wav.psnr)
        wav.write(sys.argv[4])
    elif sys.argv[2] == 'ir':
        if len(sys.argv) < 5:
            exit(-1)
        msg = util.read_file_binary(sys.argv[3])
        wav.embed(msg, randplace=True)
        print('psnr:', wav.psnr)
        wav.write(sys.argv[4])
    elif sys.argv[2] == 'x':
        if len(sys.argv) < 4:
            exit(-1)
        msg2 = wav.extract()
        util.write_file_binary(sys.argv[3], msg2)
    else:
        exit(-1)
