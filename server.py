from flask_app import app

# import models here
from flask_app.models.user import User

# import controllers here
from flask_app.controllers import users, recipes

if __name__ == '__main__':
    app.run(debug=True)