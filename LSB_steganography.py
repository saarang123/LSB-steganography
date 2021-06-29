#!/usr/bin/env python
# coding: utf-8

# In[10]:


from PIL import Image 
import cv2

def genData(data):
    newd=[]
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd
    

def modifypixels(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]
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
        
def encoder(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modifypixels(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
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

    newimg = image.copy()
    encoder(newimg, data)

    new_img_name = input("Enter the image name you want to save it as with extension format:")
    newimg.save((path+new_img_name), str(new_img_name.split(".")[1].upper()))
    
def decode():
    path="./"
    img = str(input("Enter the image name you want to decode, with extension format:"))
    image = Image.open((path+img), 'r')

    data = ''
    imgdata = iter(image.getdata())
    print ("The image to be decoded:")
    print ("\n")
    img1=cv2.imread((path + img))
    cv2.imshow("New img",img1)
    cv2.waitKey(0)
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

#_main_

a = int(input(":: Hii.Press 1 to encode an image with your own secret data. Press 2 to decode an image message from your computer, that you have received.::\n"
                        "1. Encode\n2. Decode\n"))
if (a == 1):
    encode()
elif (a == 2):
    print("The decoded secret message in the input is :  " + decode())
else:
    raise Exception("Enter correct input")

