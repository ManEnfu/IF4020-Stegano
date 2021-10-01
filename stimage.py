from PIL import Image
import sys
import random
import io
import os
import math
class BitMap:

  def __init__(self, coverPath: str = None):
    self.img: Image = None
    self.prevImg: Image = None
    self.path = coverPath
    self.status = ''
    if coverPath:
      self.readImage(coverPath)

  def readImage(self, path: str):
    img = Image.open(path)
    self.img = img

  def write(self, targetPath: str):
    if self.img:
      self.img.save(targetPath)
    else: print('no image found')

  def checksize(self, size: int):
    width, height = self.img.size
    return width * height >= size * 8
  
  def info(self):
    if not self.img == None:
      w, h = self.img.size
      print('width:', w)
      print('height:', h)
    else:
      print('No Image Loaded')

  def calculatePSNR(self) -> int:
    if self.prevImg == None:
      print('stegano image not found')
      return -1
    else:
      sqrDistance = 0
      width, height = self.img.size
      pixelsCover = list(self.prevImg.getdata())
      pixelsStego = list(self.img.getdata())
      for i in range(height):
        for j in range(width):
          evalCoverPixel = pixelsCover[i * width + j]
          evalStegoCover = pixelsStego[i * width + j]
          dist = evalCoverPixel[2] - evalStegoCover[2]
          sqrDist = dist**2
          sqrDistance += sqrDist
      rms = math.sqrt(sqrDistance/(width*height))
      psnr = 20 * math.log10(255/rms)
      return psnr

  def embed(self, msg: bytes, randplace: bool = False) -> bool:
    flag = b'\xff' if randplace else b'\x00'
    _msg = flag + len(msg).to_bytes(8, byteorder='big') + msg

    if (not self.checksize(len(_msg)) or self.img == None):
      self.status = 'errsize'
      return False
    
    newImg = self.img.copy()
    pixels = list(newImg.getdata())
    width, height = self.img.size

    if not randplace:
      for i in range(len(_msg)):
        for j in range(8):
          bit = (_msg[i] >> (7 - j)) & 1
          R, G, B, A = pixels[i * 8 + j]
          B = (B & 0xfe) | bit
          pixels[i * 8 + j] = (R, G, B, A)
    else:
      random.seed(4020)
      idx = [i for i in range(72)] + random.sample(range(72, len(pixels)), ((len(_msg) - 9) * 8))
      for i in range(len(_msg)):
        for j in range(8):
          id = i * 8 + j
          bit = (_msg[i] >> (7 - j)) & 1
          R, G, B, A = pixels[idx[id]]
          B = (B & 0xfe) | bit
          pixels[idx[id]] = (R, G, B, A)
    # write pixel
    for y in range(height):
      for x in range(width):
        newImg.putpixel((x, y), pixels[y * width + x])
    self.prevImg = self.img
    self.img = newImg
    return True

  def extract(self) ->  bytes:
    # extract flag
    if self.img == None:
      print('no image found')
      return b''
    width, height = self.img.size
    if (width * height < 72): return b''
    flag = 0x00
    dataLen = bytearray([0 for i in range(8)])
    pixels = list(self.img.getdata())
    
    # extract meta
    for i in range(9):
      for j in range(8):
        B = pixels[i * 8 + j][2]
        if i == 0:
          flag <<= 1
          flag |= (B & 1)
        else:
          dataLen[i - 1] <<= 1
          dataLen[i - 1] |= (B & 1)
    
    embeddedLen = int.from_bytes(bytes(dataLen), "big")
    embeddedData = bytearray([0 for i in range(embeddedLen)])
    if flag == 0:
      for i in range(embeddedLen):
        for j in range(8):
          B = pixels[(i + 9) * 8 + j][2]
          embeddedData[i] <<= 1
          embeddedData[i] |= (B & 1)
    elif flag == 255:
      random.seed(4020)
      idx = random.sample(range(72, len(pixels)), (embeddedLen * 8))
      for i in range(embeddedLen):
        for j in range(8):
          id = i * 8 + j
          B = pixels[idx[id]][2]
          embeddedData[i] <<= 1
          embeddedData[i] |= (B & 1)
    else: return b''
    return bytes(embeddedData)

def embedMessage(mediaPath: str, message: bytes, randomMode: bool) -> BitMap:
  bm = BitMap(mediaPath)
  bm.embed(message, randomMode)
  return bm


def extractMessage(mediaPath: str) -> bytes:
  bm = BitMap(mediaPath)
  return bm.extract()

# TEST CODE
# bitmp = BitMap(os.path.join('Hoki.png'))
# msg = b'\xff\xff\xff\x92'
# bitmp.embed(msg, True)
# print(bitmp.calculatePSNR())
# bitmp.write('test')
# print(bitmp.extract())
