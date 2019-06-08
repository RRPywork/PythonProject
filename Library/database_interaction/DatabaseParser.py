"""
Содержит обработчик запросов к базе данных.
Задача: искоренить влияние Pandas (по возможности) из потока данных. Поток данных не должен от него зависеть.
Вполне возможно (и так действительно может получиться!), обработчики и GUI будут частично зависеть от Pandas,
(используем Pandas как обертку для MatPlotLib) но потоку не должно быть никакого дела до передаваемых по нему объектов.
Author: Vitaly(Admin)
Автор: Балескин
"""
from Work.Library.DataBase import DataBase
from Work.Library.DataFlow.DBInterface import DBInterface


class DatabaseParser(DBInterface):
    """
    Обработчик БД, множества БД, сессионной БД и запросов к оным
    Автор: Балескин
    """

    def __init__(self, names, paths, hints=None):
        """
        Конструктор. Добывает БД из файлов csv. Вход - имена справочников, словарь имя справочника:путь к нему, подсказки для слияния
        и помещает их в словарь отношение:БД Автор: Балескин
        """
        assert len(names) == len(paths)
        self.its_dbs = {i: DataBase() for i in names}
        if hints is not None:
            self.hints = {i: hints[i] for i in names}
        for i in names:
            self.its_dbs[i].read(paths[i])
        self.attr_names = {names[i]: self.its_dbs[names[i]].get_attr_names() for i in range(len(names))}
        self.working_db = DataBase()

    def inclusive_attr_display(self, attr_names):
        """
        отобразить все атрибуты из списка в сессионной бд Автор - Балескин
        вход - имена атрибутов
        """
        excl_attr_names = []
        for attrs in self.attr_names.values():
            for attr in attrs:
                if attr not in attr_names:
                    excl_attr_names.append(attr)
        self.exclusive_attr_display(excl_attr_names)

    def inclusive_obj_display(self, obj_names):
        """Отобразить все объекты из списка на сессионную БД Автор - Балескин
        вхд - имена объектов"""
        self.working_db = self.working_db.get_objects(obj_names)

    def exclusive_attr_display(self, attr_names):
        """Отобразить все атрибуты кроме указанных в списке Автор - Балескин
        Вход - имена атрибутов"""
        self.working_db = DataBase()
        for (name, db) in self.its_dbs.items():
            a = self.working_db.join(db, on=self.hints[name] if self.hints[name] != '-' else None, how='left')
            self.working_db = a
        if attr_names is not None:
            for attr in attr_names:
                self.working_db.delete_attribute(attr)
        self.working_db = DataBase(self.working_db.get_db().drop_duplicates())
        self.working_db = DataBase(self.working_db.get_db().groupby(self.working_db.get_db().index).first())

    def exclusive_obj_display(self, obj_names):
        """Отобразить все объекты, кроме указанных Автр - Балескин
        Вход - список объектов"""
        self.working_db.delete_objects(obj_names)

    def parse(self, q_type, *pargs):
        """
        Автор - Балескин
        Метод, отвечающий за обработку.
        Выполняет выбор типа операции в зависимости от аргументов (в частности, первого) и делегирует частным случаям.
        Первый аргумент - тип запроса
        Второй - условия
        Итого:
        query -> query_type args
        query_type -> DISPLAY | ADD | DROP | APPEND | DELETE | STORE | CHANGE | RENAME | LOAD
        args -> attr_list obj_list conditions |
                names path_names hints|
                names |
                _names _names values name|
                _names _names values|
                pathname|
                obj_name attr_name value|
                dictionary, axis|
                name
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
            if attr_key is not None:
                if attr_key == '-i':
                    self.inclusive_attr_display(attr_names)
                elif attr_key == '-e':
                    self.exclusive_attr_display(attr_names)
            if obj_key is not None:
                if obj_key == '-i':
                    self.inclusive_obj_display(obj_names)
                elif obj_key == '-e':
                    self.exclusive_obj_display(obj_names)
            if conditions is not None:
                for cond in conditions:
                    cond._process(self.working_db)

        elif q_type == 'ADD':
            names = pargs[0]
            path_names = pargs[1]
            hints = pargs[2]
            for (name, hint) in hints.items():
                self.hints[name] = hint
            for i in range(len(names)):
                db = DataBase()
                db.read(path_names[i])
                self.its_dbs[names[i]] = db
            self.attr_names = {i: self.its_dbs[i].get_attr_names() for i in self.its_dbs.keys()}

        elif q_type == 'DROP':
            names = pargs[0]
            for name in names:
                del self.its_dbs[name]
            self.attr_names = {i: self.its_dbs[i].get_attr_names() for i in self.its_dbs.keys()}
        elif q_type == 'APPEND':
            attr_names = pargs[0]
            obj_names = pargs[1]
            obj_values = pargs[2]
            name = pargs[3]
            if name is not None:
                self.working_db.join(self.its_dbs[name].get_attributes(attr_names), on=None, how='inner')
            else:
                global_failure = False
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
        elif q_type == 'LOAD':
            self.working_db.read(pargs[0])
        pass
