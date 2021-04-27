import tkinter
from tkinter import filedialog as fd 
from MyFilters import MyFilters

def onclick():
    path = fd.askopenfilename()
    MF = MyFilters(debug=True)
    if MF.uploadImage(path):
        lbl_answer['text'] = MF.getValueFromImage()
        # MF.showCurrentStateImage()
    else:
        print('Невозможно загрузить изображение')

root = tkinter.Tk()
root.title('Kursach')

btn = tkinter.Button(root, text='Загрузить изображение', command=onclick)
btn.grid(row=1, column=1)

lbl_answer = tkinter.Label()
lbl_answer.grid(row=2, column=1)

root.mainloop()
