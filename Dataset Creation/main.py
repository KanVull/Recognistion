import os
import numpy as np
import cv2
import random
from draw_number import newImageOf

input_path = './test_images/'
output_path = './Dataset/'
name_of_csv_numbers = '__data_numbers.csv'
name_of_csv_marking = '__data_marking.csv'
res = (9, 16) # разрешение одной цифры
minSize = (3 * res[0], 3 * res[1])
maxSize = (9 * res[0], 9 * res[1])

dataset_numbers = open(f'{output_path}{name_of_csv_numbers}', 'w')
dataset_numbers.write('filename;width;height;class;xmin;ymin;xmax;ymax\n')
dataset_marking = open(f'{output_path}{name_of_csv_marking}', 'w')
dataset_marking.write('filename;width;height;class;xmin;ymin;xmax;ymax\n')

os.chdir(input_path)
for count, image_name in enumerate(os.listdir()):
    if count % 200 == 0:
        print(count)
    image = cv2.imread(image_name, 0)
    
    ## Удаление изображений если чёрного больше 20%
    allpixelsCount = image.size
    blackpixelsCount = np.count_nonzero((15 > image))
    if blackpixelsCount / allpixelsCount > 0.2:
        continue

    ## Сохранение границ металла
    thresh = cv2.threshold(image, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, (9,9))
    points = cv2.findNonZero(thresh)
    rect = cv2.boundingRect(points)
    shape_area = {'xmin': rect[0],
                  'ymin': rect[1],
                  'xmax': rect[2],
                  'ymax': rect[3]  
                }

    ## Расчёт размера прямоугольника метки
    countNumbers = random.randint(3,8)
    ranGenSize = [0, 0]
    ranGenSize[0] = random.randint(minSize[0], maxSize[0])
    ranGenSize[1] = round(ranGenSize[0] / res[0] * res[1])

    ## Расчёт позиции метки
    leftUpXpos = random.randrange(shape_area['xmin'], shape_area['xmax'] - countNumbers * ranGenSize[0])
    leftUpYpos = random.randrange(shape_area['ymin'], shape_area['ymax'] - ranGenSize[1])
    rightDownXpos = leftUpXpos + ranGenSize[0] * countNumbers
    rightDownYpos = leftUpYpos + ranGenSize[1]

    # cv2.rectangle(image, (leftUpXpos, leftUpYpos), (rightDownXpos,rightDownYpos), (0), 5)
    # x = round((rightDownXpos - leftUpXpos) / countNumbers)
    # for i in range(countNumbers):
    #     cv2.rectangle(image, (leftUpXpos + x * i, leftUpYpos), (leftUpXpos + (x + 1) * i, rightDownYpos), (255), 3)

    ## Получение чисел метки
    numbers = [(newImageOf(number, ranGenSize), number) for number in random.choices(range(10), k=countNumbers)]   

    position_of_numbers = []
    ## Добавление чисел на картинку
    for index, number in enumerate(numbers):
        rows,cols = number[0].shape
        position_of_numbers.append((leftUpXpos + ranGenSize[0] * index, leftUpYpos, cols + leftUpXpos + ranGenSize[0] * index, rows+leftUpYpos))
        roi = image[position_of_numbers[-1][1]:position_of_numbers[-1][3], position_of_numbers[-1][0]:position_of_numbers[-1][2]]
        img2gray = number[0].copy()
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
        img2_fg = cv2.bitwise_and(number[0],number[0],mask = mask)
        dst = cv2.add(img1_bg,img2_fg)
        image[position_of_numbers[-1][1]:position_of_numbers[-1][3], position_of_numbers[-1][0]:position_of_numbers[-1][2]] = dst

    ## Сохранение картинки с добавлением цифр в файл csv
    os.chdir('../' + output_path)
    cv2.imwrite(image_name, image)
    for i, number in enumerate(numbers):
        dataset_numbers.write(f'{image_name};{image.shape[1]};{image.shape[0]};{number[1]};{position_of_numbers[i][0]};{position_of_numbers[i][1]};{position_of_numbers[i][2]};{position_of_numbers[i][3]}\n')
    dataset_marking.write(f'{image_name};{image.shape[1]};{image.shape[0]};marking;{leftUpXpos};{leftUpYpos};{rightDownXpos};{rightDownYpos}\n')

    # cv2.imshow('img', image) 
    # cv2.waitKey(0)
    os.chdir('../' + input_path)

dataset_numbers.close()
dataset_marking.close()