# steganography

**Jacob Biloki**
## Architecture
This is a project to demonstrate the use of steganograhy in the form of embeded text in images. In this script I write each bit of the message into the least significant bit of each RGB value in order to change the color intensite they least amount. The resulting image is written to a result.png file.

This program contains supporting functions to Read/Write the message into the image array given.
As well as a function to read the first 11 bits to get the length of the message.

ReadMessage:
This funciton reads the message from the image by iterating through the pixels after the 11th pixel and reading the last bit of each RGB value

WriteMessage:
This function begins by writing the length of the resulting mesage into the image's first 11 bits and writing the message through he remaining bits.

## Execution
> This program is written in python 3.6.0 and should be executed from a terminal using:
Read:
  python <script> <-w> <image_file> <string_message> for console message and <script> <-w> <image_file> <-f> <file_name> to write a file"
Write:
  python <script> <-r> <image_file>
  Writing will create a new file called 'result.png' which is your new image with the message embedded.
