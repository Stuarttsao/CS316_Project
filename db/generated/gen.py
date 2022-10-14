from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_drinks = 500
num_ingredients = 100
num_components = 2000
num_menus = 200
num_menu_drinks = 2500
num_ingredient_carts = num_users
num_bar_carts = num_users
num_ratings = 1000


#num_products = 2000
#num_purchases = 2500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return available_uids
    
def gen_drinks(num_drinks):
    return available_dids
    
def gen_ingredients(num_ingredients):
    return available_iids
    
def gen_components(num_components, available_dids, available_iids):
    return

def gen_menus(num_menus, available_uids):
    return available_menu_names
    
def gen_menu_drinks(num_menu_drinks, available_uids, available_menu_names, available_dids):
    return
    
def gen_ingredient_cart(num_ingredient_carts, available_uids, available_iids):
    return

def gen_bar_cart(num_bar_carts, available_uids, available_dids):
    return
    
def gen_ratings(num_ratings, available_uids, available_dids):
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


available_uids = gen_users(num_users)
available_dids = gen_drinks(num_drinks)
available_iids = gen_ingredients(num_ingredients)
available_menu_names = gen_menus(num_menus, available_uids, available_dids)
gen_menu_drinks(num_menu_drinks, available_uids, available_menu_names, available_dids
gen_ingredient_cart(available_uids, available_iids)
gen_components(available_dids, available_iids)
gen_bar_cart(available_uids, available_dids)
gen_ratings(available_uids, available_dids)

#available_pids = gen_products(num_products)
#gen_purchases(num_purchases, available_pids)
