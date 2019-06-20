from flask import Flask 
from apis import api  # this imports the files where we actually deal with the database
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})  # this lets us use this api from any url, instead of the same one that holds this file 
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)