from flask import current_app as app

class Recommendations:
    # list of recommended drinks
    def __init__(self, did, name, category, picture, score):
        self.did = did
        self.name = name
        self.category = category
        self.picture = picture
        self.score = score

    # On the drink page, output 5 drinks that share some ingredients
    @staticmethod
    def you_may_also_like(did):
        rows = app.db.execute('''
SELECT did, name, category, instructions, picture
FROM Drinks
WHERE did = :did
''',
                              did=did)
        return Recommendations(*(rows[0])) if rows else None

    @staticmethod
    def get_top_drinks():
        rows = app.db.execute('''
SELECT did, name, category, instructions, picture
FROM Drinks
WHERE did = :did
''',
                              did=did)
        return Recommendations(*(rows[0])) if rows else None

    @staticmethod
    def get_top_drinks_in_category(category):
        rows = app.db.execute('''
SELECT did, name, category, instructions, picture
FROM Drinks
WHERE did = :did
''',
                              did=did)
        return Recommendations(*(rows[0])) if rows else None


