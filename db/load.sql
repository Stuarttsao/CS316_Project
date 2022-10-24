\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_uid_seq',
                         (SELECT MAX(uid)+1 FROM Users),
                         false);


                         
\COPY Drinks FROM 'Drinks.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.drinks_did_seq',
                         (SELECT MAX(did)+1 FROM Drinks),
                         false);

\COPY Ingredients FROM 'Ingredients.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.ingredients_iid_seq',
                        (SELECT MAX(iid)+1 FROM Ingredients),
                        false);

\COPY ingredientCart FROM 'IngredientCart.csv' WITH DELIMITER ',' NULL '' CSV

-- \COPY Components FROM 'Components.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.components_iid_seq',
--                          (SELECT MAX(iid)+1 FROM Components),
--                          false);



-- \COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.products_id_seq',
--                          (SELECT MAX(id)+1 FROM Products),
--                          false);

-- \COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.purchases_id_seq',
--                          (SELECT MAX(id)+1 FROM Purchases),
--                          false);
