# import II
from cv2 import cv2
import numpy as np
import math
import os

class MyFilters():

    __image = None
    __debug = False

    def __init__(self, debug=False):
        self.__debug = debug

    def __debagShow(self, name, image):
        if self.__debug:
            if image.shape[0] > 540 or image.shape[1] > 960:
                cv2.imshow(name, cv2.resize(image, (1600, 256)))
            else:
                cv2.imshow(name, image)    
            cv2.waitKey()

    def __masking(self, image, mask):
        mask[mask>0] = 1
        return cv2.bitwise_and(image, image, mask=mask)

    def __eraseBigAreas(self, mask):
        cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        max_area = 4000
        for c in cnts:
            area = cv2.contourArea(c)
            if area > max_area:
                cv2.drawContours(mask, [c], -1, (0,0,0), -1)
        return mask 

    def __eraseSmallAreas(self, mask):
        cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        max_area = 0
        max_area_c = cnts[0]
        for c in cnts:
            area = cv2.contourArea(c)
            if area > max_area:
                max_area_c = c
                max_area = area
        mask = np.zeros_like(mask)
        cv2.drawContours(mask, [max_area_c], -1, (255,255,255), -1)        
        return mask 

    def __contrast(self, coefficient):
        avg = self.__image.mean() + 100
        self.__image = avg + coefficient * (self.__image - avg)
        self.__image[self.__image>255] = 255
        self.__image[self.__image<0] = 0
        self.__image = self.__image.astype(np.uint8)
        self.__debagShow('contrast', self.__image)

    def __eraseNoise(self):
        _, mask = cv2.threshold(self.__image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        mask = cv2.medianBlur(mask, 3)
        mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_DILATE,(3,3)), iterations = 1)
        mask = self.__eraseBigAreas(mask)
        self.__image = self.__masking(self.__image, mask) # Big areas erased

        _, mask = cv2.threshold(self.__image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_DILATE,(7,7)), iterations = 3)

        self.__debagShow('erase noise', mask)

        # mask = self.__eraseSmallAreas(mask)
        # self.__image = self.__masking(self.__image, mask)

        # self.__debagShow('erase small areas', self.__image)

    def __getDistanse(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((x2-x1)**2 + (y2-y1)**2)**0.5

    def subimage(self, image, center, theta, width, height):
        shape = ( image.shape[1], image.shape[0] )

        matrix = cv2.getRotationMatrix2D( center=center, angle=theta, scale=1 )
        image = cv2.warpAffine( src=image, M=matrix, dsize=shape )

        x = int( center[0] - width/2  )
        y = int( center[1] - height/2 )

        image = image[ y:y+height, x:x+width ]

        return image

    def __getOnlyNumbers(self):
        new_image = cv2.dilate(self.__image, cv2.getStructuringElement(cv2.MORPH_OPEN,(21,13)), iterations = 1)
        contours = cv2.findContours(new_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        contour = contours[0]

        new_image = np.zeros_like(self.__image)
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        distanse = self.__getDistanse(box[0], box[1])
        right = box[0]
        for i in range(1,4):
            if box[i][0] > right[0]:
                right = box[i]
        left = box[0]
        for i in range(1,4):
            if box[i][0] < left[0]:
                left = box[i]
        top = box[0]
        for i in range(1,4):
            if box[i][1] < top[1]:
                top = box[i]
        bottom = box[0]
        for i in range(1,4):
            if box[i][1] > bottom[1]:
                bottom = box[i]          
        deg = math.asin((box[0][0]-box[1][0])/distanse) / math.pi * 180

        self.__image = self.subimage(
            self.__image, 
            ((right[0] - left[0])/2 + left[0], (bottom[1] - top[1])/2 + top[1]), 
            deg, 
            int(self.__getDistanse(box[1], box[2])), 
            int(self.__getDistanse(box[0], box[1]))
        ) 

        self.__debagShow('only numbers', self.__image)


    def __getimage(self, path):
        f = open(path, "rb")
        chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        return cv2.imdecode(chunk_arr, 0)

    def __getNumbersArray(self):
        path = os.path.dirname(os.path.realpath(__file__)) + "\\numbersDataSet\\images_of_0"
        os.chdir(path)
        number = self.__getimage(path+'\\'+os.listdir()[-1])
        y = self.__image.shape[0]
        yi, xi = number.shape[:2]
        dy = yi/y
        x = int(xi/dy)
        countnumbers = int(self.__image.shape[1]/x)
        blackspace = int((self.__image.shape[1] - countnumbers * x) / countnumbers) + 1
        images = [] 
        for xc in range(0, 
                        self.__image.shape[1],
                        x + blackspace):
            images.append(self.__image[:, xc:xc+x])
            self.__debagShow(str(xc+1), images[-1])
        return images

    def __recognitionValue(self):
        value = None
        self.__contrast(2)
        self.__eraseNoise()
        self.__getOnlyNumbers()
        numbers = self.__getNumbersArray()
        value = ''
        for number in numbers:
            value += II.recognize(cv2.resize(number, (100, 170)))
        return value

    def uploadImage(self, path):
        self.__image = None
        self.__image = self.__getimage(path)

        return False if self.__image is None else True    

    def runFilters(self):
        self.__contrast(2)
        self.__eraseNoise()
        return self.__image

    def showCurrentStateImage(self):
        if self.__image is not None:
            cv2.imshow('image', self.__image)
            cv2.waitKey(0)
            return True
        else:
            return False            

    def saveImage(self, name, image):
        cv2.imwrite(name, image)

    def getValueFromImage(self):
        if self.__image is not None:
            return self.__recognitionValue()
        else:
            return None                 