from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in or register.', 'login_error')
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_one(data)
    all_recipes = Recipe.get_all_with_creator()
    return render_template('dashboard.html', user = user, all_recipes = all_recipes)

@app.route('/recipes/new')
def recipes_new():
    if 'user_id' not in session:
        flash('Please log in or register.', 'login_error')
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_one(data)
    return render_template('recipes_new.html', user = user)

@app.route('/recipes/insert', methods=['POST'])
def recipes_insert():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):
    data = {
        'user_id': session['user_id'],
        "recipe_id": recipe_id
    }
    user = User.get_one(data)
    recipe = Recipe.get_one_with_creator(data)
    return render_template('show_recipe.html', user = user, recipe = recipe)

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        flash('Please log in or register.', 'login_error')
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'recipe_id': recipe_id
    }
    user = User.get_one(data)
    recipe = Recipe.get_one_with_creator(data)
    return render_template('edit_recipe.html', user = user, recipe = recipe)

@app.route('/recipes/update/<int:recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    data = {
        'recipe_id': recipe_id
    }
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')
    Recipe.update(request.form)
    return redirect(f'/recipes/{recipe_id}')