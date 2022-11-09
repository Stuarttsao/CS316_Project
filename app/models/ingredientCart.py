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
SELECT uid, iid, amount, unit
FROM ingredientCart
WHERE uid = :uid
''',
                              uid=uid)
        return [IngredientCart(*row) for row in rows]


    @staticmethod
    def remove_all_by_uid(uid):
        app.db.execute(''' DELETE FROM ingredientCart WHERE uid = :uid ''',
                          uid=uid)  

    def insert(self):
        app.db.execute(''' INSERT INTO ingredientCart (uid, iid, amount, unit)
                            VALUES (:uid, :iid, :amount, :unit) ''',
                            uid=self.uid,
                            iid=self.iid,
                            amount=self.amount,
                            unit=self.unit)



    
