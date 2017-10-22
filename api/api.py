from flask_restful import Resource, Api
from flask import Flask
from wikisort import wordRelevance

app = Flask(__name__)
api = Api(app)

class WikiInfo(Resource):
    def get(self,topic):
        return {'summary': wordRelevance(topic)}

    


api.add_resource(WikiInfo, '/wiki/<string:topic>')

if __name__ == '__main__':
    app.run(debug=True)


# wordRelevance('iPhone')

wordRelevance('Python Language')

#use summary links
