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

from flask import Blueprint
bp = Blueprint('index', __name__)


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')



@bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    drink = []
    if form.validate_on_submit():
        drink = Drinks.get_by_name(form.search.data)    
        print(drink) 
    return render_template('drinks.html', title='Home', form=form, drinks=drink)

    
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
    if form.validate_on_submit():
        ingredient = IngredientCart.get_by_uid(form.search.data)    
        print(ingredient) 
    return render_template('cart.html', title='IngredientCart', form=form, ingredients=ingredient)

