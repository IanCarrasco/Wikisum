from flask_restful import Resource, Api
from flask import Flask
from wikisort import wordRelevance
from wikisort import summaries

app = Flask(__name__)
api = Api(app)

class WikiTitle(Resource):
    def get(self,topic):
        return {'titles': wordRelevance(topic)}

class WikiSummary(Resource):
    def get(self,topic):
        return {'summaries': summaries(topics)}

    

api.add_resource(WikiTitle, '/wiki/<string:topic>/titles')
api.add_resource(WikiSummary, '/wiki/<string:titles>/summaries')

if __name__ == '__main__':
    app.run(debug=True)

