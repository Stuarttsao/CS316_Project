from flask import current_app as app

class Bartender:
    def __init__(self, uid, did):
        self.uid = uid
        self.did = did

    @staticmethod
    def get(uid, did):
        rows = app.db.execute('''
        SELECT uid, did
        FROM Bartender
        WHERE uid = :uid AND did = :did
        ''',
                              uid=uid,
                              did = did)
        return Bartender(*(rows[0])) if rows else None

    @staticmethod
    def get_by_did(did):
        rows = app.db.execute('''
        SELECT uid, did
        FROM Bartender
        WHERE did = :did
        ''',
                              did = did)
        return Bartender(*(rows[0])) if rows else None

    @staticmethod
    def get_all(uid):
        rows = app.db.execute('''
        SELECT uid, did
        FROM Bartender
        WHERE uid = :uid
        ''', uid=uid)
        return [Bartender(*row) for row in rows]

    def save(self):
        if self.did:
            self.update()
        else:
            self.insert()

    def insert(self):
        try:
            self.did = app.db.execute('''
            INSERT INTO Bartender (uid, did)
            VALUES (:uid, :did)
            ''',
                                 uid=self.uid,
                                 did=self.did)
        except:
            return False
        return True