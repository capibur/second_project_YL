import sqlite3


class DBManager:
    def __init__(self, name):
        self.name = name

    def set_saves(self, location, inventory: list, save_name, morders,score):
        self.request(f"""
        INSERT INTO save_list ( location, save_date, save_name, morders, score)
        VALUES ("{location}", date('now','localtime'), "{save_name}"), {morders}, {score};""")
        for thing in inventory:
            self.request(f"""
                    INSERT INTO in_game (name, save)
                    VALUES ("{thing.get_name(thing)}", "{save_name}");""")

    def get_saves(self, save_name, mode=False):  # при mode = true возвращается словарь с характеристиками
        inventory = [i[0] for i in self.request(f"""               
        SELECT name FROM in_game WHERE save = "{save_name}"
        """)]
        location = self.request(f"""               
        SELECT location FROM save_list WHERE save_name = "{save_name}"
        """)[0][0]
        if not mode:
            return inventory, location
        else:
            print(inventory)
            return self.get_spec(inventory), location

    def get_spec(self, thing_names):  # возвращает характеристики
        res = dict()
        for i in thing_names:
            date_thing = self.request(f"""               
                    SELECT * FROM things WHERE name = "{i}"
                    """)
            print(date_thing)
            if date_thing:
                res[date_thing[0][1]] = {"dmg": date_thing[0][2], "prt": date_thing[0][2], "descr": date_thing[0][2]}
        return res

    def get_records(self):
        records_dict = dict()
        records_list = self.request(f""" SELECT * FROM record_list""")
        for i in records_list:
            records_dict[i[1]] = {"murders": i[2], "score": i[3]}
        print(records_dict)

    def set_records(self, score, murders, n):
        self.request(f"""
        INSERT INTO record_list(name, murders, score)
        VALUES("{n}", {murders}, {score})
                    """)

    def complete(self, achievement):
        self.request(f"""UPDATE achievement_list SET achieved = 0 WHERE name = "{achievement}" """)

    def get_img(self, thing_name):
        try:
            return self.request(f"""               
                    SELECT * FROM things WHERE name = "{thing_name}"
                    """)[0][0]
        except IndexError:
            print(f"Предмет {thing_name} не имеет текстуры")

    def request(self, txt):
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        res = cur.execute(txt).fetchall()
        con.commit()
        con.close()
        return res


