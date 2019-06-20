from flask_restplus import Api

from .event import api as event  # here, we import the files that have the actual functions we want
from .user import api as user

api = Api(
    title='test',
    version='1.0',
    description='A file to practice things'
)

api.add_namespace(event, path='/event')  # when we want to get info from the events table, like say the data from event number 2
api.add_namespace(user, path='/user')  # we would need to go to https://someurl.com/event/2