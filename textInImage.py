#!/bin/bash/python3
'''
    Name:
        Jacob Biloki
    CWID:
        891882573
    Filename:
        textInImage.py
    Description:
        This program demonstrates steganography in the form of
        hidden messages in the form of text hidden in a png image.
'''

from PIL import Image
import sys

def ReadBitsLength(arr):
   '''Reads the length of the message from the bottom right of the image,
   the first 32 bits

   args: The image in the form of an array of tupples
   '''
   givenNum = ""
   for i in range(11):
      givenNum += str(bin(arr[i][0])[-1]) + str(bin(arr[i][1])[-1]) + str(bin(arr[i][2])[-1]) #Convert the R G B values to binary, get the last bit and convert to string
   return givenNum[:-1]

def ReadMessage(arr):
   '''Read the message from an image

   args: The image in the form of an array of tupples
   '''
   bit_string = ""
   message = ""
   bits = ReadBitsLength(arr)
   bitsRead = 0
   bits = int(bits,2) #Convert bit string to interger version
   upper_bound = int(bits/3) + 1 #Convert the bits to the amount of tuples to read
   for i in range(11, upper_bound+11):
      if bitsRead + 3 <= bits: #If we need to read 3 more bits then do so, if not continue to check how many bits to read
         bit_string += str(bin(arr[i][0])[-1]) + str(bin(arr[i][1])[-1]) + str(bin(arr[i][2])[-1])
         bitsRead = bitsRead + 3
      elif bitsRead + 2 <= bits:
         bit_string += str(bin(arr[i][0])[-1]) + str(bin(arr[i][1])[-1])
         bitsRead = bitsRead + 2
      elif bitsRead + 1 <= bits:
         bit_string += str(bin(arr[i][0])[-1])
         bitsRead = bitsRead + 1
      else: #No more bits to read
         break
   for i in range(0,len(bit_string),8): #Convert bit string into the message
      message += chr(int(bit_string[i:i+8],2))
   return message

def WriteMessage(arr, msg):
   '''Write a message into an image

   args: The image in the form of an array of tupples, and the message to input
   '''
   message_length = str(bin(len(msg) * 8))[2:].zfill(32) #Find the length of the message in bits, 8 bits a character
   if len(message_length) <= 32: #Make sure the length of the message is not too long
      for i in range(11): #Loop through the first 11 pixels and input our length
         j = i * 3
         pixel = list(arr[i])
         pixel[0] = pixel[0] & ~1
         pixel[0] = pixel[0] | int(message_length[j])
         pixel[1] = pixel[1] & ~1
         pixel[1] = pixel[1] | int(message_length[j+1])
         if i < 10:
            pixel[2] = pixel[2] & ~1
            pixel[2] = pixel[2] | int(message_length[j+2])
         arr[i] = tuple(pixel)
   else:
      print("Message too big!")
   bits = int(ReadBitsLength(arr),2) #Get the amount of bits we need to write
   bitsWritten = 0
   upper_bound = int(bits/3) + 5 #How many tupples we need to go through to write
   bin_list = ""
   start = 0
   for ch in msg: #Convert our message into an 8 bit ascii representation
        binstr = ch.encode('ascii')
        bin_list += (format(ord(binstr), '08b'))
   for i in range(11, upper_bound+11): #Insert our ascii bits into the image after 11 length bits
      j = start * 3
      start = start + 1
      pixel = list(arr[i])
      if bitsWritten + 3 <= bits:
         pixel[0] = pixel[0] & ~1
         pixel[0] = pixel[0] | int(bin_list[j])
         pixel[1] = pixel[1] & ~1
         pixel[1] = pixel[1] | int(bin_list[j+1])
         pixel[2] = pixel[2] & ~1
         pixel[2] = pixel[2] | int(bin_list[j+2])
         arr[i] = tuple(pixel)
         bitsWritten = bitsWritten + 3
      elif bitsWritten + 2 <= bits:
         pixel[0] = pixel[0] & ~1
         pixel[0] = pixel[0] | int(bin_list[j])
         pixel[1] = pixel[1] & ~1
         pixel[1] = pixel[1] | int(bin_list[j+1])
         arr[i] = tuple(pixel)
         bitsWritten = bitsWritten + 2
      elif bitsWritten + 1 <= bits:
         pixel[0] = pixel[0] & ~1
         pixel[0] = pixel[0] | int(bin_list[j])
         arr[i] = tuple(pixel)
         bitsWritten = bitsWritten + 1
      else:
         break
         
         


if __name__ == '__main__':
   '''Begin of program get user input and read or write

   args: Command line argument 1 is the read or write command
   Command line argument 2 is the image to read or write
   If you are writing we have additional commands
   Command line argument  3 is -f if it is a file if not then it is the raw command line message
   Command line argument 4 is the file if the -f flag is passed
   '''
   if sys.argv[1].lower() == '-r':
      try:
         im = Image.open(sys.argv[2])
      except:
         print("The image argument is invalid")
      im_array = list(im.getdata())[::-1]
      length = len(im_array)
      print(ReadMessage(im_array))
   elif sys.argv[1].lower() == '-w':
      try:
         im = Image.open(sys.argv[2])
      except:
         print("The image argument is invalid")
      if sys.argv[3].lower() == '-f':
         with open(sys.argv[4], "r") as input_file:
            message = input_file.read()
      else:
         message = sys.argv[3]
      im_array = list(im.getdata())[::-1]
      WriteMessage(im_array, message)
      im_new = Image.new(im.mode, im.size)
      im_new.putdata(im_array[::-1])
      im_new.save("resultimage.png","PNG")
   else:
      print("Invalid argument count, try python <script> <-w> <image_file> <string_message> for console message and <script> <-w> <image_file> <-f> <file_name> to write a file")
