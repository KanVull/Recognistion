import cv2
import random
import numpy as np
import os

'''
0---1
|  /|
| / |
|/  |
5---2
|  /|
| / |
|/  |
4---3

0 is lines (0 to 1) (1 to 2) (2 to 3), (3 to 4), (4 to 5), (5 to 0) 

Possible lines (0,1) (0,5) (1,2) (1,5) (2,3) (2,4) (2,5) (3,4) (4,5)
'''
numbers = { 
    0: ((0,1), (1,2), (2,3), (3,4), (4,5), (5,0)),
    1: ((5,1), (1,2), (2,3)), 
    2: ((0,1), (1,2), (2,4), (3,4)),
    3: ((0,1), (1,5), (2,5), (2,4)),
    4: ((0,5), (2,5), (1,2), (2,3)),
    5: ((0,1), (0,5), (2,5), (2,3), (3,4)),
    6: ((1,5), (4,5), (3,4), (2,3), (2,5)),
    7: ((0,1), (1,5), (4,5)),
    8: ((0,1), (0,5), (1,2), (2,3), (2,5), (3,4), (4,5)),
    9: ((0,1), (0,5), (1,2), (2,4), (2,5)),
}

def newImageOf(number, sizeWH):
    width, height = sizeWH

    def getDot():
        def getDotMatrix():
            size = random.randint(2,3)
            dot = np.zeros(shape=(size, size))
            return dot

        matrix = getDotMatrix()
        x = random.randrange(1,len(matrix))
        y = random.randrange(len(matrix))
        matrix[y][x] = 1

        def fillDotMatrix(x,y):
            def is_neighbourOne():
                if x != 0:
                    if matrix[y][x-1] == 1:
                        return True
                if x != len(matrix) - 1:
                    if matrix[y][x+1] == 1:
                        return True
                if y != 0:
                    if matrix[y-1][x] == 1:
                        return True
                if y != len(matrix) - 1:
                    if matrix[y+1][x] == 1:
                        return True
                return False        

            def zero_Neighbours():
                left = right = up = down = False
                if x != 0:
                    if matrix[y][x-1] == 0:
                        left = True
                if x != len(matrix) - 1:
                    if matrix[y][x+1] == 0:
                        right = True
                if y != 0:
                    if matrix[y-1][x] == 0:
                        up = True
                if y != len(matrix) - 1:
                    if matrix[y+1][x] == 0:
                        down = True
                return (up,right,down,left)

            if matrix[y][x] == 0:
                if is_neighbourOne():
                    matrix[y][x] = 1 if random.random() >= 0.2 else 2
                else:
                    matrix[y][x] = 2 
                up, right, down, left = zero_Neighbours()
                if up:
                    fillDotMatrix(x, y-1)
                if right:
                    fillDotMatrix(x+1, y)
                if down:
                    fillDotMatrix(x, y+1)
                if left:
                    fillDotMatrix(x-1, y)

            return matrix             


        matrix = fillDotMatrix(x-1,y)

        return np.where(matrix==2, 0, matrix)  

    deviation = random.randint(3,4)

    image = np.zeros((height,width), dtype='uint8')
    def convertToX_Y(point):
        if point == 0:
            return deviation, deviation
        if point == 1:
            return width - deviation, deviation
        if point == 2:
            return width-deviation, height // 2 
        if point == 3:
            return width-deviation, height-deviation
        if point == 4:
            return deviation, height-deviation
        if point == 5:
            return deviation, height // 2            

    for line in numbers[number]:
        point1 = convertToX_Y(line[0])
        point2 = convertToX_Y(line[1])
        if line == (2,4) or line == (1,5):
            X = np.linspace(point1[0], point2[0], random.randint(9,14))
        else:
            X = np.linspace(point1[0], point2[0], random.randint(7,12))
        Y = np.linspace(point1[1], point2[1], len(X))        
        for i in range(len(X)):
            if random.random() > 0.6:
                X[i] += random.randint(-1,1)
            if random.random() > 0.6:
                Y[i] += random.randint(-1,1)
        for i in range(len(X)):
            dot = getDot()
            for x in range(len(dot)):
                for y in range(len(dot)):
                    image[int(Y[i])-1+y][int(X[i])-1+x] = dot[y][x]             

            
    image[image==1] = 255
    return image
