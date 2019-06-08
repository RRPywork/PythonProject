# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 23:37:20 2019

@author: kolesov
@author: baleskin
"""
import sys
sys.path.insert(0, '..\\..\\')
sys.path.insert(1, '..\\')
sys.path.insert(2, '..\\Library\\')

from tkinter import messagebox as mb
import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import Canvas
from tkinter import BooleanVar
from tkinter import StringVar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Work.Library.DataBase import DataBase
from Work.Library.database_interaction.DatabaseParser import DatabaseParser
from Work.Library.configuration_parser import *

class Main(tk.Frame):
    def __init__(self, root, atributes):
        super().__init__(root)
        self.init_main(atributes)
        self.dp = dp

    def init_main(self, atributes):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        mainmenu = tk.Menu(root) 
        root.config(menu=mainmenu) 
        
        addmenu = tk.Menu(mainmenu, tearoff=0)
        addmenu.add_command(label='Добавить объект', command=self.open_add_object)
        addmenu.add_command(label='Добавить атрибут', command=self.open_add_atribute)
        
        deletemenu = tk.Menu(mainmenu, tearoff=0)
        deletemenu.add_command(label='Удалить объект', command=self.delete_object)
        deletemenu.add_command(label='Удалить атрибут', command=self.open_delete_dialog)
        
        edit = tk.Menu(mainmenu, tearoff=0)
        
        editmenu = tk.Menu(edit, tearoff=0)
        editmenu.add_command(label='Редактировать объект', command=self.open_edit_object)
        editmenu.add_command(label='Редактировать атрибут', command=self.open_edit_atribute)
        
        showmenu = tk.Menu(mainmenu, tearoff=0)
        showmenu.add_command(label='Новая сессия', command=self.open_show_DB)
        showmenu.add_command(label='Загрузить сессию', command=self.open_download_session)
        
        edit.add_cascade(label="Добавить", menu=addmenu)
        edit.add_cascade(label="Удалить", menu=deletemenu)
        edit.add_cascade(label="Редактировать", menu=editmenu)
        mainmenu.add_cascade(label="Действие", menu=edit)
        mainmenu.add_cascade(label="База данных", menu=showmenu)
        
        mainmenu.add_command(label='Сохранить', command=self.open_save_DB)
        mainmenu.add_command(label='Справка', command=self.open_info)
        mainmenu.add_command(label='Отчеты', command=self.open_reports)
        mainmenu.add_command(label='×', command=self.destroy_links)


        self.scrollbar1 = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scrollbar1.pack(side='bottom', fill='x')
        
        self.scrollbar2 = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar2.pack(side='right', fill='y')
        
        
        self.tree = ttk.Treeview(self, columns=[i for i in atributes], height=100, 
                                 xscrollcommand=self.scrollbar1.set, yscrollcommand=self.scrollbar2.set)
        self.tree.pack(side='top')
        
        for i in atributes:
             self.tree.column(i, anchor=tk.CENTER)
             
        for i in atributes:
            self.tree.heading(i, text=i)
        self.tree.heading("#0", text="Model")
        
        self.scrollbar1.config(command=self.tree.xview)
        self.scrollbar2.config(command=self.tree.yview)
        
        self.update_DB()

    def open_reports(self):
        self.app1 = Reports()

    def download_session(self, entry):
        #print('11111')
        #print(entry.get()+'!')
        dp.parse("LOAD",entry.get())
        self.update_DB()
    
    def destroy_links(self):
        self.tree.focus_set()
        self.update_DB()
        

    def update_DB(self):
        self.tree.config(columns=[i for i in dp.working_db.get_db().columns])
        for i in dp.working_db.get_db().columns:
             self.tree.column(i, anchor=tk.CENTER)
             self.tree.heading(i, text=i)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row_data[1], text=row_data[0]) for row_data in zip(dp.working_db.get_db().index.tolist(), dp.working_db.get_db().values.tolist())]
        
    def add_object(self, key_entry, Entries):
        dp.parse("APPEND",[],[key_entry.get()],[{i:j for i,j in zip(dp.working_db.get_db().columns,[k.get() for k in Entries])}], None)
        self.update_DB()
    
    def add_atribute(self,entry,combobox):
        dp.parse("APPEND",[entry.get()],[],[],None)
        self.update_DB()
    
    def delete_object(self):
        if self.tree.selection()== ():
            mb.showerror('Ошибка','Должны быть выбраны объекты')
        else:
            for i in self.tree.selection():   
                dp.parse("DELETE",[],[self.tree.item(i)['text']])
            self.update_DB()
    
    def delete_atribute(self, Entries):
        dp.parse("DELETE",[dp.working_db.get_db().columns[i] for i in Entries],[])
        self.update_DB()
        
    
    def edit_object(self, Entries):
        for i,j in zip(dp.working_db.get_db().columns,Entries):
            dp.parse("CHANGE", i, self.tree.item(self.tree.selection()[0])['text'],str(j.get()))
        self.tree.focus_set()
        self.update_DB()
        
    def select_all(self, Variables):
        for i in Variables:
            if i.get()==False:
                [j.set(True) for j in Variables]
            else:
                [j.set(False) for j in Variables]
    
    def edit_atribute(self,combobox,entry):
        dp.parse("RENAME", {combobox.get():entry.get()}, "columns")
        self.update_DB()
    
    def view_records(self, Variables, atributes):
        dp.parse("DISPLAY",["-i"]+[i for i,j in zip(atributes,Variables) if j.get()],[None,None], None)
        self.update_DB()
    
    def save_DB(self, entry):
        dp.parse("STORE", entry.get())
        
    def open_download_session(self):
        Download_session()
        
    def open_info(self):
        pass

    def open_add_object(self):
        Add_object(atributes)
        
    def open_add_atribute(self):
        Add_atribute()
        
    def open_delete_dialog(self):
        Delete_atribute()
        
    def open_edit_object(self):
        if self.tree.selection()==():
            mb.showerror('Ошибка','Должен быть выбран объект')
        else:
            Edit_object()
        
    def open_edit_atribute(self):
        Edit_atribute()
    
    def open_show_DB(self):
        Show_DB(atributes)
        
    def open_save_DB(self):
        Save_DB()
        
        
class Download_session(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        
    def init_child(self):
        self.title('Загрузка сессии')
        self.geometry('300x150+400+300')
        self.resizable(False, False)
        
        self.label_name1 = tk.Label(self, text='Введите название существующей базы даных:')
        self.label_name1.pack(side='top', pady=7)
        
        self.label_name2 = tk.Label(self, text='(без расширения)')
        self.label_name2.pack(side='top')
        
        self.entry = ttk.Entry(self, width=30)
        self.entry.pack(side='top', pady=7)
        
        
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=210, y=110)

        self.btn_ok = ttk.Button(self, text='Загрузить', command=self.destroy)
        self.btn_ok.place(x=130, y=110)
        
        self.btn_ok.bind('<Button-1>', lambda event: self.view.download_session(self.entry))
        
        self.grab_set()
        self.focus_set() 
    
class Delete_atribute(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        
    def init_child(self):
        self.title('Удалить атрибуты')
        self.geometry('200x300+400+300')
        self.resizable(False, False)
                
        myframe=tk.Frame(self,width=200,height=250)
        myframe.pack(anchor='nw')
        myscrollbar=tk.Scrollbar(myframe,orient="vertical")
        myscrollbar.pack(side='right',fill='y')
        lbox=tk.Listbox(myframe,width=30,height=16, selectmode=tk.EXTENDED, yscrollcommand=myscrollbar.set)
        myscrollbar.configure(command=lbox.yview)
        lbox.pack(anchor='nw')
        [lbox.insert(tk.END,i) for i in dp.working_db.get_db().columns]
                         
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=20, y=265)

        btn_ok = ttk.Button(self, text='Удалить', command=self.destroy)
        btn_ok.place(x=100, y=265)
    
        btn_ok.bind('<Button-1>', lambda event: self.view.delete_atribute(lbox.curselection()))
    
        self.grab_set()
        self.focus_set()
    
class Add_object(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(root)
        self.init_child(atributes)
        self.view = app
        
    def init_child(self, atributes):
        self.title('Добавить новый объект')
        self.geometry('350x300+400+300')
        self.resizable(False, False)
                
        self.myframe=tk.Frame(self,width=300,height=300,bd=0)
        self.myframe.place(x=0,y=0)
        
        canvas=Canvas(self.myframe,bd=0,highlightthickness=0)
        self.frame=tk.Frame(canvas, bd=0)
        myscrollbar=tk.Scrollbar(self.myframe,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)
    
        myscrollbar.pack(side="right",fill="y")
        canvas.pack(side="left")
        canvas.create_window((0,10),window=self.frame,anchor='nw')
        self.frame.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all"),width=330,height=250))
        
        self.Key_label=ttk.Label(self.frame, text='Model:')
        self.Key_label.grid(row=0, column=2, pady=3, padx=30, sticky='w')
        
        self.Key_entry=ttk.Entry(self.frame)
        self.Key_entry.grid(row=0, column=3, padx=30)
        
        self.Labels = [ttk.Label(self.frame, text=i+':') for i in dp.working_db.get_db().columns]
        self.Entries = [ttk.Entry(self.frame) for i in range(len(dp.working_db.get_db().columns))]
        
        for i,j in zip([i for i in range(len(dp.working_db.get_db().columns)+1)[1:]], self.Labels):
            j.grid(row=i,column=2, pady=3, padx=30, sticky='w')
            
        for i,j in zip([i for i in range(len(dp.working_db.get_db().columns)+1)[1:]], self.Entries):
            j.grid(row=i,column=3, pady=3, padx=30)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=240, y=265)

        self.btn_ok = ttk.Button(self, text='Добавить', command=self.destroy)
        self.btn_ok.place(x=160, y=265)
        
        self.btn_ok.bind('<Button-1>', lambda event: self.view.add_object(self.Key_entry, self.Entries))    
    
        self.grab_set()
        self.focus_set()

class Add_atribute(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child(atributes)
        self.view = app
        
    def init_child(self, atributes):
        self.title('Добавить новый атрибут')
        self.geometry('300x200+400+300')
        self.resizable(False, False)
        
        self.label_name = tk.Label(self, text='Имя атрибута:')
        self.label_name.place(x=30,y=40)
        
        self.entry = ttk.Entry(self)
        self.entry.place(x=130, y=40)
        
        self.label_type = tk.Label(self, text = 'Тип данных:')
        self.label_type.place(x=30, y=90)
        
        self.combobox = ttk.Combobox(self, values=['Число','Строка'], width=17)
        self.combobox.place(x=130, y=90)
        
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=210, y=160)

        self.btn_ok = ttk.Button(self, text='Добавить', command=self.destroy)
        self.btn_ok.place(x=130, y=160)
        
        self.btn_ok.bind('<Button-1>', lambda event: self.view.add_atribute(self.entry, self.combobox))
        
        self.grab_set()
        self.focus_set() 
        
class Edit_atribute(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        
    def init_child(self):
        self.title('Редактировать атрибут')
        self.geometry('300x200+400+300')
        self.resizable(False, False)
        
        self.label_name = tk.Label(self, text='Новое название:')
        self.label_name.place(x=30,y=90)
        
        self.entry = ttk.Entry(self)
        self.entry.place(x=130, y=90)
        
        self.label_type = tk.Label(self, text = 'Атрибут:')
        self.label_type.place(x=30, y=40)
        
        self.combobox = ttk.Combobox(self, values=[i for i in dp.working_db.get_db().columns], width=17)
        self.combobox.place(x=130, y=40)
        
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=210, y=160)

        self.btn_ok = ttk.Button(self, text='Сохранить', command=self.destroy)
        self.btn_ok.place(x=130, y=160)
        
        self.btn_ok.bind('<Button-1>', lambda event: self.view.edit_atribute(self.combobox, self.entry))
        
        self.grab_set()
        self.focus_set() 
        
class Edit_object(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child(self.view)
        
    def init_child(self,view):
        self.title('Редактировать объект')
        self.geometry('350x300+400+300')
        self.resizable(False, False)
                
        self.myframe=tk.Frame(self,width=300,height=300,bd=0)
        self.myframe.place(x=0,y=0)
        
        canvas=Canvas(self.myframe,bd=0,highlightthickness=0)
        self.frame=tk.Frame(canvas, bd=0)
        myscrollbar=tk.Scrollbar(self.myframe,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)
    
        myscrollbar.pack(side="right",fill="y")
        canvas.pack(side="left")
        canvas.create_window((0,10),window=self.frame,anchor='nw')
        self.frame.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all"),width=330,height=250))
        
        self.Variables = [StringVar() for i in range(len(dp.working_db.get_db().columns))]
        self.Labels = [ttk.Label(self.frame, text=i+':') for i in dp.working_db.get_db().columns]
        self.Entries = [ttk.Entry(self.frame, textvariable=j) for i,j in zip(range(len(dp.working_db.get_db().columns)),self.Variables)]
        
        [self.Variables[j].set(i) for i,j in zip(view.tree.item(view.tree.selection())['values'],range(len(self.Variables)))]        
        for i,j in zip([i for i in range(len(dp.working_db.get_db().columns))], self.Labels):
            j.grid(row=i,column=2, pady=3, padx=30, sticky='w')
            
        for i,j in zip([i for i in range(len(dp.working_db.get_db().columns))], self.Entries):
            j.grid(row=i,column=3, pady=3, padx=30)
                          
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=240, y=265)

        self.btn_ok = ttk.Button(self, text='Сохранить', command=self.destroy)
        self.btn_ok.place(x=160, y=265)
        
        self.btn_ok.bind('<Button-1>', lambda event: self.view.edit_object(self.Entries))
        self.btn_cancel.bind('<Button-1>', lambda event: self.view.destroy_links())
        
        self.grab_set()
        self.focus_set()
        
class Show_DB(tk.Toplevel):
    def __init__(self, atributes):
        super().__init__(root)
        self.init_child(atributes)
        self.view = app
        

        
    def init_child(self, atributes):
        self.title('Отобразить')
        self.geometry('200x300+400+300')
        self.resizable(False, False)
                
 
        self.myframe=tk.Frame(self,width=200,height=300,bd=0)
        self.myframe.place(x=0,y=0)
        
        canvas=Canvas(self.myframe,bd=0,highlightthickness=0)
        self.frame=tk.Frame(canvas, bd=0)
        myscrollbar=tk.Scrollbar(self.myframe,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)
    
        myscrollbar.pack(side="right",fill="y")
        canvas.pack(side="left")
        canvas.create_window((0,10),window=self.frame,anchor='nw')
        self.frame.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all"),width=180,height=250))
        
        self.Variables = [BooleanVar() for i in range(len(atributes))]
        self.Checkbuttons = [tk.Checkbutton(self.frame, text=i, variable=j) for i,j in zip(atributes,self.Variables)]
        
        self.checkbutton_stringvar = BooleanVar()
        self.checkbutton = tk.Checkbutton(self.frame, text='Выбрать все', variable=self.checkbutton_stringvar)
        self.checkbutton.grid(row=1,column=2, pady=3, padx=20, sticky='w')
        
        for i,j in zip([i for i in range(len(self.Checkbuttons))], self.Checkbuttons):
            j.grid(row=i+1,column=2, pady=3, padx=20, sticky='w')
            
        self.checkbutton.bind('<Button-1>', lambda event: self.view.select_all(self.Variables))
                         
        
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=20, y=265)

        btn_ok = ttk.Button(self, text='Обновить', command=self.destroy)
        btn_ok.place(x=100, y=265)
        
        
        btn_ok.bind('<Button-1>', lambda event: self.view.view_records(self.Variables, atributes))
    
        self.grab_set()
        self.focus_set()
        
    
class Save_DB(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        
    def init_child(self):
        self.title('Сохранение базы данных')
        self.geometry('300x150+400+300')
        self.resizable(False, False)
        
        self.label_name1 = tk.Label(self, text='Введите название новой базы даных:')
        self.label_name1.pack(side='top', pady=7)
        
        self.label_name2 = tk.Label(self, text='(без расширения)')
        self.label_name2.pack(side='top')
        
        self.entry = ttk.Entry(self, width=30)
        self.entry.pack(side='top', pady=7)
        
        
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=210, y=110)

        self.btn_ok = ttk.Button(self, text='Сохранить', command=self.destroy)
        self.btn_ok.place(x=130, y=110)
        
        self.btn_ok.bind('<Button-1>', lambda event: self.view.save_DB(self.entry))
        
        self.grab_set()
        self.focus_set() 


class Reports(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.state('zoomed')
        self.dataframe = self.view.dp.working_db.get_db()
        self.attributes = list(self.dataframe.keys())
        self.v_attrs = [str(attr) for attr in self.attributes if self.isValAttr(str(attr))]
        self.q_attrs = [str(attr) for attr in self.attributes if not attr in self.v_attrs]
        self.figure=plt.Figure(figsize=(5,4),dpi=75)
        self.ax= self.figure.add_subplot(111)
        self.to_delete=[]
        self.combos = []
        self.labels=[]
        self.to_file = None
        self.report_type= "NONE"
        self.text_type="NONE"
        self.init_child(self.view)


    def isValAttr(self, attr):
        val = str(self.dataframe[attr].iloc[0])
        dots=0
        for ch in val:
            if not(str.isdigit(ch) or (ch == '.')):
                return False
            if ch=='.':
                dots+=1
            if(dots>1):
                return False
        return True

    def init_child(self, view):
        self.title('Проект по питону')
        self.geometry('1000x550')
        self.plot_area_frame = tk.LabelFrame(self, text='Plot Area')
        self.plot_area_frame.place(x=500,y=10,height=500,width=450)

        self.settings_area_frame = tk.LabelFrame(self,text='Settings Area')
        self.settings_area_frame.place(x=100,y=10,height=500,width=350)

        self.menu = tk.Menu(self)
        new_item = tk.Menu(self.menu, tearoff=0)
        new_item.add_command(label='Новый')
        new_item.add_separator()
        new_item.add_command(label='Изменить')
        self.menu.add_cascade(label='Файл', menu=new_item)

        self.btn_save = ttk.Button(self.settings_area_frame, text='Сохранить', command=self.open_save_report)
        self.btn_save.pack(side='bottom', anchor='se')

        value = StringVar()
        self.combo = ttk.Combobox(self.settings_area_frame, textvariable=value)
        lbl = tk.Label(self.settings_area_frame ,text='Выберите вид отчета:')
        lbl.place(x=10,y=7,width=150)
        self.combo['values'] = ("Столбчатая диаграмма(кач-кач)","Гистограмма(кол-кач)",
                                "Диаграмма Бокса-Вискера(кол-кач)","Диаграмма рассеивания(2 кол - кач)",
                                "Сводная таблица (кач-кач)", "Набор осн. опис. стат")
        self.combo.current(0)
        self.combo.place(x=10,y=30, width=200)

        self.choose_btn = ttk.Button(self.settings_area_frame, text='Выбрать',command=self.click)
        self.choose_btn.place(x=250, y=30, width=70)

        self.btn_cancel = ttk.Button(self.settings_area_frame, text='Закрыть', command=self.destroy)
        self.btn_cancel.pack(anchor='se', side='bottom')
#        self.btn_cancel.bind('<Button-1>', lambda event: self.view.destroy_links())
        self.grab_set()
        self.focus_set()

    def paint_figure(self):
        """"""
        self.report_type= "GRAPH"
        canvas = FigureCanvasTkAgg(self.figure , master=self.plot_area_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=20,y=10,height=450,width=400)
        self.to_file = self.figure

    def clear(self):
        self.figure.clear()
        self.figure=plt.Figure(figsize=(5,4),dpi=75)
        self.ax= self.figure.add_subplot(111)

    def add_combo(self, attrs, text):
        ys=[73,116,159,202]
        self.combos.append(ttk.Combobox(self.settings_area_frame))
        self.labels.append(tk.Label(self.settings_area_frame, text=text, anchor='w'))
        self.to_delete.append(self.combos[-1])
        self.combos[-1]["values"]=attrs
        self.combos[-1].current(0)
        self.combos[-1].place(x=10, y=ys[len(self.combos)-1]+2, height=20, width=200)
        self.labels[-1].place(x=10, y=ys[len(self.combos)-1]-21, height=20)
        self.to_delete.append(self.labels[-1])

    def click(self):
        for i in self.to_delete:
            i.destroy()
        self.to_delete.clear()
        self.combos.clear()
        self.clear()
        btn2 = ttk.Button(self.settings_area_frame, text='Построить')
        if self.combo.get()=="Диаграмма рассеивания(2 кол - кач)":
            self.add_combo(self.v_attrs, text="Выберите количественный атрибут")
            self.add_combo(self.v_attrs, text="Выберите количественный атрибут")
            self.add_combo(self.q_attrs, text="Выберите качественный атрибут")
            btn2.bind("<Button-1>", self.Buildscatter)

        if self.combo.get()=="Столбчатая диаграмма(кач-кач)":
            self.add_combo(self.q_attrs, text="Выберите качественный атрибут")
            self.add_combo(self.q_attrs, text="Выберите качественный атрибут")
            btn2.bind("<Button-1>",self.Buildbar)
        if self.combo.get()=="Гистограмма(кол-кач)":
            self.add_combo(self.v_attrs, text="Выберите количественный атрибут")
            self.add_combo(self.q_attrs, text="Выберите качественный атрибут")
            btn2.bind("<Button-1>",self.Buildhist)
        if self.combo.get()=="Диаграмма Бокса-Вискера(кол-кач)":
            self.add_combo(self.v_attrs, text="Выберите количественный атрибут")
            self.add_combo(self.q_attrs, text="Выберите качественный атрибут")
            btn2.bind("<Button-1>",self.Buildbox)
        if self.combo.get()=="Сводная таблица (кач-кач)":
            self.add_combo(self.q_attrs, text="Выберите качественный атрибут")
            self.add_combo(self.q_attrs, text="Выберите качественный атрибут")
            self.add_combo(self.v_attrs, text="Выберите количественный атрибут для аггрегации")
            self.add_combo(["mean", "sum", "standard deviation"], text="Выберите метод аггрегации")
            btn2.bind("<Button-1>",self.BuildPivot)
        if self.combo.get()=="Набор осн. опис. стат":
            self.listbox = tk.Listbox(self.settings_area_frame, selectmode='extended', height=5)
            [self.listbox.insert('end',i) for i in self.v_attrs]
            self.label = tk.Label(self.settings_area_frame, text='Выберите атрибуты:')
            self.label.place(x=10, y=70)
            self.to_delete.append(self.label)
            self.listbox.place(x=10, y=95)
            self.to_delete.append(self.listbox)
            btn2.bind("<Button-1>",lambda event: self.MajorDescStats(self.listbox.curselection()))
        btn2.place(x=250, y=73, width=70)


    def Buildbar(self, event=None):
        first_attr = self.combos[0].get()
        second_attr = self.combos[1].get()
        vals_prep = {i:set() for i in set(self.dataframe[first_attr].values)}
        for i in self.dataframe[[first_attr, second_attr]].values:
            vals_prep[i[0]].add(i[1])
        self.clear()
        vals = {i:len(vals_prep[i]) for i in vals_prep.keys()}
        indices = list(set(self.dataframe[first_attr].values))
        d = pd.DataFrame({first_attr:indices, second_attr:list(vals.values())})
        d.plot.bar(ax=self.ax,x=first_attr, y=second_attr)
        #add label, saying "Измеряется количество разных значений второго атрибута"
        self.paint_figure()

    def Buildhist(self, event=None):
        first_attr = self.combos[0].get()
        second_attr = self.combos[1].get()
        self.clear()
        self.dataframe.hist(ax=self.ax, column=first_attr, by=second_attr, bins=int(1+np.log2(len(self.dataframe[first_attr].values))))
        self.paint_figure()

    def Buildbox(self, event=None):
        first_attr = self.combos[0].get()
        second_attr = self.combos[1].get()
        self.clear()
        self.dataframe.boxplot(ax=self.ax, by=second_attr, column=first_attr)
        self.paint_figure()

    def Buildscatter(self, event=None):
        first_attr = self.combos[0].get()
        second_attr = self.combos[1].get()
        third_attr = self.combos[2].get()
        s = list(set(self.dataframe[third_attr].values))
        colormap = {s[i] : i for i in range(len(s))}
        colors = [colormap[element] for element in self.dataframe[third_attr].values]
        ind = np.arange(5)
        width= .5
        self.clear()
        self.dataframe.plot.scatter(ax=self.ax, x=first_attr, y=second_attr, c=colors, colormap='viridis')
        text=""
        for item in colormap.items():
            text+=str(item[0]) + ":" + str(item[1]) + "\n"
        self.lblLegend = tk.Label(self, text=text)
        self.lblLegend.place(x=1000,y=10, height=len(colormap)*20, width=200)
        self.to_delete.append(self.lblLegend)
        self.paint_figure()

    def BuildPivot(self, event=None):
        first_attr = self.combos[0].get()
        second_attr = self.combos[1].get()
        third_attr = self.combos[2].get()
        agg_method = self.combos[3].get()
        agg_func = None
        if agg_method=="mean":
            agg_func = np.mean
        elif agg_method=="sum":
            agg_func = np.sum
        elif agg_method=="standard deviation":
            agg_func = np.std
        self.clear()
        self.pivot = self.dataframe.pivot_table(index=first_attr, columns=second_attr, values=third_attr, fill_value=0, aggfunc=agg_func)
        print(self.pivot)
        self.report_type = "TEXT"
        self.text_type="PIVOT"
        self.scrollbar1 = tk.Scrollbar(self.plot_area_frame, orient=tk.HORIZONTAL)
        self.scrollbar1.pack(side='bottom', fill='x')

        self.scrollbar2 = tk.Scrollbar(self.plot_area_frame, orient=tk.VERTICAL)
        self.scrollbar2.pack(side='right', fill='y')
        self.tree = ttk.Treeview(self.plot_area_frame, columns=[i for i in self.pivot.keys()], height=50,
                                 xscrollcommand=self.scrollbar1.set, yscrollcommand=self.scrollbar2.set)
        self.tree.pack(side='right')
        self.to_file = self.pivot
        for i in self.pivot.keys():
             self.tree.column(i, anchor=tk.CENTER)

        for i in self.pivot.keys():
            self.tree.heading(i, text=i)

        self.scrollbar1.config(command=self.tree.xview)
        self.scrollbar2.config(command=self.tree.yview)
        self.tree.config(columns=[i for i in self.pivot.columns])
        for i in self.pivot.columns:
             self.tree.column(i, anchor=tk.CENTER)
             self.tree.heading(i, text=i)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row_data[1], text=row_data[0]) for row_data in zip(self.pivot.index.tolist(), self.pivot.values.tolist())]
        self.to_delete.append(self.tree)
        
    def save_report(self, entry, combobox):
#        Создать окно, в котором можно выбрать имя файла и формат, произвести сохранение
#        Конструктор принимает сохраняемый объект, его тип - графический или текстовый, и сохраняет в файл.
#        Формат граф. файла определяет пользователь. Для текстовых отчетов: набор осн.опис.стат - .txt; сводная таблица - .xslx
        name = entry.get()+combobox.get().lower()#change to choice result
        if self.report_type== "GRAPH":
            f = open(os.path.dirname(os.path.realpath(__file__))+ "\\..\\Graphics\\"+ name, 'w')
            f.close()
            self.figure.savefig(fname=os.path.dirname(os.path.realpath(__file__))+ "\\..\\Graphics\\"+ name)
        elif self.report_type== "TEXT":
            if self.text_type == "PIVOT":
                name = "text1.xlsx"
                f = open(os.path.dirname(os.path.realpath(__file__))+ "\\..\\Output\\"+ name, 'w')
                f.close()
                self.pivot.to_excel(os.path.dirname(os.path.realpath(__file__))+ "\\..\\Output\\"+ name, sheet_name="pivot_table")


    def MajorDescStats(self, atributes1):
        atributes = [self.v_attrs[i] for i in list(atributes1)]
        self.index = atributes
        self.DICT = {'Среднее арифметическое':[round(np.mean(self.dataframe[i].values)) for i in atributes],'Мода':[Counter(np.array(self.dataframe[i].values).flat).most_common(1)[0][0] for i in atributes],
                'Медиана':[np.median(self.dataframe[i].values) for i in atributes],'Стандартное отклонение':[round(np.std(self.dataframe[i].values)) for i in atributes]}
        self.df = pd.DataFrame(self.DICT,index=self.index)
        self.scrollbar1 = tk.Scrollbar(self.plot_area_frame, orient=tk.HORIZONTAL)
        self.scrollbar1.pack(side='bottom', fill='x')

        self.scrollbar2 = tk.Scrollbar(self.plot_area_frame, orient=tk.VERTICAL)
        self.scrollbar2.pack(side='right', fill='y')
        self.tree = ttk.Treeview(self.plot_area_frame, columns=[i for i in self.df.columns], height=35, 
                                 xscrollcommand=self.scrollbar1.set, yscrollcommand=self.scrollbar2.set)
        self.tree.pack(side='right')
        
        for i in self.df.columns:
             self.tree.column(i, anchor=tk.CENTER)
             
        for i in self.df.columns:
            self.tree.heading(i, text=i)
        self.tree.heading("#0", text="Атрибут")
        
        self.scrollbar1.config(command=self.tree.xview)
        self.scrollbar2.config(command=self.tree.yview)
        self.to_delete.append(self.tree)
        self.to_delete.append(self.scrollbar1)
        self.to_delete.append(self.scrollbar2)             
    def open_save_report(self):
        Save_report(self.to_file, self.report_type, self.text_type)
    
class Save_report(tk.Toplevel):
    def __init__(self, to_file, report_type, text_type="NONE"):
        super().__init__(root)
#        self.plottype1 = plottype
#        self.figure1 = figure
#        self.text_type1 = text_type
#        self.pivot1 = pivot
        self.to_file = to_file
        self.report_type = report_type
        self.text_type = text_type
        self.view = app
        self.init_child()
        
    def init_child(self):
        self.title('Сохранение отчета')
        self.geometry('300x200+400+300')
        self.resizable(False, False)
        
        self.label_name1 = tk.Label(self, text='Введите название файла (без расширения):')
        self.label_name1.pack(side='top', pady=7)
        
        self.entry = ttk.Entry(self, width=30)
        self.entry.pack(side='top', pady=7)
        
        self.label_name1 = tk.Label(self, text='Выберите расширение:')
        self.label_name1.pack(side='top', pady=7)
        if self.report_type=='GRAPH' :
            self.combobox = ttk.Combobox(self, values=['PDF','PNG','JPEG'])
        elif self.report_type=='TEXT':
            if self.text_type=='PIVOT':
                self.combobox = ttk.Combobox(self, values=['xlsx'])
            elif self.text_type=='MDS':
                self.combobox = ttk.Combobox(self, values=['txt'])
        self.combobox.pack(side='top', pady=7)
        
        
        
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=210, y=160)

        self.btn_ok = ttk.Button(self, text='Сохранить', command=self.save)
        self.btn_ok.place(x=130, y=160)
        
        #self.btn_ok.bind('<Button-1>', lambda event: self.save)
        
        self.grab_set()
        self.focus_set()

    def save(self, event=None):
        self.filename = self.entry.get()
        self.extension = self.combobox.get()
        if(self.report_type=='GRAPH'):
            f = open(os.path.dirname(os.path.realpath(__file__))+ "\\..\\Graphics\\"+ self.filename + '.' + self.extension, 'w')
            f.close()
            self.to_file.savefig(fname=os.path.dirname(os.path.realpath(__file__))+ "\\..\\Graphics\\"+ self.filename + '.' + self.extension)
        elif(self.report_type=='TEXT'):
            if self.text_type=='PIVOT':
                f = open(os.path.dirname(os.path.realpath(__file__))+ "\\..\\Output\\"+ self.filename + '.' + self.extension, 'w')
                f.close()
                self.to_file.to_excel(os.path.dirname(os.path.realpath(__file__))+ "\\..\\Output\\"+ self.filename + '.' + self.extension, sheet_name="pivot_table")
        self.destroy()


    
if __name__ == "__main__":
    root = tk.Tk()
    cp = ConfigurationParser("config.ini")
    config = cp.parse()
    main_dbs = config["paths"]

    dp = DatabaseParser(list(main_dbs.items.keys()),main_dbs.items, hints=config["hints"].items)
    dp.parse("DISPLAY",["-e",None],[None,None],None)
    atributes = dp.working_db.get_db().columns
    app = Main(root, atributes)
    app.pack()
    root.title("База данных CPU")
    root.state('zoomed')
    root.geometry("650x345+300+200")
    root.mainloop()
