from flask import current_app as app

class Components:
    def __init__(self, did, iid, amount, unit):
        self.did = did
        self.iid = iid
        self.amount = amount
        self.unit = unit

    @staticmethod
    def get_by_did(did):
        rows = app.db.execute(''' SELECT DISTINCT did, components.iid, amount, unit, ingredients.name FROM components, ingredients WHERE did = :did AND components.iid = ingredients.iid''', did=did)
        print("rows", rows)
        return rows

    @staticmethod
    def get_ingredients(did):
        rows = app.db.execute(''' SELECT DISTINCT did, components.iid, amount, unit, ingredients.name 
        FROM components, ingredients WHERE did = :did AND components.iid = ingredients.iid''', did=did)
        print("rows", rows)
        return rows

    @staticmethod
    def get_by_iid(iid):
        rows = app.db.execute(''' SELECT did, iid, amount, unit FROM components WHERE iid = :iid ''', iid=iid)
        return [Components(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute(''' SELECT did, iid, amount, unit FROM components ''')
        return [Components(*row) for row in rows]

    
    @staticmethod
    def remove_all_by_did(did):
        app.db.execute(''' DELETE FROM components WHERE did = :did ''', did=did)

    @staticmethod
    def update_by_did(did, iid, amount, unit):
        app.db.execute(''' UPDATE components SET iid = :iid, amount = :amount, unit = :unit WHERE did = :did ''', iid=iid, amount=amount, unit=unit, did=did)

    @staticmethod
    def insert(did, iid, amount, unit):
        app.db.execute(''' INSERT INTO components (did, iid, amount, unit) VALUES (:did, :iid, :amount, :unit) ''',
                        did=did,
                        iid=iid,
                        amount=amount,
                        unit=unit)
    
    def insert(self):
        app.db.execute(''' INSERT INTO components (did, iid, amount, unit) VALUES (:did, :iid, :amount, :unit) ''',
                        did=self.did,
                        iid=self.iid,
                        amount=self.amount,
                        unit=self.unit)
    
    
    