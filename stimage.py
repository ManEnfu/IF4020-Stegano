from PIL import Image
import sys
import random
import io
import os

class BitMap:

  def __init__(self, coverPath: str = None):
    self.data: bytearray = bytearray(b'')
    self.img: Image = None
    if coverPath:
      self.readImage(coverPath)

  def readImage(self, path: str):
    img = Image.open(path)
    self.img = img
    buffer = io.BytesIO()
    img.save(buffer, 'bmp')
    self.data = bytearray(buffer.getvalue())

  def writeImage(self, path: str):
    img = Image.open(io.BytesIO(bytes(self.data)))
    img.save(path)

  def checksize(self, size: int):
    return len(self.data) >= size * 8
  
  def info(self):
    if self.img:
      w, h = self.img.size
      print('size:', len(self.data), 'Byte')
      print('width:', w)
      print('height:', h)
    else:
      print('No Image Loaded')
  
  def embed(self, msg: bytes, randplace: bool = False) -> bool:
    flag = b'\xff' if randplace else b'\x00'
    _msg = flag + len(msg).to_bytes(8, byteorder='big') + msg
    if not self.checksize(len(_msg)):
      return False
    if not randplace:
      for i in range (len(_msg)):
        for j in range(8):
          bit = (_msg[i] >> (7 - j)) & 1
          self.data[i * 24 + j * 3] = (self.data[i * 24 + j * 3] & 0xfe) | bit
    else:
      random.seed(4020)
      idx = [i for i in range(72)] + random.sample(range(72, len(self.data)//3), ((len(_msg) - 9) * 8))
      for i in range(len(_msg)):
        for j in range(8):
          bit = (_msg[i] >> (7 - j)) & 1
          evalIndex: int = idx[i * 8 + j] * 3
          self.data[evalIndex] = (self.data[evalIndex] & 0xfe) | bit
    return True
  
  def extract(self) -> bytes:
    # extract flag
    if (len(self.data) < 72): return b'' # didn't have any metadata
    flag = 0x00
    dataLen = bytearray([0 for i in range(8)])

    # extract meta data
    for i in range(9):
      for j in range(8):
        if (i == 0):
          flag <<= 1
          flag |= self.data[i * 24 + j * 3] & 1
        else:
          dataLen[i - 1] <<= 1
          dataLen[i - 1] |= (self.data[i * 24 + j * 3] & 1)
    
    embeddedLen = int.from_bytes(bytes(dataLen), "big")
    embeddedData = bytearray([0 for i in range(embeddedLen)])
    if flag == 0x00:
      for i in range(embeddedLen):
        for j in range(8):
          bit = self.data[(i+9)*24 + j*3] & 1
          embeddedData[i] = (embeddedData[i] << 1) | bit
    elif flag == 0xff:
      random.seed(4020)
      idx = random.sample(range(72, len(self.data)//3), (embeddedLen * 8))
      for i in range(embeddedLen):
        for j in range(8):
          bit = self.data[idx[i*8+j]*3] & 1
          embeddedData[i] = (embeddedData[i] << 1) | bit
    else:
      return b''

    return bytes(embeddedData)





    



bitmp = BitMap(os.path.join('Hoki2.bmp'))
bitmp.info()
msg = b'\xff\xff\xff\x92'
bitmp.embed(msg)
# bitmp.writeImage('asd.bmp')
print(bitmp.extract())
# print(bitmp.data[:72])
