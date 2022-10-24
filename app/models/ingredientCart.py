from flask import current_app as app


class IngredientCart:
    """
    This is just a TEMPLATE for Cart, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
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
        return [ingredientCart(*row) for row in rows]
