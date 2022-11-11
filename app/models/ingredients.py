from flask import current_app as app

class Ingredients:
    def __init__(self, name, category, instructions, picture):
        # drink characteristics
        self.name = name
        self.category = category
        self.instructions = instructions
        self.picture = picture

    @staticmethod
    # search drinks by ingredients list
    def get_by_ingredient(name):
        rows = app.db.execute('''
            SELECT DISTINCT d.name, d.category, d.instructions, d.picture
            FROM Components c, Drinks d, Ingredients i
            WHERE i.name = :name and c.iid = i.iid and d.did = c.did
            ''',
                              name=name)
        return [Ingredients(*row) for row in rows]
