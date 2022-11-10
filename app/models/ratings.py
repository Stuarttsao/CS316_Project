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
        self.date = time_rated
        self.score = score
        self.description = descript
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
        return [Ratings(*row) for row in rows] if rows else None

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
