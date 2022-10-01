import sqlite3

class Bd:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('data.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS admins(
                    id INTEGER PRIMARY KEY,
                    name TEXT);
                """)
        self.conn.commit()

    def add_admin(self, tid, name):
        par = (tid, name)
        try:
            self.cur.execute("INSERT INTO admins VALUES(?, ?);", par)
            self.conn.commit()
            return 'Ок'
        except sqlite3.IntegrityError:
            return "пользователь уже есть"
        
    def chek(self, ids):
        admins = self.get_admins()
        flag = False
        for admin in admins:
            if str(admin[0]) == str(ids) or str(187756771) == str(ids) or str(1096174342) == str(ids): 
                flag = True
        return flag

    def get_one_admin(self, ids):
        return list(self.cur.execute("SELECT * FROM admins WHERE (id={});".format(ids)))

    def del_admin(self, ids):
        self.cur.execute("DELETE FROM admins WHERE (id={});".format(ids))
        self.conn.commit()

    def get_admins(self):
        return list(self.cur.execute("""SELECT * FROM admins"""))
