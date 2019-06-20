from .imports import Namespace, Resource, fields, request, query, make_json, make_insert_statement, make_update_statement

api = Namespace('user', description='user operations')

# this is where we define what you need in a user, which lets us test things easier in the Swagger UI
user_model = api.model('User Model', 
		  {
              'firstname': fields.String(description="Person's first name"),
              'lastname': fields.String(description="Person's last name"),
              'email': fields.String(description="Person's email")
              })

@api.route('/')  # this sets which url we need to go to if we want to use these functions (this one would be https://url.com/user/)
class UserList(Resource):

    def get(self):  # if someone makes a get request to https://url.com/users, they will get the information for all users in json format
        '''lists out all users'''
        statement = f"SELECT user_id, firstname, lastname, email FROM users"
        result = query(statement)
        return make_json(result)
    
    @api.expect(user_model)
    def post(self):  # if they make a post request to this url, and provide a json input that matches the model, it will insert it into the database
        '''add something to the user table'''

        value_dictionary = request.json  # the json that they provided is turned into a python dictionary

        sql = make_insert_statement(table="users", val_dict=value_dictionary)  
        # this is a function that just makes a string 
        #       'INSERT INTO users (firstname, lastname, email) VALUES ('jimmy', 'smith', 'email@mail.com')
        # but makes it based on what data is provided by the dictionary

        id = query(sql)  # it saves the id of the entry it just added
        return make_json(query(f"SELECT * FROM users WHERE user_id={id}"))  # then it returns the new entry


@api.route('/<int:user_id>/')
class User(Resource):

    def get(self, user_id):
        # this gets the data for only one user
        ''' 
        Gets the user_id, email, firtname, lastname
        '''
        result = query(f"SELECT user_id, firstname, lastname, email FROM users WHERE user_id={user_id}")
        return make_json(result)

    
    @api.expect(user_model)
    def put(self, user_id):  # put requests are for updating data, so this will update the entry with id = user_id
        '''updates the entry with this id, takes in a firstname, lastname, email'''
        value_dictionary = request.json
        # this finds the data the user put in as a json, then uses it as a dictionary

        sql = make_update_statement(table="users", val_dict=value_dictionary, where_clause=f"user_id={user_id}")
        # this will make the string 
        #       "UPDATE users SET firstname='jimmy' WHERE user_id=3"
        # depending on what data is provided in the json 

        query(sql)
        return make_json(query(f"SELECT * FROM users WHERE user_id={user_id}"))  # finally, it returns the entry it just updated
    
    def delete(self, user_id):  # this deletes the entry, and returns it at the end when someone makes a DELETE request to this url
        '''deletes this entry'''
        res = query(f"SELECT * FROM users WHERE user_id={user_id}")
        query(f"DELETE FROM users WHERE user_id={user_id}")
        return make_json(res)

