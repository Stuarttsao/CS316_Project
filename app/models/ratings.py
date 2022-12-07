from flask import current_app as app


class Ratings:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, did, time_rated, score, descript, likes, dislikes):
        #self.id = id
        self.uid = uid
        self.did = did
        self.time_rated = time_rated
        self.score = score
        self.descript = descript
        self.likes = likes
        self.dislikes = dislikes

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, did, time_rated, score, descript, likes, dislikes
FROM Ratings
WHERE uid = :uid
''',
                              uid=uid)
        return Ratings(*rows) if rows else None

    @staticmethod
    def get_most_recent(uid):
        rows = app.db.execute('''
SELECT uid, did, time_rated, score, descript, likes, dislikes
FROM Ratings
WHERE uid = :uid
ORDER BY time_rated DESC
LIMIT 5
''',
                              uid=uid)
        print("rows:",rows) #remember to enforce uniqueness
        return [Ratings(*row) for row in rows]

    @staticmethod
    def get_by_drink(did):
        rows = app.db.execute('''
SELECT uid, did, time_rated, score, descript, likes, dislikes
FROM Ratings
WHERE did = :did
ORDER BY time_rated DESC
LIMIT 5
''',
                              did=did)
        print("rows:",rows) #remember to enforce uniqueness
        return [Ratings(*row) for row in rows]

    @staticmethod
    def get_avg_rating(did):
        avg_score = app.db.execute('''
SELECT round(avg(score), 1)
FROM Ratings
WHERE did = :did
LIMIT 5
''',
                              did=did)
        print("avg_score:", avg_score) #remember to enforce uniqueness
        return avg_score

#     @staticmethod
#     def get_all_by_uid_since(uid, since):
#         rows = app.db.execute('''
# SELECT id, uid, pid, review_time, review_content
# FROM Review
# WHERE uid = :uid
# AND review_time >= :since
# ORDER BY review_time DESC
# ''',
#                               uid=uid,
#                               since=since)
#         return [Review(*row) for row in rows]

    @staticmethod
    def remove_all_by_uid(uid):
        app.db.execute(''' DELETE FROM Ratings WHERE uid = :uid ''',
                        uid=uid)  

    @staticmethod
    def remove_all_by_did(did):
        app.db.execute(''' DELETE FROM Ratings WHERE did = :did ''',
                        did=did)  

    @staticmethod
    def remove_all_by_uid_did(uid, did):
        app.db.execute(''' DELETE FROM Ratings WHERE uid = :uid AND did = :did ''',
                        uid = uid,
                        did = did)  

    def insert(self):
        app.db.execute(''' INSERT INTO Ratings (uid, did, time_rated, score, descript, likes, dislikes)
                            VALUES (:uid, :did, :time_rated, :score, :descript, :likes, :dislikes) ''',
                            uid=self.uid,
                            did=self.did,
                            time_rated=self.time_rated,
                            score=self.score,
                            descript=self.descript,
                            likes=self.likes,
                            dislikes=self.dislikes)

    @staticmethod
    def downvote(uid, did):
        app.db.execute(''' UPDATE Ratings Set dislikes = dislikes + 1 WHERE dislikes >= 0 AND uid = :uid AND did = :did ''',
                        uid = uid,
                        did = did)

    @staticmethod
    def upvote(uid, did):
        app.db.execute(''' UPDATE Ratings Set likes = likes + 1 WHERE likes >= 0 AND uid = :uid AND did = :did''',
                        uid = uid,
                        did = did)
