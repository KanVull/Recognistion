# import tkinter
# from tkinter import filedialog as fd 
import os
from MyFilters import MyFilters

def main():
    path_in = u'F:/Python/Recognistion/Dataset/'
    path_out = u'F:/Python/Recognistion/Dataset Pre-processed Images/'
    MF = MyFilters(debug=False)
    os.chdir(path_in)
    random_paths = {path: None for path in os.listdir() if path.split('.')[-1] == 'jpg'}
    count = len(random_paths.keys())
    for inx, path in enumerate(random_paths.keys()):
        string = str(int(inx/count*100)) + '%'
        string = '\r' + ' ' * (4 - len(string)) + string + ' is processed!'
        print(string, end = '')
        if MF.uploadImage(path):
            random_paths[path] = MF.runFilters()
        else:
            print('Невозможно загрузить изображение') 
    print() 
    os.chdir(path_out)
    for inx, (name, image) in enumerate(random_paths.items()):
        if image is not None: 
            MF.saveImage(name, image)
            string = str(int(inx/count)) + '%'
            string = '\r' + ' ' * (4 - len(string)) + string + ' is saved!'
            print(string, end = '')        

if __name__ == '__main__':
    carriage_return = "I will use a carriage\rreturn"
    # print( carriage_return )
    main()

