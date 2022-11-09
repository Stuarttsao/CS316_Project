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
from .models.cart import Cart
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
    form = SearchForm()
    rating = []
    if form.validate_on_submit():
        rating = Ratings.get_most_recent(form.search.data)    
        print(rating) 
    return render_template('social.html', title='Rating', form=form, ratings=rating)

@bp.route('/menus', methods=['GET', 'POST'])
def menu():
    form = SearchForm()
    menu = []
    if form.validate_on_submit():
        menu = Menus.get_most_recent(form.search.data)    
        print(menu) 
    return render_template('menu.html', title='Menu', form=form, menus=menu)

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

@bp.route('/recommendations', methods=['GET', 'POST'])
def recommend():
    form = SearchForm()
    drink = []
    if form.validate_on_submit():
        drink = Ingredients.get_by_ingredient(form.search.data) 
        print(drink)
    return render_template('recommendations.html', title='Recommendations', form=form, drinks=drink)

