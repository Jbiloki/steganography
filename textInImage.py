#!/bin/bash/python3

from PIL import Image
import numpy as np

def extractEleven(arr):
   lastEleven = arr[-11:]
   return lastEleven
   #for i in range(10,0,-1):
   #   print(lastEleven[i])

def ReadWriteEleven(arr, command):
   if command is 'r':
      givenNum = ""
      for i in range(10,-1,-1):
         givenNum += str(bin(arr[i][0])[-1]) + str(bin(arr[i][1])[-1]) + str(bin(arr[i][2])[-1])
      return givenNum[:-1]

def ReadMessage(arr, bits):
   bit_string = ""
   message = ""
   for i in range((len(arr)-11), (len(arr) - int(bits,2)), -1):
      bit_string += str(bin(arr[i][0])[-1]) + str(bin(arr[i][1])[-1]) + str(bin(arr[i][2])[-1])
   print(bit_string)
   for i in range(len(bit_string)):
      message += chr(int(bit_string[i-8:i],2))
   return message

if __name__ == '__main__':
   im = Image.open('testImage.png')
   #im = im.rotate(180)
   #im.show()
   im_array = list(im.getdata())
   length = len(im_array)
   eleven = extractEleven(im_array)
   bits = ReadWriteEleven(eleven, 'r')
   #print(bits)
   message = ReadMessage(im_array,bits) 
