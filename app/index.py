# from urllib import request
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from flask_wtf import FlaskForm


from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User
from .models.drinks import Drinks
from .models.ratings import Ratings
from .models.menus import Menus
from .models.ingredientCart import IngredientCart
from .models.ingredients import Ingredients
#from .models.cart import Cart
from .models.bartender import Bartender
from .models.barcart import BarCart
from .models.components import Components
from .models.recommendations import Recommendations


from flask import Blueprint
bp = Blueprint('index', __name__)

import openai
secret = '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'

def generateImage(text):
    openai.api_key = secret
    response = openai.Image.create(
        prompt=text,
        n =2,
        size= "256x256",
    )
    return response


ingredients2 = []



class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class addDrinkForm(FlaskForm):
    drinkName = StringField('Drink Name', validators=[DataRequired()])
    drinkCategory = StringField('Drink Category', validators=[DataRequired()])
    drinkInstructions = StringField('Drink Instructions', validators=[DataRequired()])
    drinkImage = StringField('Drink Image', validators=[DataRequired()])
    submit1 = SubmitField('Add Drink')

class editDrinkForm(FlaskForm):
    drinkInstructions = StringField('Drink Instructions', validators=[DataRequired()])
    submit_edit = SubmitField('Submit Edit')

class deleteCartForm(FlaskForm):
    userID1 = StringField('User ID', validators=[DataRequired()])
    submit1 = SubmitField('Clear Cart')

