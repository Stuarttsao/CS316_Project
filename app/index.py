from flask import render_template
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
    submit1 = SubmitField('Delete Cart')

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


    

    
@bp.route('/ratings', methods=['GET', 'POST'])
def social():
    my_rating = []
    authenticated = False
    if current_user.is_authenticated:
        current_uid = current_user.uid
        authenticated = True
        my_rating = Ratings.get_most_recent(current_uid)    

    form = SearchForm()
    rating = []
    if form.validate_on_submit():
        rating = Ratings.get_most_recent(form.search.data)    
        print(rating) 
    return render_template('social.html', title='Rating', auth=authenticated, form=form, my_ratings=my_rating, ratings=rating)
    
@bp.route('/menus', methods=['GET', 'POST'])
def menu():
    form = SearchForm()
    menu = []
    addMenu = addMenuForm()
    my_menus = []
    authenticated = False

    if form.validate_on_submit():
        menu = Menus.get_most_recent(form.search.data)    
        print(menu)
    if current_user.is_authenticated:
        current_uid = current_user.uid
        authenticated = True
        
        if addMenu.submit4.data and addMenu.validate():
            now = datetime.datetime.now()
            usermenu = Menus(uid=current_uid, name=addMenu.menuName.data, time_made=now.strftime("%m-%d-%Y %H:%M:%S"),summary=addMenu.menuSummary.data)
            usermenu.insert()
            
        my_menus = Menus.get_most_recent(current_uid)
        print(my_menus) 
    return render_template('menu.html', title='Menu', form=form, menus=menu, my_menus=my_menus, addMenu=addMenu, auth=authenticated)

@bp.route('/cart', methods=['GET', 'POST'])
def cartIndex():
    form = SearchForm()
    ingredient = []
    makable = []
    # delete cart
    deleteCart = deleteCartForm()
    if deleteCart.submit1.data and deleteCart.validate_on_submit():
        IngredientCart.remove_all_by_uid(deleteCart.userID1.data)
    
    # add to cart
    addCart = addCartForm()
    if addCart.submit2.data and addCart.validate():
        print("cart")
        cart = IngredientCart(uid=addCart.userID2.data, iid=addCart.ingredientID.data, amount=addCart.amount.data, unit=addCart.unit.data)
        cart.insert()

        # print(cart)

    if form.submit.data and form.validate_on_submit():
        ingredient = IngredientCart.get_by_uid(form.search.data)    
        
        iidList = []
        for i in ingredient:
            iidList.append(i.iid)
        print(iidList)

        makable = IngredientCart.search_by_cart(iidList)
        print(makable)

    return render_template('cart.html', title='IngredientCart', form=form, addCart = addCart ,deleteCart = deleteCart,ingredients=ingredient, makable = makable)

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

