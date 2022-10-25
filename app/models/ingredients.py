from flask import current_app as app

class Ingredients:
    def __init__(self, iid, name):
        self.iid = iid
        self.name = name
        

    @staticmethod
    def get_by_ingredient(name):
        rows = app.db.execute('''
SELECT DISTINCT i.name, d.name 
FROM Components c, Drinks d, Ingredients i
WHERE i.name = :name and c.iid = i.iid and d.did = c.did
''',
                              name=name)
        return [Ingredients(*row) for row in rows]
