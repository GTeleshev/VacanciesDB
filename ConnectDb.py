import os
import sqlite3

connname = 'vacancies.db'


# CREATE TABLE "vacancies" (
#     "id"	INTEGER,
# "NAME"	TEXT,
# "SKILLS"	TEXT,
# "DESCRIPTION"	TEXT,
# "SALARY"	TEXT,
# "TYPE"	INTEGER,
# PRIMARY KEY("id" AUTOINCREMENT)
# )

class ConnectDb:
    def __init__(self, name_file='vacancies.db'):
        self.connstring = f'{name_file}'
        self.all_data = self.select_all_db()
        self.all_data_dict = self.from_sql_to_dict()

    def select_all_db(self):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        data = cursor.execute('''SELECT * FROM VACANCIES''')
        cursor.close()
        conn.close()
        return data

    def clear_db(self):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM VACANCIES;''')
        conn.commit()
        conn.close()

    def insert_in_db(self, name, skills, description, salary, type):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        dbstring = f'''INSERT INTO VACANCIES (NAME, SKILLS, DESCRIPTION, SALARY, TYPE) VALUES 
                ('{name}', '{skills}', '{description}', '{salary}', '{type}')'''
        cursor.execute(dbstring)
        conn.commit()
        conn.close()

    # from_sql_to_dict (former)

    def from_sql_to_dict(self):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        data = cursor.execute('''SELECT * FROM VACANCIES''')
        res = {}
        for id, row in enumerate(data):
            res[id] = {
                'name': row[1],
                'skills': row[2],
                'description': row[3],
                'salary': row[4],
                'type': row[5]
            }
        conn.close()
        return res

    def select_where(self, column, value):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        data = cursor.execute(f"""SELECT * FROM VACANCIES WHERE {column} = '{value}'""")
        conn.close()
        return data

    def select_where_like(self, column, value):
        conn = sqlite3.connect(self.connstring)
        cursor = conn.cursor()
        data = cursor.execute(f"""SELECT * FROM VACANCIES WHERE {column} LIKE '%{value}%'""")
        conn.close()
        return data

    def finish(self, data_dict):
        self.clear_db()
        for key, value in data_dict.items():
            self.insert_in_db(value["NAME"], value["SKILLS"], value["DESCRIPTION"], value["SALARY"], value["TYPE"])
