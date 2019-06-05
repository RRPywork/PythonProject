# -*- coding: utf-8 -*-
"""
Created on Sun May 19 19:20:08 2019

@author: xzero
"""

from tkinter import *  
from tkinter import ttk  
from tkinter.ttk import Combobox
import matplotlib as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

 
#df = pd.read_csv('https://bit.ly/2A2zkI6')

#def clicked():
    
    
  
window = Tk()  
window.title("Проект по питону")  
window.geometry('1000x550')  


tab_control = ttk.Notebook(window)  
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

lf = LabelFrame(tab2, text='Plot Area') 
lf.place(x=500,y=10,height=500,width=450) 

lf2 = LabelFrame(tab2,text='Settings Area')
lf2.place(x=100,y=10,height=500,width=350)






 
menu = Menu(window)
new_item = Menu(menu)
new_item = Menu(menu, tearoff=0)
new_item.add_command(label='Новый')
new_item.add_separator()
new_item.add_command(label='Изменить')
menu.add_cascade(label='Файл', menu=new_item)
window.config(menu=menu)



tab_control.add(tab1, text='База данных')
tab_control.add(tab2, text='Отчеты')  
tab_control.pack(expand=1,fill='both')  

value = StringVar()
combo = Combobox(lf2, textvariable=value)  
lbl = Label(lf2 ,text='Выберите вид отчета:')
lbl.place(x=10,y=7,height=20,width=150)
combo['values'] = ("Столбчатая диаграмма(кач-кач)","Гистограмма(кол-кач)", "Диаграмма Бокса-Вискера(кол-кач)","Диаграмма рассеивания(2 кол - кач)", "Сводная таблица (кач-кач)", "Набор осн. опис. стат")
combo.current(0)  
combo.place(x=10,y=30, height=20, width=200)

def Buildbar():
    f=plt.Figure(figsize=(5,4),dpi=75)
    ax= f.add_subplot(111)

    data = (20, 35, 37 ,39 ,40)

    ind = np.arange(5)
    width= .5
    rects = ax.bar(ind, data, width)

    canvas = FigureCanvasTkAgg(f , master=lf)
    canvas.draw()
    canvas.get_tk_widget().place(x=20,y=10,height=450,width=400)

def Buildhist():
    f=plt.Figure(figsize=(5,4),dpi=75)
    ax= f.add_subplot(111)

    data = (20, 35, 37 ,39 ,40)

    ind = np.arange(5)
    width= .5
    rects = ax.bar(ind, data, width)

    canvas = FigureCanvasTkAgg(f , master=lf)
    canvas.draw()
    canvas.get_tk_widget().place(x=20,y=10,height=450,width=400)
    
def Buildbox():
    f=plt.Figure(figsize=(5,4),dpi=75)
    ax=f.subplots()
    

    canvas = FigureCanvasTkAgg(ax , master=lf)
    canvas.draw()
    canvas.get_tk_widget().place(x=20,y=10,height=450,width=400)
    
def Buildscatter():
    f=plt.Figure(figsize=(5,4),dpi=75)
    ax= f.add_subplot(111)

    data = (20, 35, 37 ,39 ,40)

    ind = np.arange(5)
    width= .5
    rects = ax.bar(ind, data, width)

    canvas = FigureCanvasTkAgg(f , master=lf)
    canvas.draw()
    canvas.get_tk_widget().place(x=20,y=10,height=450,width=400)

       
        
        
        
