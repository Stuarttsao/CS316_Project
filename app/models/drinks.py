from flask import current_app as app

class Drinks:
    def __init__(self, did, name, category, instructions, picture):
        self.did = did
        self.name = name
        self.category = category
        self.instructions = instructions
        self.picture = picture

    @staticmethod
    def get_by_did(did):
        rows = app.db.execute('''
SELECT did, name, category, instructions, picture
FROM Drinks
WHERE did = :did
''',
                              did=did)
        return [Drinks(*row) for row in rows]

    @staticmethod
    def get_by_name(name):
        rows = app.db.execute('''
SELECT did, name, category, instructions, picture
FROM Drinks
WHERE name = :name
''',
                              name=name)
        print("rows", rows)
        return [Drinks(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT did, name, category, instructions, picture
FROM Drinks
''')
        return [Drinks(*row) for row in rows]

    @staticmethod
    def get_by_category(category):
        rows = app.db.execute('''
SELECT did, name, category, instructions, picture
FROM Drinks
WHERE category = :category
''',
                              category=category)
        print("rows", rows)
        print(rows)
        return [Drinks(*row) for row in rows]

    @staticmethod
    def get_by_instructions(instructions):
        rows = app.db.execute('''
SELECT did, name, category, instructions, picture
FROM Drinks
WHERE instructions = :instructions
''',
                              instructions=instructions)
        return Drinks(*(rows[0])) if rows else None


    @staticmethod
    def get_drinks_by_ingredientName(ingredientName):
        rows = app.db.execute('''
SELECT Drinks.did, Drinks.name, Drinks.category, Drinks.instructions, Drinks.picture
FROM Drinks, Ingredients, Components
WHERE Ingredients.name = :ingredientName AND Ingredients.iid = Components.iid AND Components.did = Drinks.did
''',
                                ingredientName=ingredientName)
        return [Drinks(*row) for row in rows]





    def update(self, instructions):
        app.db.execute(''' 
        UPDATE Drinks 
        SET did = :did, name = :name, category = :category, instructions = :instructions, picture = :picture
        WHERE did = :did ''', 
        did=self.did, name=self.name, category=self.category, instructions=instructions, picture=self.picture)

    def save(self):
        if self.did:
            self.update()
        else:
            self.insert()

    def insert(self):
        try:
            self.did = app.db.execute('''
            INSERT INTO Drinks (name, category, instructions, picture)
            VALUES (:name, :category, :instructions, :picture)
            ''',
                                 name=self.name,
                                 category=self.category,
                                 instructions=self.instructions,
                               picture=self.picture)
        except:
            return False
        return True