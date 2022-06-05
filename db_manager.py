import sqlite3


class DBManager:
    def __init__(self, name):
        self.name = name

    def set_saves(self, location, inventory: list, save_name, murders,score, player_name):
        self.request(f"""
        INSERT INTO save_list ( location, save_date, save_name, murders, score,player_name)
        VALUES ("{location}", date('now','localtime'), "{save_name}", {murders}, {score}, "{player_name}")""")
        if inventory:
            for thing in inventory:
                self.request(f"""
                        INSERT INTO in_game (name, save)
                        VALUES ("{thing.get_name(thing)}", "{save_name}");""")
    def append_thing(self, thing, save_name):
        self.request(f"""INSERT INTO in_game (name, save)
                         VALUES ("{thing}", "{save_name}");
                     """)

    def get_saves(self, save_name, mode=False):  # при mode = true возвращается словарь с характеристиками
        if save_name:
            print(f'{save_name}         fcedfc vedf')
            inventory = [i[0] for i in self.request(f"""               
            SELECT name FROM in_game WHERE save = "{save_name}"
            """)]
            name = self.request(f"""               
            SELECT player_name FROM save_list WHERE save_name = "{save_name}"
            """)[0][0]
            location = self.request(f"""               
            SELECT location FROM save_list WHERE save_name = "{save_name}"
            """)[0][0]

            if not mode:
                return  inventory, location, name
            else:
                print(inventory)
                return self.get_spec(inventory), location

    def get_spec(self, thing_names):  # возвращает характеристики
        res = {"dmg": 0, "prt": 0, "descr": 0}
        date_thing = self.request(f"""               
                SELECT * FROM things WHERE name = "{thing_names}"
                """)
        print(date_thing)
        if date_thing:
            res = {"dmg": date_thing[0][2], "prt": date_thing[0][2], "descr": date_thing[0][2]}
        return res

    def get_records(self, name=False):
        records_dict = dict()
        records_list = self.request(f""" SELECT * FROM record_list""")
        for i in records_list:
            records_dict[i[1]] = {"murders": i[2], "score": i[3]}
        print(records_dict)

    def set_records(self, score, murders, n):
        self.request(f"""
        INSERT INTO record_list(name, murders, score)
        VALUES("{n}", {murders}, {score})""")
    def update_records(self, score, murders, n):
        self.request(f"""UPDATE record_list SET score = {score}, murders = {murders}  WHERE name = "{n}" """)

    def complete(self, achievement):
        self.request(f"""UPDATE achievement_list SET achieved = 1 WHERE name = "{achievement}" """)

    def get_img(self, thing_name):
        try:
            return self.request(f"""               
                    SELECT img FROM things WHERE name = "{thing_name}"
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


