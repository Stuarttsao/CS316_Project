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
    submit = SubmitField('Add Drink')

class deleteCartForm(FlaskForm):
    userID = StringField('User ID', validators=[DataRequired()])
    submit = SubmitField('Delete Cart')


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

        # add drinks to database
    addDrink = addDrinkForm()
    if addDrink.validate_on_submit():
        drink = Drinks(did= 1000, name=addDrink.drinkName.data, category=addDrink.drinkCategory.data, picture=addDrink.drinkImage.data, instructions=addDrink.drinkInstructions.data)
        drink.insert()
        print(drink)
   
    drinks = []

    if form.validate_on_submit():
        drinks = Drinks.get_by_name(form.search.data)    
        print(drinks) 
    return render_template('drinks.html', title='Home', form=form, drinks=drinks, addDrink=addDrink)


    

    
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

    # delete cart
    deleteCart = deleteCartForm()
    if deleteCart.validate_on_submit():
        IngredientCart.remove_all_by_uid(deleteCart.userID.data)
        

    if form.validate_on_submit():
        ingredient = IngredientCart.get_by_uid(form.search.data)    
        print(ingredient) 
    return render_template('cart.html', title='IngredientCart', form=form, deleteCart = deleteCart,ingredients=ingredient)

@bp.route('/recommendations', methods=['GET', 'POST'])
def recommend():
    form = SearchForm()
    drink = []
    if form.validate_on_submit():
        drink = Ingredients.get_by_ingredient(form.search.data) 
        print(drink)
    return render_template('recommendations.html', title='Recommendations', form=form, drinks=drink)