def Click():
    if combo.get()=="Диаграмма рассеивания(2 кол - кач)":
        elem1 = Combobox(lf2)
        lbl1 = Label(lf2, text="Выберите количественный атрибут")
        lbl1.place(x=10, y=50, height=20, width=200)
        elem1['values']=("Частота","Цена","TDP","Объём кэша L3")
        elem1.current(0)
        elem1.place(x=10,y=73, height=20, width=200)
        lbl2 = Label(lf2, text="Выберите количественный атрибут")
        lbl2.place(x=10, y=93, height=20, width=200)
        elem2 = Combobox(lf2)
        elem2['values']=("Частота","Цена","TDP","Объём кэша L3")
        elem2.current(0)
        elem2.place(x=10,y=116, height=20,width=200)
        btn2 = Button(lf2, text='Построить',command=Buildscatter)
        btn2.place(x=230, y=73, height=20, width=70)
        elem3 = Combobox(lf2)
        lbl3 = Label(lf2, text="Выберите качественный атрибут")
        lbl3.place(x=10, y=136, height=20, width=200)
        elem3['values']=("Модель","Линейка","Socket","Ядро","Изготовитель","Техпроцесс")
        elem3.current(0)
        elem3.place(x=10,y=159, height=20,width=200) 
    if combo.get()=="Столбчатая диаграмма(кач-кач)":
        elem3 = Combobox(lf2)
        elem1 = Combobox(lf2)
        lbl1 = Label(lf2, text="Выберите качественный атрибут")
        lbl1.place(x=10, y=50, height=20, width=200)
        elem1['values']=("Модель","Линейка","Socket","Ядро","Изготовитель","Техпроцесс")
        elem1.current(0)
        elem1.place(x=10,y=73, height=20, width=200)
        lbl2 = Label(lf2, text="Выберите качественный атрибут")
        lbl2.place(x=10, y=93, height=20, width=200)
        elem2 = Combobox(lf2)
        elem2['values']=("Модель","Линейка","Socket","Ядро","Изготовитель","Техпроцесс")
        elem2.current(0)
        elem2.place(x=10,y=116, height=20,width=200)
        btn2 = Button(lf2, text='Построить',command=Buildbar)
        btn2.place(x=230, y=73, height=20, width=70)
        elem3 = Combobox(lf2)
        lbl3 = Label(lf2, text="Выберите качественный атрибут")
        lbl3.place(x=10, y=136, height=20, width=200)
        elem3['values']=("Модель","Линейка","Socket","Ядро","Изготовитель","Техпроцесс")
        elem3.current(0)
        elem3.place(x=10,y=159, height=20,width=200)
        lbl3.destroy()
        elem3.destroy()
    if combo.get()=="Гистограмма(кол-кач)":
        elem1 = Combobox(lf2)
        lbl1 = Label(lf2, text="Выберите количественный атрибут")
        lbl1.place(x=10, y=50, height=20, width=200)
        elem1['values']=("Частота","Цена","TDP","Объём кэша L3")
        elem1.current(0)
        elem1.place(x=10,y=73, height=20, width=200)
        lbl2 = Label(lf2, text="Выберите качественный атрибут")
        lbl2.place(x=10, y=93, height=20, width=200)
        elem2 = Combobox(lf2)
        elem2['values']=("Модель","Линейка","Socket","Ядро","Изготовитель","Техпроцесс")
        elem2.current(0)
        elem2.place(x=10,y=116, height=20,width=200)
        btn2 = Button(lf2, text='Построить',command=Buildhist)
        btn2.bind('<Button-1>')
        btn2.place(x=230, y=73, height=20, width=70)
        elem3 = Combobox(lf2)
        lbl3 = Label(lf2, text="Выберите качественный атрибут")
        lbl3.place(x=10, y=136, height=20, width=200)
        elem3['values']=("Модель","Линейка","Socket","Ядро","Изготовитель","Техпроцесс")
        elem3.current(0)
        elem3.place(x=10,y=159, height=20,width=200)
        lbl3.place_forget()
        elem3.place_forget()
        n1=elem1.get()
        n2=elem2.get()
        print(n1,n2)
    if combo.get()=="Диаграмма Бокса-Вискера(кол-кач)":
        elem1 = Combobox(lf2)
        lbl1 = Label(lf2, text="Выберите количественный атрибут")
        lbl1.place(x=10, y=50, height=20, width=200)
        elem1['values']=("Частота","Цена","TDP","Объём кэша L3")
        elem1.current(0)
        elem1.place(x=10,y=73, height=20, width=200)
        lbl2 = Label(lf2, text="Выберите качественный атрибут")
        lbl2.place(x=10, y=93, height=20, width=200)
        elem2 = Combobox(lf2)
        elem2['values']=("Модель","Линейка","Socket","Ядро","Изготовитель","Техпроцесс")
        elem2.current(0)
        elem2.place(x=10,y=116, height=20,width=200)
        n=elem1.get()
        k=elem2.get()
        btn2 = Button(lf2, text='Построить',command=Buildbox)
        btn2.place(x=230, y=73, height=20, width=70)
        elem3 = Combobox(lf2)
        lbl3 = Label(lf2, text="Выберите качественный атрибут")
        lbl3.place(x=10, y=136, height=20, width=200)
        elem3['values']=("Модель","Линейка","Socket","Ядро","Изготовитель","Техпроцесс")
        elem3.current(0)
        elem3.place(x=10,y=159, height=20,width=200)
        lbl3.place_forget()
        elem3.place_forget()
   
btn = Button(lf2, text='Выбрать',command=Click)
btn.place(x=230, y=30, height=20, width=70)



window.mainloop()
