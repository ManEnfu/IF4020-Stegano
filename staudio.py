import wave
import sys
import util

class Wav:

    def __init__(self, path: str = None):
        self.data: bytearray = bytearray(b'')
        self.params: tuple = ()
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
        return len(self.data) >= size * 8

    def embed(self, msg: bytes, randplace: bool = False) -> bool:
        _msg = len(msg).to_bytes(8, byteorder='big') + msg
        if not self.checksize(len(_msg)):
            return False
        if not randplace:
            for i in range(len(_msg)):
                for j in range(8):
                    bit = (_msg[i] >> (7 - j)) & 1
                    cb = self.data[i * 8 + j]
                    # print(cb, bit)
                    cb = (cb & 0xfe) | bit
                    # print('>', cb)
                    self.data[i * 8 + j] = cb
        return True

    
    def extract(self) -> bytes:
        di = 0
        mlen = 0
        for i in range(64):
            cb = self.data[di]
            bit = cb & 1
            # print('#', bit)
            mlen = (mlen << 1) | bit
            di += 1
        # print(mlen)
        data = bytearray([0 for i in range(mlen)])
        for i in range(mlen):
            mb = 0
            for j in range(8):
                cb = self.data[di]
                bit = cb & 1
                mb = (mb << 1) | bit
                di += 1
            data[i] = mb
        return bytes(data)
        

if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit(-1)
    wav = Wav(sys.argv[1])
    if sys.argv[2] == 'i':
        if len(sys.argv) < 5:
            exit(-1)
        msg = util.read_file_binary(sys.argv[3])
        wav.embed(msg)
        wav.write(sys.argv[4])
    elif sys.argv[2] == 'x':
        if len(sys.argv) < 4:
            exit(-1)
        msg2 = wav.extract()
        util.write_file_binary(sys.argv[3], msg2)
    else:
        exit(-1)
