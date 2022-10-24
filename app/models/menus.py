from flask import current_app as app


class Menus:
    def __init__(self, uid, name, time_made, summary):
        #self.id = id
        self.uid = uid
        self.name = name
        self.date = time_made
        self.summary = summary

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, name, time_made, summary
FROM Menus
WHERE uid = :uid
''',
                              uid=uid)
        return Menus(*(rows[0])) if rows else None

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