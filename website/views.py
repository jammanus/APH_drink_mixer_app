from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json, requests

views = Blueprint('views', __name__)

# Function to make API request and return JSON data
def get_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to handle home route
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        name_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={search_query}"
        drinks = get_json_data(name_url).get('drinks', [])
        return render_template("search-cocktail.html", user=current_user, drinks=drinks)

    api_lnk = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=ice"
    random_drinks = get_json_data(api_lnk).get('drinks', [])

    api_cat = "https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list"
    bycat = get_json_data(api_cat).get('drinks', [])
    return render_template("home.html", user=current_user, random_drinks=random_drinks, cates=bycat)

# Function to handle search by letter route
@views.route('/browse/letter/<lett>', methods=['GET', 'POST'])
def searchby_letter(lett):
    ltr_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={lett}"
    ltr_data = get_json_data(ltr_url).get('drinks', [])
    return render_template("search-by-letter.html", user=current_user, letter=ltr_data)

# Function to handle filter by category route
@views.route('/browse/category/<cat>', methods=['GET', 'POST'])
def filterby_category(cat):
    cat_api = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?c={cat}"
    getcat = get_json_data(cat_api).get('drinks', [])

    # get category list
    api_cat = "https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list"
    bycat = get_json_data(api_cat).get('drinks', [])
    return render_template("filter-by-category.html", user=current_user, categories=getcat, cates=bycat)

# Function to handle drink detail route
@views.route('/drink/<did>', methods=['GET', 'POST'])
def drink_detail(did):
    drink_url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={did}"
    drink_data = get_json_data(drink_url).get('drinks', [])
    return render_template("drink-detail.html", user=current_user, drink=drink_data)

# Function to handle ingredient detail route
@views.route('/ingredient/<iid>/<ing>', methods=['GET', 'POST'])
def ingredient_detail(iid, ing):
    api_url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?iid={iid}"
    res_ing = get_json_data(api_url).get('ingredients', [])

    api_link = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ing}"
    res_drinks = get_json_data(api_link).get('drinks', [])

    return render_template("ingredient-detail.html", user=current_user, drinks=res_ing, res_drinks=res_drinks)

# Function to handle ingredient detail without ID route
@views.route('/ingredient/<ing>')
def ing_detail(ing):
    ingredient_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?i={ing}"
    ingredient_data = get_json_data(ingredient_url).get('ingredients', [])

    drinks_url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ing}"
    drinks_data = get_json_data(drinks_url).get('drinks', [])

    return render_template("ingredient-detail.html", user=current_user, ingredient=ingredient_data, res_drinks=drinks_data)

# Function to handle delete note route
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note.get('noteId', '')
    note_obj = Note.query.get(noteId)
    if note_obj and note_obj.user_id == current_user.id:
        db.session.delete(note_obj)
        db.session.commit()
    return jsonify({})
