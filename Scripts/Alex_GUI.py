# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 23:37:20 2019

@author: kolesov
"""
from abc import ABC
from abc import abstractmethod
from pandas import DataFrame
from pandas import Series
from pandas import read_csv
from tkinter import messagebox as mb
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import BooleanVar
from tkinter import StringVar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

"""
Содержит обработчик запросов к базе данных.
Задача: искоренить влияние Pandas (по возможности) из потока данных. Поток данных не должен от него зависеть.
Вполне возможно (и так действительно может получиться!), обработчики и GUI будут частично зависеть от Pandas,
(используем Pandas как обертку для MatPlotLib) но потоку не должно быть никакого дела до передаваемых по нему объектов.
Author: Vitaly(Admin)
"""
""""""
class Block:
    """"""
    def __init__(self, block_name):
        """"""
        self.name = block_name
        self.items = dict()

    def add_item(self, item_name, item_value):
        self.items[item_name]=item_value



class ConfigurationParser:
    """"""
    def __init__(self, path):
        """"""
        self.path = path
        self.blocks = dict()

    def parse(self):
        """"""
        with open(self.path, 'r') as f:
            block_name = ""
            strs=f.readlines()
            for line in strs:
                if line[0]=='[':
                    block_name = line[1:-2]
                    self.blocks[block_name]=Block(block_name)
                elif line!="":
                    name, val = line.split('=')
                    val = val[:-1] if val[-1]=='\n' else val
                    self.blocks[block_name].add_item(name, val)
        return self.blocks


class DBInterface(ABC):
    """
    Абстрактный класс-интерфейс
    """
    @abstractmethod
    def parse(self, *pargs):
        """Абстрактный метод. Должен быть унаследован потомками. Парсит БД и возвращает данные"""
        

class DatabaseParser(DBInterface):
    """
    Обработчик
    """
    def __init__(self, names, paths, hints=None):
        """
        Конструктор. Добывает БД из файлов csv (или sql, или ... Смотря что в методе)
        и помещает их в словарь отношение:БД
        """
        assert len(names) == len(paths)
        self.its_dbs = {i:DataBase() for i in names}
        if hints is not None:
            self.hints = {i:hints[i] for i in names}
        for i in names:
            self.its_dbs[i].read(paths[i])
        self.attr_names = {names[i]:self.its_dbs[names[i]].get_attr_names() for i in range(len(names))}
        self.working_db = DataBase()

    def inclusive_attr_display(self, attr_names):
        excl_attr_names = []
        for attrs in self.attr_names.values():
            for attr in attrs:
                if attr not in attr_names:
                    excl_attr_names.append(attr)
        self.exclusive_attr_display(excl_attr_names)

    def inclusive_obj_display(self, obj_names):
        self.working_db = self.working_db.get_objects(obj_names)

    def exclusive_attr_display(self, attr_names):
        self.working_db = DataBase()
        for (name, db) in self.its_dbs.items():
            a = self.working_db.join(db, on=self.hints[name] if self.hints[name]!='-' else None, how='inner')
            self.working_db = a
        if attr_names is not None:
            for attr in attr_names:
                self.working_db.delete_attribute(attr)

    def exclusive_obj_display(self, obj_names):
        self.working_db.delete_objects(obj_names)

    def parse(self, q_type, *pargs):
        """
        Метод, отвечающий за обработку.
        Выполняет выбор типа операции в зависимости от аргументов (в частности, первого) и делегирует частным случаям.
        Первый аргумент - тип запроса
        Второй - условия
        Итого:
        query -> query_type args
        query_type -> DISPLAY | ADD | DROP | APPEND | DELETE | STORE | CHANGE | RENAME
        args -> attr_list obj_list conditions |
                names path_names hints|
                names |
                _names _names values name|
                _names _names values|
                pathname|
                obj_name attr_name value|
                dictionary, axis
        names, path_names, _names, name - строки (или списки строк!) (возможны пустые строки)
        attr_list -> key _names | NONE
        obj_list -> key _names | NONE
        key -> NONE | -e | -i (Отсутствие ключа = Отсутствие аргумента -> тогда под условие попадает все!) i - включая;  e - исключая
        conditions - процессоры boolean(Database, obj_name, attr_name)
        """
        if q_type == 'DISPLAY':
            attr_key = pargs[0][0]
            attr_names = pargs[0][1:]
            obj_key = pargs[1][0]
            obj_names = pargs[1][1:]
            conditions = pargs[2]
            if self.working_db.empty():
                self.working_db = DataBase(name='DATA')
            if(attr_key is not None):
                if attr_key == '-i':
                    self.inclusive_attr_display(attr_names)
                elif attr_key == '-e':
                    self.exclusive_attr_display(attr_names)
            if(obj_key is not None):
                if obj_key == '-i':
                    self.inclusive_obj_display(obj_names)
                elif obj_key == '-e':
                    self.exclusive_obj_display(obj_names)
            if(conditions is not None):
                for cond in conditions:
                    cond._process(self.working_db)

        elif q_type == 'ADD':
            names = pargs[0]
            path_names = pargs[1]
            hints = pargs[2]
            for (name, hint) in hints.items():
                self.hints[name]=hint
            for i in range(len(names)):
                db = DataBase()
                db.read(path_names[i])
                self.its_dbs[names[i]] = db
            self.attr_names = {i:self.its_dbs[i].get_attr_names() for i in self.its_dbs.keys()}

        elif q_type == 'DROP':
            names = pargs[0]
            for name in names:
                del self.its_dbs[name]
            self.attr_names = {i:self.its_dbs[i].get_attr_names() for i in self.its_dbs.keys()}
        elif q_type == 'APPEND':
            attr_names = pargs[0]
            obj_names = pargs[1]
            obj_values = pargs[2]
            name = pargs[3]
            if name is not None:
                self.working_db.join(self.its_dbs[name].get_attributes(attr_names), on=None, how='inner')
            else:
                global_failure=False
                for attr in attr_names:
                    failure = True
                    for n, attrs in self.attr_names.items():
                        if attr in attrs:
                            self.working_db.join(self.its_dbs[n].get_attributes([attr]), on=None, how='inner')
                            failure = False
                            break
                    if failure:
                        self.working_db.append_attribute(attr, [None for i in self.working_db.get_db().values])
                        global_failure = True


            objects = dict(zip(obj_names, obj_values))
            for o_name, values in objects.items():
                self.working_db.append_object(o_name, list(values.keys()), list(values.values()))

        elif q_type == 'DELETE':
            attr_names = pargs[0]
            obj_names = pargs[1]
            self.working_db.delete_objects(obj_names)
            for attr in attr_names:
                self.working_db.delete_attribute(attr);
        elif q_type == 'STORE':
            path_name = pargs[0]
            self.working_db.store(path_name)
        elif q_type == 'CHANGE':
            attr_name = pargs[0]
            obj_name = pargs[1]
            value = pargs[2]
            self.working_db.change_value(obj_name, attr_name, value)
        elif q_type == 'RENAME':
            mapper = pargs[0]
            axis = pargs[1]
            self.working_db.rename(mapper, axis)
        pass


class DataBase:
    """
    Класс с БД - это лучший класс
    """
    def __init__(self, db=None, name=None):
        """"""
        if db is None:
            self.db = DataFrame()
        else:
            self.db = DataFrame(db)
        if name is None:
            self.name = ''
        else:
            self.name = name

    def get_db(self):
        """"""
        return self.db

    def get_attr_names(self):
        d = [i for i in self.db.keys()]
        return d;

    def append_object(self, index, column_data, object_data):
        """"""
        self.db = self.db.append(Series(object_data, index=column_data, name=index))

    def append_attribute(self, attr_name, attr_values):
        """"""
        self.db[attr_name] = attr_values

    def append_attributes(self, attr_names, db):
        """"""
        for i in attr_names:
            self.append_attribute(i, db.get_attributes([i]).get_db())

    def delete_objects(self, object_keys):
        """"""
        self.db = self.db.drop(object_keys, axis=0)

    def delete_attribute(self, attr_name):
        """"""
        if attr_name is not None:
            self.db = self.db.drop([attr_name], axis=1)

    def get_value(self, key, attr_name):
        """"""
        return self.db.at[key, attr_name]
    
    def rename(self, mapper, axis):
        """"""
        self.db = self.db.rename(mapper, axis=axis)

    def change_value(self, key, attr_name, new_value):
        """"""
        temp = self.get_value(key, attr_name)
        self.db[attr_name].loc[key] = new_value
        return temp

    def get_objects(self, keys):
        """"""
        k = self.db.loc[keys, :]
        return DataBase(k)

    def get_objects_exclusive(self, keys):
        """"""
        k = self.db.drop(keys, axis=0)
        return DataBase(k)

    def get_attributes(self, attr_names):
        """"""
        k = self.db[attr_names]
        return DataBase(k)

    def get_attributes_exclusive(self, attr_names):
        """"""
        k = self.db.drop(attr_names, axis=1)
        return DataBase(k)

    def get_part(self, keys, attr_names):
        """"""
        if attr_names is None:
            return self.get_objects(keys)
        if keys is None:
            return self.get_attributes(attr_names)
        k = self.db[attr_names].loc[keys,:]
        return DataBase(k)

    def get_part_exclusive(self, keys, attr_names):
        """"""
        k = self.db.drop(attr_names, axis=1)
        a = k.drop(keys, axis=0)
        return DataBase(a)

    def get_name(self):
        return self.name

    def join(self, other, on, how):
        """"""
        db = DataFrame(self.db)
        if self.db.empty:
            return DataBase(other.get_db(), name=self.name)
        return DataBase(db.join(other.get_db(), on, how, lsuffix="_caller", rsuffix="_callee"))

    def empty(self):
        """"""
        return self.db.empty

    def store(self, filename):
        """"""
        path = '.\\Data\\'
        self.db.to_csv(path + filename + '.csv', index=True)

    def read(self, filename):
        """"""
        path = '.\\Data\\'
        self.db = read_csv(path + filename + '.csv', index_col=0)
#        print(self.db)
        

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
        
        
        self.tree = ttk.Treeview(self, columns=[i for i in atributes], height=15, 
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
        Reports()

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
            mb.showerror('Ошибка','Должен быть выбран объект')
        else:
            dp.parse("DELETE",[],[self.tree.item(self.tree.selection()[0])['text']])
            self.update_DB()
    
    def delete_atribute(self, Entries):
        dp.parse("DELETE",[dp.working_db.get_db().columns[i] for i in Entries],[])
        self.update_DB()
        
    
    def edit_object(self, Entries):
        for i,j in zip(dp.working_db.get_db().columns,Entries):
            dp.parse("CHANGE", i, self.tree.item(self.tree.selection()[0])['text'],str(j.get()))
        self.tree.focus_set()
        self.update_DB()
    
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
        
        for i,j in zip([i for i in range(len(self.Checkbuttons))], self.Checkbuttons):
            j.grid(row=i,column=2, pady=3, padx=20, sticky='w')
                         
        
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
        self.dataframe = self.view.dp.working_db.get_db()
        self.attributes = list(self.dataframe.keys())
        self.v_attrs = [str(attr) for attr in self.attributes if self.isValAttr(str(attr))]
        self.q_attrs = [str(attr) for attr in self.attributes if not attr in self.v_attrs]
        self.figure=plt.Figure(figsize=(5,4),dpi=75)
        self.ax= self.figure.add_subplot(111)

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
        self.resizable(False, False)
        self.plot_area_frame = tk.LabelFrame(self, text='Plot Area')
        self.plot_area_frame.place(x=500,y=10,height=500,width=450)

        self.settings_area_frame = tk.LabelFrame(self,text='Settings Area')
        self.settings_area_frame.place(x=100,y=10,height=500,width=350)

#        self.menu = tk.Menu(self)
#        new_item = tk.Menu(self.menu, tearoff=0)
#        new_item.add_command(label='Новый')
#        new_item.add_separator()
#        new_item.add_command(label='Изменить')
#        self.menu.add_cascade(label='Файл', menu=new_item)

        self.btn_save = ttk.Button(self, text='Сохранить', command=self.save_report)
        self.btn_save.place(x=250, y=265)

        self.combo = ttk.Combobox(self.settings_area_frame)
        lbl = tk.Label(self.settings_area_frame ,text='Выберите вид отчета:')
        lbl.place(x=10,y=6,width=150)
        self.combo['values'] = ("Столбчатая диаграмма(кач-кач)","Гистограмма(кол-кач)", "Диаграмма Бокса-Вискера(кол-кач)","Диаграмма рассеивания(2 кол - кач)", "Сводная таблица (кач-кач)", "Набор осн. опис. стат")
        self.combo.current(0)
        self.combo.place(x=10,y=30)

        self.choose_btn = ttk.Button(self.settings_area_frame, text='Выбрать',command=self.click)
        self.choose_btn.place(x=230, y=30)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=340, y=265)
        self.btn_cancel.bind('<Button-1>', lambda event: self.view.destroy_links())
        
        self.grab_set()
        self.focus_set()

    def paint_figure(self):

        canvas = FigureCanvasTkAgg(self.figure , master=self.plot_area_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=20,y=10,height=450,width=400)

    def click(self):
        if self.combo.get()=="Диаграмма рассеивания(2 кол - кач)":
            self.first_combo = ttk.Combobox(self.settings_area_frame)
            lbl1 = tk.Label(self.settings_area_frame, text="Выберите количественный атрибут")
            lbl1.place(x=10, y=50, height=20, width=200)
            self.first_combo['values']=self.v_attrs
            self.first_combo.current(0)
            self.first_combo.place(x=10,y=73, height=20, width=200)
            lbl2 = tk.Label(self.settings_area_frame, text="Выберите количественный атрибут")
            lbl2.place(x=10, y=93, height=20, width=200)
            self.second_combo = ttk.Combobox(self.settings_area_frame)
            self.second_combo['values']=self.v_attrs
            self.second_combo.current(0)
            self.second_combo.place(x=10,y=116, height=20,width=200)
            btn2 = ttk.Button(self.settings_area_frame, text='Построить',command=self.Buildscatter)
            btn2.place(x=230, y=73)
            self.third_combo = ttk.Combobox(self.settings_area_frame)
            lbl3 = tk.Label(self.settings_area_frame, text="Выберите качественный атрибут")
            lbl3.place(x=10, y=136, height=20, width=200)
            self.third_combo['values']=self.q_attrs
            self.third_combo.current(0)
            self.third_combo.place(x=10,y=159, height=20,width=200)
        if self.combo.get()=="Столбчатая диаграмма(кач-кач)":
            self.third_combo = ttk.Combobox(self.settings_area_frame)
            self.first_combo = ttk.Combobox(self.settings_area_frame)
            lbl1 = tk.Label(self.settings_area_frame, text="Выберите качественный атрибут")
            lbl1.place(x=10, y=50, height=20, width=200)
            self.first_combo['values']=self.q_attrs
            self.first_combo.current(0)
            self.first_combo.place(x=10,y=73, height=20, width=200)
            lbl2 = tk.Label(self.settings_area_frame, text="Выберите качественный атрибут")
            lbl2.place(x=10, y=93, height=20, width=200)
            self.second_combo = ttk.Combobox(self.settings_area_frame)
            self.second_combo['values']=self.q_attrs
            self.second_combo.current(0)
            self.second_combo.place(x=10,y=116, height=20,width=200)
            btn2 = ttk.Button(self.settings_area_frame, text='Построить',command=self.Buildbar)
            btn2.place(x=230, y=73)
            self.third_combo = ttk.Combobox(self.settings_area_frame)
            lbl3 = tk.Label(self.settings_area_frame, text="Выберите качественный атрибут")
            lbl3.place(x=10, y=136, height=20, width=200)
            self.third_combo['values']=self.q_attrs
            self.third_combo.current(0)
            self.third_combo.place(x=10,y=159, height=20,width=200)
            lbl3.destroy()
            self.third_combo.destroy()
        if self.combo.get()=="Гистограмма(кол-кач)":
            self.first_combo = ttk.Combobox(self.settings_area_frame)
            lbl1 = tk.Label(self.settings_area_frame, text="Выберите количественный атрибут")
            lbl1.place(x=10, y=50, height=20, width=200)
            self.first_combo['values']=self.v_attrs
            self.first_combo.current(0)
            self.first_combo.place(x=10,y=73, height=20, width=200)
            lbl2 = tk.Label(self.settings_area_frame, text="Выберите качественный атрибут")
            lbl2.place(x=10, y=93, height=20, width=200)
            self.second_combo = ttk.Combobox(self.settings_area_frame)
            self.second_combo['values']=self.q_attrs
            self.second_combo.current(0)
            self.second_combo.place(x=10,y=116, height=20,width=200)
            btn2 = ttk.Button(self.settings_area_frame, text='Построить',command=self.Buildhist)
            btn2.place(x=230, y=73)
#            self.third_combo = ttk.Combobox(self.settings_area_frame)
#            lbl3 = tk.Label(self.settings_area_frame, text="Выберите качественный атрибут")
#            lbl3.place(x=10, y=136, height=20, width=200)
#            self.third_combo['values']=self.q_attrs
#            self.third_combo.current(0)
#            self.third_combo.place(x=10,y=159, height=20,width=200)
#            lbl3.place_forget()
#            self.third_combo.place_forget()
            
        if self.combo.get()=="Диаграмма Бокса-Вискера(кол-кач)":
            self.first_combo = ttk.Combobox(self.settings_area_frame)
            lbl1 = tk.Label(self.settings_area_frame, text="Выберите количественный атрибут")
            lbl1.place(x=10, y=50, height=20, width=200)
            self.first_combo['values']=self.v_attrs
            self.first_combo.current(0)
            self.first_combo.place(x=10,y=73, height=20, width=200)
            lbl2 = tk.Label(self.settings_area_frame, text="Выберите качественный атрибут")
            lbl2.place(x=10, y=93, height=20, width=200)
            self.second_combo = ttk.Combobox(self.settings_area_frame, values=self.q_attrs)
            self.second_combo.current(0)
            self.second_combo.place(x=10,y=116, height=20,width=200)
            btn2 = ttk.Button(self.settings_area_frame, text='Построить',command=self.Buildbox)
            btn2.place(x=230, y=73)
            self.third_combo = ttk.Combobox(self.settings_area_frame, values=self.q_attrs)
            lbl3 = tk.Label(self.settings_area_frame, text="Выберите качественный атрибут")
            lbl3.place(x=10, y=136, height=20, width=200)
            self.third_combo.current(0)
            self.third_combo.place(x=10,y=159, height=20,width=200)
            lbl3.place_forget()
            self.third_combo.place_forget()

    def Buildbar(self):
        data = (20, 35, 37 ,39 ,40)
        ind = np.arange(5)
        width= .5
        self.ax.clear()
        rects = self.ax.bar(ind, data, width)

        self.paint_figure()

    def Buildhist(self):
#        first_attr = self.first_combo.get()
#        second_attr = self.second_combo.get()
#
#        data = (20, 35, 37 ,39 ,40)
#
#        ind = np.arange(5)
#        width= .5
#        self.ax.clear()
#        rects = self.ax.h
        
        self.dataframe.plot.hist(bins=3)
        self.paint_figure()

    def Buildbox(self):
        data = (20, 0, 37 ,39 ,40)

        ind = np.arange(5)
        width= .5
        self.ax.clear()
        rects = self.ax.boxplot((20, 35, 37 ,39 ,40),(20, 35, 37 ,39 ,40))
        self.paint_figure()

    def Buildscatter(self):
        first_attr = self.first_combo.get()
        second_attr = self.second_combo.get()
        third_attr = self.third_combo.get()
        step_size = 3/len(self.q_attrs)
        color = [0,0,0]
        s = list(set(self.dataframe[third_attr].values))
        colormap = {s[i] : i for i in range(len(s))}
        colors = [colormap[element] for element in self.dataframe[third_attr].values]
        print(colors)

        ind = np.arange(5)
        width= .5
        self.ax.clear()
        #rects = self.ax.bar(ind, data, width)
        self.dataframe.plot.scatter(ax=self.ax, x=first_attr, y=second_attr, c=colors, colormap='viridis')
        self.paint_figure()

    def save_report(self):

        pass

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
    root.geometry("650x345+300+200")
    root.resizable(False, False)
    root.mainloop()