class addCartForm(FlaskForm):
    userID2 = StringField('User ID', validators=[DataRequired()])
    ingredientID = StringField('Ingredient ID', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    submit2 = SubmitField('Add to Cart')

class addBarForm(FlaskForm):
    drinkName = StringField('Drink Name', validators=[DataRequired()])
    timesMade = StringField('Times Made', validators=[DataRequired()])
    submit3 = SubmitField('Add to Your Bar')

class addMenuForm(FlaskForm):
    menuName = StringField('Menu Name', validators=[DataRequired()])
    menuSummary = StringField('Menu Summary', validators=[DataRequired()])
    submit4 = SubmitField('Add New Menu')

class addDrinktoMenuForm(FlaskForm):
    drinkName = StringField('Drink Name', validators=[DataRequired()])
    submit = SubmitField('Add Drink to Menu')

class deleteReviewUidForm(FlaskForm):
    userID = StringField('User ID', validators=[DataRequired()])
    submit2 = SubmitField('Delete Cart')

class deleteReviewDidForm(FlaskForm):
    drinkID = StringField('Drink ID', validators=[DataRequired()])
    submit3 = SubmitField('Delete Cart')

class deleteReviewUidDidForm(FlaskForm):
    userID2 = StringField('User ID', validators=[DataRequired()])
    drinkID2 = StringField('Drink ID', validators=[DataRequired()])
    submit4 = SubmitField('Delete Cart')

class addReviewForm(FlaskForm):
    #userID3 = StringField('User ID', validators=[DataRequired()])
    #drinkID3 = StringField('Drink ID', validators=[DataRequired()])
    #time_rated = StringField('Time Rated', validators=[DataRequired()])
    score = StringField('Score', validators=[DataRequired()])
    descript = StringField('Description', validators=[DataRequired()])
    #likes = StringField('Likes', validators=[DataRequired()])
    #dislikes = StringField('Dislikes', validators=[DataRequired()])
    submit5 = SubmitField('Add Review')

class getAvgRatingForm(FlaskForm):
    drinkID4 = StringField('Drink ID', validators=[DataRequired()])
    submit6 = SubmitField('Search')

class editReviewForm(FlaskForm):
    score2 = StringField('Score', validators=[DataRequired()])
    descript2 = StringField('Description', validators=[DataRequired()])
    submit7 = SubmitField('Edit Review')

@bp.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    drinks = []
    ingredients = []

    if form.submit.data and form.validate_on_submit():
        checked = request.form.get('searchTerm') 
        print(checked)
        if checked == "drink":
            drinks = Drinks.get_by_name(form.search.data) 
        elif checked == "ingredient":
            drinks = Drinks.get_drinks_by_ingredientName(form.search.data)
        elif checked == "category":
            drinks = Drinks.get_by_category(form.search.data)
        
           
        print(drinks) 
        if drinks != []:
            ingredients = Components.get_by_did(drinks[0].did)
            print(ingredients)
    return render_template('home.html', title='Home', form=form, drinks=drinks, ingredients = ingredients)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/profile/<uid>', methods=['GET', 'POST'])
def user_profile(uid):
    user = User.get_by_uid(uid)
    menus = Menus.get_most_recent(uid)
    ratings = Ratings.get_most_recent(uid)
    barcart = BarCart.get_most_made(uid)
    disp_bar = []
    if barcart:
        for drink in barcart:
            thisDrink = Drinks.get_by_did(drink.did)[0]
            disp_bar.append((thisDrink.name, drink))
    user_drinks = Bartender.get_all(uid)
    disp_drinks = []
    if user_drinks:
        for drink in user_drinks:
            thisDrink = Drinks.get_by_did(drink.did)[0]
            disp_drinks.append((thisDrink.name, drink))
    authenticated = False
    if current_user.is_authenticated:
        authenticated = True

    times_made = BarCart.get_count(uid)
    drinks_invented = Bartender.get_count(uid)
    return render_template('user_profile.html', title='Profile', menus=menus, ratings=ratings, auth=authenticated, user=user, barcart=disp_bar, drinks=disp_drinks, times_made=times_made, drinks_invented=drinks_invented)


@bp.route('/add', methods=['GET', 'POST'])
def add():


        # add drinks to database
    form2 = SearchForm()
    ingredients = ingredients2

    addedIngredients = []

    drink = 0
    addedDrink = False
    newDrink = False
    addDrink = addDrinkForm()
    authenticated = False


    if addDrink.submit1.data:
        print("in add")

        try:
            res = generateImage(addDrink.drinkName.data + "cocktail")
            drink = Drinks(did= 1000, name=addDrink.drinkName.data, category=addDrink.drinkCategory.data, picture=res["data"][0]["url"], instructions=addDrink.drinkInstructions.data)
        except: 
            drink = Drinks(did= 1000, name=addDrink.drinkName.data, category=addDrink.drinkCategory.data, picture="na", instructions=addDrink.drinkInstructions.data)

        
        drink.insert()

        addedDrink = True
        newDrink = Drinks.get_by_name(addDrink.drinkName.data)
        print("new drink:")
        print(newDrink[0].did)
        
        # print("ingredients:", ingredients[0])
        for ing in ingredients2:
            print("added", ing.name)
            print(newDrink[0].did)

            temp = Components(newDrink[0].did, ing.iid, 1, 1)
            temp.insert()

        ingredients2.clear()

        if current_user.is_authenticated:
            authenticated = True
            if addedDrink:
                author = Bartender(uid=current_user.uid, did=newDrink[0].did)
                author.insert()

        return redirect(url_for('index.drink', did= newDrink[0].did))

    if form2.submit.data and form2.validate_on_submit():   
        print("in 1")
        ing2 = Ingredients.get_by_name(form2.search.data)
        if ing2:
            print(ing2[0].name)
            print(ing2[0].iid)

            ingredients2.append(ing2[0])
    
    if current_user.is_authenticated:
        authenticated = True
        if addedDrink:
            author = Bartender(uid=current_user.uid, did=newDrink[0].did)
            author.insert()

    return render_template('drinks.html', title='Add Drink', addDrink=addDrink, drink=drink, auth=authenticated, form2 = form2, ingredients=ingredients, addedIngredients=addedIngredients)

# individual drink pages
@bp.route('/drink/<did>', methods=['GET', 'POST'])
def drink(did):
    print("did: ", did)
    authenticated = False
    current_uid = -1

    voted = False

    if current_user.is_authenticated:
        current_uid = current_user.uid
        authenticated = True
    
    # add to reviews
    addReview = addReviewForm()
    if authenticated and addReview.validate_on_submit():
        now_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        print("cart")
        cart = Ratings(uid=current_uid, did=did, time_rated=now_time, score=addReview.score.data, descript=addReview.descript.data, likes=0, dislikes=0)
        cart.insert()

    #upvote/downvote functionality
    
    if request.method == 'POST':
        if voted == False:
            if request.form.get("upvote"):
                did_in = request.form.get('did_out')
                uid_in = request.form.get('uid_out')
                Ratings.upvote(uid_in, did_in)
                voted = True
            if request.form.get("downvote"):
                did_in = request.form.get('did_out')
                uid_in = request.form.get('uid_out')
                Ratings.downvote(uid_in, did_in)
                voted = True
    
    print("did: ", did)
    ingredients = Components.get_by_did(did)
    avg_rating = Ratings.get_avg_rating(did)
    ratings = Ratings.get_by_drink(did)
    author = Bartender.get_by_did(did)


    recommendations = Recommendations.you_may_also_like(did)
    
    edit = False
    if author:
        author = author.uid
        if current_user.is_authenticated:
            if author == current_user.uid:
                edit = True
    drink = Drinks.get_by_did(did)[0]

    editDrink = editDrinkForm()
    if editDrink.validate_on_submit():
        drink.update(editDrink.drinkInstructions.data)

    drink = Drinks.get_by_did(did)[0]
    return render_template('drink.html', title='Drink', drink=drink, authenticated=authenticated, ingredients=ingredients, avg=avg_rating, ratings=ratings, editDrink=editDrink, addReview=addReview, edit=edit, author=author, recommendations=recommendations)

# @bp.route('/addToCart/<iid>', methods=['GET', 'POST'])
# def addToCart(iid):
#     ingredient = Ingredients.get_by_iid(iid)


@bp.route('/ratings', methods=['GET', 'POST'])
def ratings():
    authenticated = False
    current_uid = -1
    ratings_new = []
    if current_user.is_authenticated:
        current_uid = current_user.uid
        authenticated = True
        if request.method == 'POST':
            if request.form.get("deleteRating"):
                name = request.form.get('deleteRating')[7:]
                name = Drinks.get_by_name(name)[0].did
                Ratings.remove_all_by_uid_did(current_uid, name)
            if request.form.get("editRating"):
                name = request.form.get('editRating')[5:]
                # add edit functionality here
        ratings = Ratings.get(current_uid)
        if ratings:
            for rating in ratings:
                name = Drinks.get_by_did(rating.did)[0].name
                ratings_new.append((name, rating))
    return render_template('ratings.html', title='Rating', authenticated=authenticated, ratings=ratings_new)

@bp.route('/editratings/<uid>/<did>', methods=['GET', 'POST'])
def ratingEdit(uid, did):
    print("did: ", did)
    authenticated = False
    current_uid = -1

    if current_user.is_authenticated:
        current_uid = current_user.uid
        authenticated = True
    
    # edit review
    editReview = editReviewForm()
    if authenticated and editReview.validate_on_submit():
        now_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        print("cart")
        Ratings.updateRating(uid=current_uid, did=did, score=editReview.score2.data, descript=editReview.descript2.data)

    return render_template('editrating.html', editReview=editReview)

@bp.route('/menus/<uid>/<menuName>/<summary>/<date>', methods=['GET', 'POST'])
def menu(uid, menuName, summary, date):
    addDrink = addDrinktoMenuForm()
    dids = Menus.get_menudrinks(uid, menuName)
    drinks = []
    owned = False
    drinkadd = True
    for did in dids:
        drink = Drinks.get_by_did(did)[0]
        drinks.append(drink)
    if current_user.is_authenticated:
        if str(current_user.uid) == str(uid):
            owned = True
    if addDrink.submit.data and addDrink.validate():
        drink = Drinks.get_by_name(addDrink.drinkName.data)
        if len(drink) == 1:
            Menus.insert_drink(uid, menuName, drink[0].did)
            drinks = []
            dids = Menus.get_menudrinks(uid, menuName)
            for did in dids:
                drink = Drinks.get_by_did(did)[0]
                drinks.append(drink)
                print(drinks)
        else:
            drinkadd = False
    return render_template('menu.html', title='Menu', uid=uid, menuName=menuName, 
                            summary=summary, date=date, drinks=drinks, dids=dids, owned=owned, addDrink = addDrink,
                            drinkadd=drinkadd)

@bp.route('/menus', methods=['GET', 'POST'])
def menus():
    uid_search = SearchForm()
    menus = []
    search = True
    addMenu = addMenuForm()
    my_menus = []
    authenticated = False
    added = True

    if uid_search.validate_on_submit():
        uids = Menus.uids()
        if int(uid_search.search.data) not in uids:
            menus = []
        menus = Menus.get(uid_search.search.data)
        if menus:
            search = True
        else:
            search = False
    if current_user.is_authenticated:
        current_uid = current_user.uid
        authenticated = True
        
        if addMenu.submit4.data and addMenu.validate():
            now = datetime.datetime.now()
            usermenu = Menus(uid=current_uid, name=addMenu.menuName.data, time_made=now.strftime("%m-%d-%Y %H:%M:%S"),summary=addMenu.menuSummary.data)
            if not usermenu.insert():
                added = False
        if request.method == 'POST':
            if request.form.get("deleteMenu"):
                name = request.form.get('deleteMenu')[7:]
                Menus.delete_menu(current_user.uid, name)
        my_menus = Menus.get_most_recent(current_uid)
    return render_template('menus.html', title='Menus', form=uid_search, menus=menus, my_menus=my_menus, addMenu=addMenu, auth=authenticated, added=added, search=search)

@bp.route('/cart', methods=['GET', 'POST'])
def cartIndex():
    form = SearchForm()
    ingredients = []
    makable = []
    addIngredient = []
    deleteCart = deleteCartForm()
    addCart = addCartForm()
    localCart = []
    # delete cart
    if current_user.is_authenticated:
        
        localCart = IngredientCart.get_by_uid(current_user.uid)

        if request.method == 'POST':

            if request.form.get('clearCart') == 'Clear Cart':
                IngredientCart.remove_all_by_uid(current_user.uid)
                localCart = IngredientCart.get_by_uid(current_user.uid)
                print(localCart)
                print("deleted cart")
            
            if request.form.get('add'):
                cart = IngredientCart(uid=current_user.uid, iid=request.form.get('ingredient'), amount=100, unit="placeholder")
                cart.insert()
                localCart = IngredientCart.get_by_uid(current_user.uid)

        # # add to cart
        # if addCart.submit2.data and addCart.validate():
        #     print("cart")
        #     cart = IngredientCart(uid=addCart.userID2.data, iid=addCart.ingredientID.data, amount=addCart.amount.data, unit=addCart.unit.data)
        #     cart.insert()
        #     localCart = IngredientCart.get_by_uid(current_user.uid)

        if form.submit.data and form.validate_on_submit():        
            ingredients = Ingredients.get_by_name(form.search.data)
            print(ingredients)

        if request.form.get('makable') == 'Search':       
            iidList = []
            for i in localCart:
                iidList.append(i.iid)
            print(iidList)

            makable = IngredientCart.search_by_cart(iidList)
            print(makable)

    authenticated = False
    if current_user.is_authenticated:
        authenticated = True
    return render_template('cart.html', title='IngredientCart',
    form=form, addCart = addCart ,deleteCart = deleteCart,ingredients=ingredients, localCart = localCart, makable = makable, user=authenticated)



@bp.route('/barcart', methods=['GET', 'POST'])
def barCart():

    my_drinks=[]
    authenticated = False
    addBarCart = addBarForm()

    if current_user.is_authenticated:
        current_uid = current_user.uid
        authenticated = True
        
        if addBarCart.submit3.data and addBarCart.validate():
            submit_drink = Drinks.get_by_name(addBarCart.drinkName.data)
            barcart = BarCart(uid=current_uid, did=submit_drink[0].did,times_made=addBarCart.timesMade.data)
            barcart.insert()
            
        my_drinks_barcart = BarCart.get_drinks_in_cart(current_uid)
        if my_drinks_barcart:
            for barcart in my_drinks_barcart:
                drinkName = Drinks.get_by_did(barcart.did)[0].name
                my_drinks.append((drinkName, barcart))
            print(my_drinks)

    return render_template('barcart.html', title='BarCart', auth=authenticated, addBarCart=addBarCart, my_drinks=my_drinks)

@bp.route('/recommendations', methods=['GET', 'POST'])
def recommend():

    categories = Recommendations.get_unique_categories()
    
    return render_template('recommendations.html', title='Explore', categories=categories)

# individual explore pages
@bp.route('/recommendations/<list_name>', methods=['GET', 'POST'])
def explore(list_name):
    categories = {'Cocoa': 'Cocoa',
'Coffee ': 'Coffee / Tea',
'Cocktail': 'Cocktail',
'Homemade Liqueur': 'Homemade Liqueur',
'Milk ': 'Milk / Float / Shake',
'Shot': 'Shot',
'Beer': 'Beer',
'Ordinary Drink':'Ordinary Drink',
'Soft Drink ': 'Soft Drink / Soda',
'Other': 'Other/Unknown',
'Punch ': 'Punch / Party Drink'}

    error = False
    if list_name == 'drinks':
        results = Recommendations.get_top_drinks() 
        return render_template('topdrinklist.html', title='list_name', results=results, list_name=list_name)
    elif list_name not in categories:
        error = True
        return render_template('recommendations.html', title='Explore', categories=Recommendations.get_unique_categories(), error=error)

    results = Recommendations.get_top_drinks_in_category(categories[list_name]) 
    return render_template('topdrinklist.html', title='list_name', results=results, list_name=list_name)