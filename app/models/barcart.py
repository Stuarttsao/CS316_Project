from flask import current_app as app


class BarCart:
    """
    This is just a TEMPLATE for Cart, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, did, times_made):
        self.uid = uid
        self.did = did
        self.times_made = times_made

    @staticmethod
    def get_drinks_in_cart(uid):
        rows = app.db.execute('''
        SELECT uid, did, times_made
        FROM barCart
        WHERE uid = :uid
        ORDER BY times_made DESC
        ''',
                              uid=uid)
        return [BarCart(*row) for row in rows] if rows else None

    @staticmethod
    def get_most_made(uid):
        rows = app.db.execute('''
        SELECT uid, did, times_made
        FROM barCart
        WHERE uid = :uid
        ORDER BY times_made DESC
        LIMIT 5
        ''',
                              uid=uid)
        return [BarCart(*row) for row in rows] if rows else None

    def update(self, times_made):
        app.db.execute(''' UPDATE barCart SET uid = :uid, did = :did, times_made = times_made + :times_made WHERE did = :did ''', uid=self.uid, did=self.did, times_made=times_made)

    def insert(self):
        try:
            app.db.execute('''
            INSERT INTO barCart (uid, did, times_made)
            VALUES (:uid, :did, :times_made)
            ''',
                                    uid=self.uid,
                                    did=self.did,
                                    times_made=self.times_made,
                                    )
        except:
            self.update(self.times_made)

    @staticmethod
    def remove_drink(uid, did):
        app.db.execute(''' DELETE FROM Cart WHERE uid = :uid AND did = :did ''',
                          uid=uid,
                          did=did)  
    