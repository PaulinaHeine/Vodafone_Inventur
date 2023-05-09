from PIL import Image
import pytesseract
# from tesseract import image_to_string
import numpy as np
import re
from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.1/bin/tesseract'

filename = '/Users/paulinaheine/IMG_3163.png'

img1 = np.array(Image.open(filename))

#img1.save("/Users/paulinaheine/IMG_3163.png", dpi=(600, 600))

text = pytesseract.image_to_string(img1, config='--psm 4')

print(text)

from PIL import Image
import pytesseract
import cv2
import numpy as np

img_height = 180
img_width = 180

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.1/bin/tesseract'

img = cv2.imread('/Users/paulinaheine/s-l1600.jpg')


# IMAGE IMPROVEMENT
# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# apply image thresholding
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_thresh = cv2.adaptiveThreshold(img,
          255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
# invert the image, 255 is the maximum value
img_thresh = 255 - img_thresh
# display image
#plt.imshow(img_thresh)
#plt.show()


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)



#img = cv2.imread('/Users/paulinaheine/s-l1600.jpg')
#img=opening(img)
img = cv2.imread('/Users/paulinaheine/IMG_3120.png')
img = canny(img)
#plt.imshow(img)


'''
gray = get_grayscale(img)
noise = remove_noise(img)
erode = erode(img)
# thresh = thresholding(gray)
opening = opening(img)
canny = canny(gray)

osd = pytesseract.image_to_osd('/Users/paulinaheine/s-l1600.jpg', config='--psm 0 -c min_characters_to_try=5')
angle = re.search('(?<=Rotate: )\d+', osd)
script = re.search('(?<=Script: )\d+', osd)
print("angle: ", angle)
print("script: ", script)
'''
#my_conf = r'--oem 3 --psm 6 outputbase digits'
#my_conf = r'--oem 3 --psm 6'
#my_conf = r'--psm 4'
my_conf = r"--psm 11 --oem 3"

#trasnfering the text
res_list = pytesseract.image_to_string(img, config=my_conf)
#Text snippests as a list
res_list_2 = list2 = res_list.split("\n")
res_list_2  = list(filter(lambda el: len(el) > 2, res_list_2 ))
'Remove empty stuff'
while '' in res_list_2:
    res_list_2.remove('')
print(res_list_2)
'Print list'
for i in range(len(res_list_2)):
    print(res_list_2[i])


###Für mehrere Einstellungen:

configs = [r'--oem 3 --psm 6 outputbase digits', r'--oem 3 --psm 6',r'--psm 4', r"--psm 11 --oem 3"
]
res = []
for con in configs:

    # Alle sinnvollen Einstellungen werden durchprobiert
    res_list = pytesseract.image_to_string(img, config=con)
    # Alle Einträge werden in einzelne snippets unterteilt
    res_list_2 = res_list.split("\n")
    # Alle leeren Einträge werden entfernt
    while '' in res_list_2:
        res_list_2.remove('')
    # Alle Einträge mit weniger als 3 Einträgen werden entferht
    res_list_2 = list(filter(lambda el: len(el) > 3, res_list_2))
    res.append(res_list_2)


'''
#Small example for Data

data = {"SUNFIREV60X": "bliblablub", "SUNFIREV65X":"rerarug" }


#Regex Function for comparing data

import regex


txt = data
x = re.findall("SUNFIREV60X", "VVVVVGHGUZGZSUNFIREV60XHJJJ")
print(x)

'''