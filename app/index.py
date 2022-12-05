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
from .models.barcart import BarCart
from .models.components import Components

from flask import Blueprint
bp = Blueprint('index', __name__)


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class addDrinkForm(FlaskForm):
    drinkName = StringField('Drink Name', validators=[DataRequired()])
    drinkCategory = StringField('Drink Category', validators=[DataRequired()])
    drinkInstructions = StringField('Drink Instructions', validators=[DataRequired()])
    drinkImage = StringField('Drink Image', validators=[DataRequired()])
    submit1 = SubmitField('Add Drink')

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
    userID3 = StringField('User ID', validators=[DataRequired()])
    drinkID3 = StringField('Drink ID', validators=[DataRequired()])
    time_rated = StringField('Time Rated', validators=[DataRequired()])
    score = StringField('Score', validators=[DataRequired()])
    descript = StringField('Description', validators=[DataRequired()])
    likes = StringField('Likes', validators=[DataRequired()])
    dislikes = StringField('Dislikes', validators=[DataRequired()])
    submit5 = SubmitField('Add to Cart')

class getAvgRatingForm(FlaskForm):
    drinkID4 = StringField('Drink ID', validators=[DataRequired()])
    submit6 = SubmitField('Search')


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    drinks = []
    ingredients = []

    if form.submit.data and form.validate_on_submit():
        drinks = Drinks.get_by_name(form.search.data) 
           
        print(drinks) 
        if drinks != []:
            ingredients = Components.get_by_did(drinks[0].did)
            print(ingredients)

        

        # add drinks to database
    addDrink = addDrinkForm()
    if addDrink.submit1.data and addDrink.validate_on_submit():
        drink = Drinks(did= 1000, name=addDrink.drinkName.data, category=addDrink.drinkCategory.data, picture=addDrink.drinkImage.data, instructions=addDrink.drinkInstructions.data)
        drink.insert()
        print(drink)
   
    return render_template('drinks.html', title='Home', form=form, drinks=drinks, addDrink=addDrink, ingredients = ingredients)


@bp.route('/drink/<did>', methods=['GET', 'POST'])
def drink(did):
    drink = Drinks.get_by_did(did)
    ingredients = Components.get_by_did(did)
    return render_template('drink.html', title='Drink', drink=drink, ingredients=ingredients)

# @bp.route('/addToCart/<iid>', methods=['GET', 'POST'])
# def addToCart(iid):
#     ingredient = Ingredients.get_by_iid(iid)


@bp.route('/ratings', methods=['GET', 'POST'])
def social():
    form = SearchForm()
    rating = []

    # delete by uid
    deleteReviewUid = deleteReviewUidForm()
    if deleteReviewUid.validate_on_submit():
        Ratings.remove_all_by_uid(deleteReviewUid.userID.data)

    # delete by did
    deleteReviewDid = deleteReviewDidForm()
    if deleteReviewDid.validate_on_submit():
        Ratings.remove_all_by_did(deleteReviewDid.drinkID.data)

    # delete by uid/did combo
    deleteReviewUidDid = deleteReviewUidDidForm()
    if deleteReviewUidDid.validate_on_submit():
        Ratings.remove_all_by_uid_did(deleteReviewUidDid.userID2.data, deleteReviewUidDid.drinkID2.data)
    
    # add to reviews
    addReview = addReviewForm()
    if addReview.validate():
        print("cart")
        cart = Ratings(uid=addReview.userID3.data, did=addReview.drinkID3.data, time_rated=addReview.time_rated.data, score=addReview.score.data, descript=addReview.descript.data, likes=addReview.likes.data, dislikes=addReview.dislikes.data)
        cart.insert()

    # find average rating of a drink
    getAvgRating = getAvgRatingForm()
    avg = 0
    if getAvgRating.validate_on_submit():
        avg = Ratings.get_avg_rating(getAvgRating.drinkID4.data)
        print(avg)


    if form.validate_on_submit():
        rating = Ratings.get_most_recent(form.search.data)    
        print(rating) 
    return render_template('social.html', title='Rating', form=form, deleteReviewUid = deleteReviewUid, deleteReviewDid = deleteReviewDid, deleteReviewUidDid = deleteReviewUidDid, addReview = addReview, getAvgRating = getAvgRating, ratings=rating, avgs=avg)

@bp.route('/menus/<uid>/<menuName>/<summary>/<date>', methods=['GET', 'POST'])
def menu(uid, menuName, summary, date):
    addDrink = addDrinktoMenuForm()
    dids = Menus.get_menudrinks(uid, menuName)
    drinks = []
    owned = False
    drinkadd = True
    for did in dids:
        drink = Drinks.get_by_did(did)
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
                drink = Drinks.get_by_did(did)
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
    addMenu = addMenuForm()
    my_menus = []
    authenticated = False
    added = True

    if uid_search.validate_on_submit():
        uids = Menus.uids()
        if int(uid_search.search.data) not in uids:
            menus = []
        menus = Menus.get(uid_search.search.data)    
    if current_user.is_authenticated:
        current_uid = current_user.uid
        authenticated = True
        
        if addMenu.submit4.data and addMenu.validate():
            now = datetime.datetime.now()
            usermenu = Menus(uid=current_uid, name=addMenu.menuName.data, time_made=now.strftime("%m-%d-%Y %H:%M:%S"),summary=addMenu.menuSummary.data)
            if not usermenu.insert():
                added = False
        my_menus = Menus.get_most_recent(current_uid)
    return render_template('menus.html', title='Menus', form=uid_search, menus=menus, my_menus=my_menus, addMenu=addMenu, auth=authenticated, added=added)

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

    return render_template('cart.html', title='IngredientCart',
    form=form, addCart = addCart ,deleteCart = deleteCart,ingredients=ingredients, localCart = localCart, makable = makable)



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
                drinkName = Drinks.get_by_did(barcart.did).name
                my_drinks.append([drinkName, barcart.times_made])
            print(my_drinks)
    return render_template('barcart.html', title='BarCart', auth=authenticated, addBarCart=addBarCart, my_drinks=my_drinks)

@bp.route('/recommendations', methods=['GET', 'POST'])
def recommend():
    form = SearchForm()
    drink = []
    if form.validate_on_submit():
        drink = Ingredients.get_by_ingredient(form.search.data) 
        print(drink)

