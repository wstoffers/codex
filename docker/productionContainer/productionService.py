#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
from flask import Flask
from flask_restful import reqparse, Resource, Api

from productionModel import awaken

#define:
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('ingredients')

class cocktailClassifier(Resource):
    def __init__(self):
        pass

    def post(self):
        args = parser.parse_args()
        return awaken((args['ingredients'],))

#run:
if __name__ == '__main__':
    import waitress as waitperson
    api.add_resource(cocktailClassifier, '/')
    waitperson.serve(app, host='0.0.0.0', port=8080)
