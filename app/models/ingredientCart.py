from flask import current_app as app


class IngredientCart:
    def __init__(self, uid, iid, amount, unit):
        self.uid = uid
        self.iid = iid
        self.amount = amount
        self.unit = unit

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT uid, ingredientCart.iid, amount, unit, ingredients.name
FROM ingredientCart, ingredients
WHERE uid = :uid AND ingredientCart.iid = ingredients.iid
''',
                              uid=uid)
        return rows


    @staticmethod
    def remove_all_by_uid(uid):
        app.db.execute(''' DELETE FROM ingredientCart WHERE uid = :uid ''',
                          uid=uid)  

    

    @staticmethod
    def search_by_cart(ingredients):

        app.db.execute(''' CREATE TABLE temp AS
                SELECT did, iid
                FROM components
                WHERE iid = :ingredient
                ''', ingredient=ingredients[0])


        for ingredient in ingredients[1:]:
            print(ingredient)
            app.db.execute('''
                INSERT INTO temp
                (SELECT did, iid
                FROM components
                WHERE iid = :ingredient)
                ''', ingredient=ingredient)

        test = app.db.execute('''
            SELECT did, iid
            FROM temp
            ''')
        print(test)

        rows = app.db.execute(''' 
        WITH total AS (
            Select did, COUNT(iid) as count
            FROM components
            GROUP BY did
        ),
        total2 AS (
            Select did, COUNT(iid) as count
            FROM temp
            GROUP BY did
        )
        SELECT drinks.name
        FROM drinks, total2, total
        WHERE total2.did = total.did AND total2.count = total.count AND total2.did = drinks.did
        ''')

        print(rows)
        app.db.execute(''' DROP TABLE temp ''')
        return rows


    def insert(self):
        app.db.execute(''' INSERT INTO ingredientCart (uid, iid, amount, unit)
                            VALUES (:uid, :iid, :amount, :unit) ''',
                            uid=self.uid,
                            iid=self.iid,
                            amount=self.amount,
                            unit=self.unit)



    
