#!/usr/bin/env python
# coding: utf-8

# In[10]:


from PIL import Image 
import cv2

def convertToBinary(data):
    newdata = []
    for i in data:
        newdata.append(format(ord(i), '08b'))
    return newdata
    

def encodepixels(pix, data):
    datalist = convertToBinary(data)
    lendata = len(datalist)
    image_data = iter(pix)
    for i in range(lendata):
        pix = [value for value in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == "0" and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == "1" and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
        
def encode_image(new_image, data):
    w = new_image.size[0]
    (x, y) = (0, 0)
    for pixel in encodepixels(new_image.getdata(), data):
        new_image.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
            
def encode():
    path="./" #enter your path here
    img = input("Enter image name with extension format:")
    image = Image.open((path + img), 'r')

    data = input("Enter your secret message:")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    new_image = image.copy()
    encode_image(new_image, data)

    new_img_name = input("Enter the image name you want to save it as with extension format:")
    new_image.save((path + new_img_name), str(new_img_name.split(".")[1].upper()))
    
def decode():
    path="./"
    img = str(input("Enter the image name you want to decode, with extension format:"))
    image = Image.open((path + img), 'r')

    data = ''
    image_data = iter(image.getdata())
    print ("The image to be decoded:")
    print ("\n")
    image1 = cv2.imread((path + img))
    cv2.imshow("New img", image1)
    cv2.waitKey(0)
    while (True):
        pixels = [value for value in image_data.__next__()[:3] +
                                image_data.__next__()[:3] +
                                image_data.__next__()[:3]]

        binary_string = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binary_string += '0'
            else:
                binary_string += '1'

        data += chr(int(binary_string, 2))
        if (pixels[-1] % 2 != 0):
            return data

#_main_

"""
lsb_input.png is an image used for testing
lsb_output.png is a encoded image of lsb_input.png with the message "this is to test lsb steganography"
"""

a = int(input(":: Hii.Press 1 to encode an image with your own secret data. Press 2 to decode an image message from your computer, that you have received.::\n"
                        "1. Encode\n2. Decode\n"))
if (a == 1):
    encode()
elif (a == 2):
    print("The decoded secret message in the input is :  " + decode())
else:
    raise Exception("Enter correct input")

