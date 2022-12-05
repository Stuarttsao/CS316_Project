from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import pandas as pd
import numpy as np

#GETTING USABLE DATA FROM COCKTAIL DB AFTER SCRAPING----------------------------------------------------------

cocktail_df = pd.read_csv('repository.csv')
drink_names = cocktail_df['name'].values.tolist()
drink_category = cocktail_df['category'].values.tolist()
drink_instructions = cocktail_df['instructions'].values.tolist()
drink_images = cocktail_df['imageUrl'].values.tolist()
ingredient_cols = cocktail_df.columns[cocktail_df.columns.str.startswith('ingredients')]
ingredient_cols = [col for col in ingredient_cols if col.endswith('name')]
ingredient_names = pd.unique(cocktail_df[ingredient_cols].values.ravel()).tolist()

components = []
with open('repository.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    next(reader_obj)
    ingredient_ind = np.array([i for i in range(31) if (i >= 7) and (i % 2 == 1)])
    for row in reader_obj:
        row = np.array(row)
        drink = row[1]
        ingredients = row[ingredient_ind]
        measures = row[ingredient_ind+1]
        for i in range(len(ingredients)):
            ingredient = ingredients[i]
            if ingredient != '':
                measure_amount = measures[i].split(' ')
                measure = measure_amount[0]
                if len(measure_amount) > 1:
                    amount = measure_amount[1]
                components.append([drink, ingredient, measure, amount])

components = np.array(components)
units = list(set(components[:,3]))

#GETTING USABLE DATA FROM COCKTAIL DB AFTER SCRAPING----------------------------------------------------------

num_users = 20
num_drinks = len(drink_names)
num_ingredients = len(ingredient_names)
num_components = len(components)
num_menus = 50
num_menu_drinks = 300
num_ingredient_carts = 400
num_bar_carts = 100
num_ratings = 1000

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    uids = []
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 5 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            uids.append(uid)
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return uids
    
def gen_drinks(num_drinks):
    dids = []
    with open('Drinks.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Drinks...', end=' ', flush=True)
        for did in range(num_drinks):
            if did % 50 == 0:
                print(f'{did}', end=' ', flush=True)
            name = drink_names[did]
            category = drink_category[did]
            instructions = drink_instructions[did]
            #description = fake.sentence(nb_words=8)[:-1]
            image_url_id = fake.random_int(min=0, max=len(drink_images)-1)
            dids.append(did)
            writer.writerow([did, name, category, drink_images[image_url_id], instructions])##, description])
        print(f'{num_drinks} generated')
    return dids
    
def gen_ingredients(num_ingredients):
    iids = []
    with open('Ingredients.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Ingredients...', end=' ', flush=True)
        for iid in range(num_ingredients):
            if iid % 100 == 0:
                print(f'{iid}', end=' ', flush=True)
            name = ingredient_names[iid]
            #description = fake.sentence(nb_words=8)[:-1]
            iids.append(iid)
            writer.writerow([iid, name])#, description])
        print(f'{num_ingredients} generated')
    return iids
    
def gen_components(num_components, dids, iids):
    check = []
    with open('Components.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Components...', end=' ', flush=True)
        for id in range(num_components):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            component = components[id]
            did = 'WRONG INPUT'
            if (component[0] in drink_names):
                did = drink_names.index(component[0])
            iid = 'WRONG INPUT'
            if (component[1] in ingredient_names):
                iid = ingredient_names.index(component[1])
            amount = component[2]
            unit = component[3]
            if (iid,did) not in check:
                writer.writerow([iid, did, amount, unit])
                check.append((iid,did))
        print(f'{num_components} generated')
    return

def gen_menus(num_menus, uids):
    menu_names = []
    with open('Menus.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Menus...', end=' ', flush=True)
        for id in range(num_menus):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            name = fake.sentence(nb_words=1)[:-1]
            summary = fake.sentence(nb_words=8)[:-1]
            uid = fake.random_element(elements=uids)
            date = fake.date_time()
            menu_names.append([uid, name])
            writer.writerow([uid, name, date, summary])
        print(f'{num_menus} generated')
    return menu_names
    
def gen_menu_drinks(num_menu_drinks, menu_names, dids):
    menu_drinks = {}
    with open('Menu_Drinks.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Menu_Drinks...', end=' ', flush=True)
        for id in range(num_menu_drinks):
            if id % 50 == 0:
                print(f'{id}', end=' ', flush=True)
            did = fake.random_element(elements=dids)
            menu_name_id = fake.random_int(min=0, max=len(menu_names)-1)
            uid = menu_names[menu_name_id][0]
            menu_name = menu_names[menu_name_id][1]
            if uid not in menu_drinks:
                menu_drinks[uid] = {}
            if menu_name not in menu_drinks[uid]:
                menu_drinks[uid][menu_name] = []
            if did not in menu_drinks[uid][menu_name]:
                writer.writerow([uid, menu_name, did])
                menu_drinks[uid][menu_name].append(did)
        print(f'{num_menu_drinks} generated')
    return
    
def gen_ingredient_cart(num_ingredient_carts, uids, iids):
    check = []
    with open('IngredientCart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('IngredientCart...', end=' ', flush=True)
        for id in range(num_ingredient_carts):
            if id % 50 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            iid = fake.random_element(elements=iids)
            amount = fake.random_int(min=0, max=100)
            unitid = fake.random_int(min=0, max=len(units)-1)
            if (uid,iid) not in check:
                writer.writerow([uid, iid, amount, units[unitid]])
                check.append((uid,iid))
        print(f'{num_ingredient_carts} generated')
    return

def gen_bar_cart(num_bar_carts, uids, dids):
    check = []
    with open('BarCart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('BarCart...', end=' ', flush=True)
        for id in range(num_bar_carts):
            if id % 50 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            did = fake.random_element(elements=dids)
            times_made = fake.random_int(min=0, max=20)
            if (uid, did) not in check:
                writer.writerow([uid, did, times_made])
                check.append((uid,did))
        print(f'{num_bar_carts} generated')
    return
    
def gen_ratings(num_ratings, uids, dids):
    check = []
    with open('Ratings.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Ratings...', end=' ', flush=True)
        for id in range(num_ingredient_carts):
            if id % 50 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            did = fake.random_element(elements=dids)
            date = fake.date_time()
            score = fake.random_int(min=0, max=5)
            likes = fake.random_int(min=0, max=100)
            dislikes = fake.random_int(min=0, max=100)
            description = fake.sentence(nb_words=8)[:-1]
            if (uid,did) not in check:
                writer.writerow([uid, did, date, score, description, likes, dislikes])
                check.append((uid,did))
        print(f'{num_ratings} generated')
    return

# def gen_products(num_products):
#     available_pids = []
#     with open('Products.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Products...', end=' ', flush=True)
#         for pid in range(num_products):
#             if pid % 100 == 0:
#                 print(f'{pid}', end=' ', flush=True)
#             name = fake.sentence(nb_words=4)[:-1]
#             price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
#             available = fake.random_element(elements=('true', 'false'))
#             if available == 'true':
#                 available_pids.append(pid)
#             writer.writerow([pid, name, price, available])
#         print(f'{num_products} generated; {len(available_pids)} available')
#     return available_pids


# def gen_purchases(num_purchases, available_pids):
#     with open('Purchases.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Purchases...', end=' ', flush=True)
#         for id in range(num_purchases):
#             if id % 100 == 0:
#                 print(f'{id}', end=' ', flush=True)
#             uid = fake.random_int(min=0, max=num_users-1)
#             pid = fake.random_element(elements=available_pids)
#             time_purchased = fake.date_time()
#             writer.writerow([id, uid, pid, time_purchased])
#         print(f'{num_purchases} generated')
#     return


uids = gen_users(num_users)
dids = gen_drinks(num_drinks)
iids = gen_ingredients(num_ingredients)
menu_names = gen_menus(num_menus, uids)
gen_menu_drinks(num_menu_drinks, menu_names, dids)
gen_ingredient_cart(num_ingredient_carts, uids, iids)
gen_components(num_components, dids, iids)
gen_bar_cart(num_bar_carts, uids, dids)
gen_ratings(num_ratings, uids, dids)

#available_pids = gen_products(num_products)
#gen_purchases(num_purchases, available_pids)
