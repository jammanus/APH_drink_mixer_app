from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json, requests

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/browse/letter/<lett>', methods=['GET', 'POST'])
def searchby_letter(lett):
    api_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={lett}"
    getresult = requests.get(api_url)
    res_letter = getresult.json()

    return render_template("search-by-letter.html", user=current_user, letter=res_letter)

@views.route('/browse/search/<name>', methods=['GET', 'POST'])
def searchby_name(name):
    api_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"
    getresult = requests.get(api_url)
    res_name = getresult.json()

    return render_template("search-cocktail.html", user=current_user, drinks=res_name)

@views.route('/drink/<did>', methods=['GET', 'POST'])
def drink_detail(did):
    api_url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={did}"
    getresult = requests.get(api_url)
    res_drink = getresult.json()

    return render_template("drink-detail.html", user=current_user, drinks=res_drink)

@views.route('/ingredient/<iid>/<name>', methods=['GET', 'POST'])
def ingredient_detail(iid,name):
    api_url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?iid={iid}"
    getresult = requests.get(api_url)
    res_ing = getresult.json()

    # to get the drinks available for this ingredient
    api_link = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={name}"
    getdrinks = requests.get(api_link)
    results = getdrinks.json()

    return render_template("ingredient-detail.html", user=current_user, drinks=res_ing, res_drinks=results)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
