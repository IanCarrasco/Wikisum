from flask_restful import Resource, Api
from flask import Flask
from flask_cors import CORS
from wikisort import wordRelevance, summaries

app = Flask(__name__)
CORS(app, resources={r"/wiki/*": {"origins": "*"}})
api = Api(app)

class WikiTitle(Resource):
    def get(self,topic):
        return {'titles': wordRelevance(topic)}

class WikiSummary(Resource):
    def get(self,topics):
        return {'summaries': summaries(topics)}



api.add_resource(WikiTitle, '/wiki/<string:topic>/titles')
api.add_resource(WikiSummary, '/wiki/<string:topics>/summaries')

if __name__ == '__main__':
    app.run(debug=True)
