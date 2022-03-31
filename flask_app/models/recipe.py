from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.is_under_30 = data['is_under_30']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data['creator']

    @staticmethod
    def validate_recipe(form):
        is_valid = True
        if len(form['name']) < 1:
            flash('Please enter the recipe name.', 'name')
            is_valid = False
        if len(form['description']) < 1:
            flash('Please enter the recipe description.', 'description')
            is_valid = False
        if len(form['instructions']) < 1:
            flash('Please enter the recipe instructions.', 'instructions')
            is_valid = False
        if len(form['date_made']) < 1:
            flash('Please enter the date.', 'date_made')
            is_valid = False
        if 'is_under_30' not in form:
            flash('Please select yes or no.', 'is_under_30')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, date_made, is_under_30, creator_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(is_under_30)s, %(creator_id)s);'
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def get_all_with_creator(cls):
        query = 'SELECT * from recipes JOIN users on users.id = recipes.creator_id;'
        recipes = []
        results = connectToMySQL('recipes_schema').query_db(query)
        for result in results:
            data = {
                'user_id': result['creator_id']
            }
            creator = User.get_one(data)
            recipe_data = {
                'id': result['id'],
                'name': result['name'],
                'description': result['description'],
                'instructions': result['instructions'],
                'date_made': result['date_made'],
                'is_under_30': result['is_under_30'],
                'creator_id': result['creator_id'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'creator': creator
            }
            recipes.append(Recipe(recipe_data))
        return recipes

    @classmethod
    def get_one_with_creator(cls, data):
        query = 'SELECT * FROM recipes WHERE id = %(recipe_id)s;'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        data = {
            'user_id': results[0]['creator_id']
        }
        creator = User.get_one(data)
        recipe_data = {
            'id': results[0]['id'],
            'name': results[0]['name'],
            'description': results[0]['description'],
            'instructions': results[0]['instructions'],
            'date_made': results[0]['date_made'],
            'is_under_30': results[0]['is_under_30'],
            'creator_id': results[0]['creator_id'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'creator': creator
        }
        recipe = Recipe(recipe_data)
        return recipe

    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, is_under_30 = %(is_under_30)s WHERE id = %(recipe_id)s;'
        connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE from recipes WHERE id = %(recipe_id)s;'
        connectToMySQL('recipes_schema').query_db(query, data)
