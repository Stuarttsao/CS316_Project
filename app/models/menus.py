from flask import current_app as app


class Menus:
    def __init__(self, uid, name, time_made, summary):
        #self.id = id
        self.uid = uid
        self.name = name
        self.date = time_made
        self.summary = summary

    @staticmethod
    def uids():
        ret = app.db.execute('''
SELECT uid
FROM Menus
        ''')
        return set([entry[0] for entry in ret])

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, name, time_made, summary
FROM Menus
WHERE uid = :uid
''',
                              uid=uid)
        return [Menus(*row) for row in rows] if rows else None

    @staticmethod
    def get_by_name(name):
        rows = app.db.execute('''
SELECT uid, name, time_made, summary
FROM Menus
WHERE name = :name
''',
                              name=name)
        return [Menus(*row) for row in rows] if rows else None

    @staticmethod
    def get_most_recent(uid):
        rows = app.db.execute('''
SELECT uid, name, time_made, summary
FROM Menus
WHERE uid = :uid
ORDER BY time_made DESC
''',
                              uid=uid)
        print("rows:",rows) #remember to enforce uniqueness
        return [Menus(*row) for row in rows]
    
    def insert(self):
        app.db.execute('''
        INSERT INTO Menus (uid, name, time_made, summary)
        VALUES (:uid, :name, :time_made, :summary)
        ''',
                                 uid=self.uid,
                                 name=self.name,
                                 time_made=self.date,
                                 summary = self.summary
                                )
        return

    def insert_drink(uid, menuName, did):
        try:
            app.db.execute('''
            INSERT INTO MenuDrinks (uid, menuName, did)
            VALUES (:uid, :menuName, :did)
            ''',
                                    uid=uid,
                                    menuName=menuName,
                                    did=did,
                                    )
        except:
            return False
        return True
    
    def get_menudrinks(uid, menuName):
        drinks = app.db.execute('''
SELECT did
FROM MenuDrinks
WHERE uid = :uid AND menuName = :name
''',
                              uid=uid, name=menuName)
        print(drinks)
        return [drink[0] for drink in drinks]