import sqlite3
import json


class Menu:
    def __init__(self, id, date, desc):
        self.id = id
        self.date = date
        self.desc = desc

    def to_dict(self):
        return {"id": self.id, "date": self.date, "desc": self.desc}


class MenuRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        sql = """
            CREATE table if not exists menus (
                id varchar,
                date varchar,
                desc varchar
            )
        """

        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def get_all(self):
        sql = """SELECT * FROM menus ORDER BY date desc"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        dict_menu = []
        for item in data:
            menu_class = Menu(
                id=item["id"], date=item["date"], desc=json.loads(item["desc"]))
            dict_menu.append(menu_class)
        return dict_menu

 # ---------------------------------------------------

    def get_by_id(self, id):
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM menus WHERE id =?""", (id,))
        data = cursor.fetchone()
        menu_class = Menu(
            id=data["id"], date=data["date"], desc=json.loads(data["desc"]))
        return menu_class

    def get_by_date(self, date):
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM menus WHERE date =?""", (date,))
        data = cursor.fetchone()
        menu_class = Menu(
            id=data["id"], date=data["date"], desc=json.loads(data["desc"]))
        return menu_class

    def save(self, menu):
        sql = """insert into menus (id,date, desc) values (
            :id,:date, :desc
        ) """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, menu.to_dict())
        conn.commit()