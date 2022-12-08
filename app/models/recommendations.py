from flask import current_app as app

class Recommendations:
    # list of recommended drinks
    def __init__(self, did, name, category, picture, score):
        self.did = did
        self.name = name
        self.category = category
        self.picture = picture
        self.score = score

    @staticmethod
    def get_unique_categories():
        categories = app.db.execute('''
SELECT DISTINCT category
FROM Drinks
''',
                              )
                          
        return categories


    @staticmethod
    def get_category(did):
        rows = app.db.execute('''
SELECT Drinks.category
FROM Drinks
WHERE Drinks.did = :did
''',
                              did=did)
                          
        return rows[0]
   
    # On the drink page, output 5 drinks in same category
    @staticmethod
    def you_may_also_like(did):
        category = Recommendations.get_category(did)['category']
        rows = app.db.execute('''
SELECT Drinks.did, Drinks.name, Drinks.category, Drinks.picture, (SELECT round(avg(R1.score), 1) FROM Ratings R1 WHERE R1.did = Drinks.did LIMIT 5) as score
FROM Drinks
WHERE Drinks.category = :category AND Drinks.did != :did 
LIMIT 5
''',
                              did=did, category=category)
      
        return [Recommendations(*(row)) for row in rows]

    #get all time top drinks
    @staticmethod
    def get_top_drinks():
        rows = app.db.execute('''
SELECT D.did, D.name, D.category, D.picture, (SELECT round(avg(R1.score), 1) FROM Ratings R1 WHERE R1.did = D.did LIMIT 5) as score
FROM Drinks D
WHERE (SELECT round(avg(R1.score), 1) FROM Ratings R1 WHERE R1.did = D.did LIMIT 5) <> 0
ORDER BY score DESC
LIMIT 10
''',
                             )
        return [Recommendations(*row) for row in rows]

    @staticmethod
    def get_top_drinks_in_category(category):
        rows = app.db.execute('''
SELECT D.did, D.name, D.category, D.picture, (SELECT round(avg(R1.score), 1) FROM Ratings R1 WHERE R1.did = D.did LIMIT 5) as score
FROM Drinks D
WHERE D.category = :category AND (SELECT round(avg(R1.score), 1) FROM Ratings R1 WHERE R1.did = D.did LIMIT 5) <> 0
ORDER BY score DESC
LIMIT 10
''',
                              category=category)
        return [Recommendations(*row) for row in rows]


