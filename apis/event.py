from .imports import Namespace, Resource, fields, request, query, make_json, make_insert_statement, make_update_statement

api = Namespace('events', description='event operations')


# this is where we define what you need in an event, which lets us test things easier in the Swagger UI
event_model = api.model('Event Model', 
		  {
              'title': fields.String(description="Event title"),
              'description': fields.String(description="Event description"),
              'category': fields.String(description="Event Category")
              })

@api.route('/')  # this is the "route", which tells us which url we need to go to (this one would be https://url.com/event/)
class EventList(Resource):

    def get(self):
        """gets every thing from the events table"""
        return make_json(query("SELECT * FROM events"))
    
    @api.expect(event_model)
    def post(self):
        '''add something to the events table'''
        value_dictionary = request.json
        sql = make_insert_statement(table="events", val_dict=value_dictionary)
        # this is a function that just makes a string 
        #       'INSERT INTO events (title, description, category) VALUES ('bleh', 'do stuff', 'service')
        # but makes it based on what data is provided by the dictionary

        id = query(sql)
        return make_json(query(f"SELECT * FROM events WHERE event_id={id}"))


@api.route('/<int:id>/') # this route would be https://url.com/event/69 or whichever id number at the end
class Event(Resource):
    def get(self, id):
        '''Gets an entry with the given id'''
        return make_json(query(f"SELECT * FROM events WHERE event_id={id}"))
    
    @api.expect(event_model)
    def put(self, id):
        '''updates the entry with this id, takes in a title, description, and category'''
        
        value_dictionary = request.json
        sql = make_update_statement(table="events", val_dict=value_dictionary, where_clause=f"event_id={id}")
        # this will make the string 
        #       "UPDATE events SET title='blah' WHERE event_id=3"
        # depending on what data is provided in the json 

        query(sql)
        return make_json(query(f"SELECT * FROM events WHERE event_id={id}"))
    
    def delete(self, id):  # this deletes the entry, and returns it at the end when someone makes a DELETE request to this url
        '''deletes this entry'''
        res = query(f"SELECT * FROM events WHERE event_id={id}")
        query(f"DELETE FROM events WHERE event_id={id}")
        return make_json(res)

    