from flask import current_app as app

class Ingredients:
    def __init__(self, iid, name):
        self.iid = iid
        self.name = name

    @staticmethod
    def get_by_iid(iid):
        rows = app.db.execute('''
SELECT iid, name
FROM Ingredients
WHERE iid = :iid
''',

                                iid=iid)
        return Ingredients(*(rows[0])) if rows else None

    @staticmethod
    def get_by_name(name):
        rows = app.db.execute('''
SELECT iid, name
FROM Ingredients
WHERE name = :name
''',
                                name=name)
        return [Ingredients(*row) for row in rows]


        