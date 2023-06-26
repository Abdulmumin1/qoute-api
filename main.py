import json
from flask import Flask, request
from flask_restful import Resource, Api
import pprint
import random

app = Flask(__name__)
api = Api(app)

qoutes_json = None

with open('quote.json', 'r') as qts:
    qoutes_json = json.loads(qts.read())


def write_new_qoute(data):
    new = []
    with open('new_qoutes.json', 'r') as qts:
        existing_qoutes = qts.read()
        new = json.loads(existing_qoutes) if existing_qoutes else []
        new.append(json.loads(data))
        json.dump(new, open('new_qoutes.json', 'w'), indent=2)


def qoute_by_id(id_):
    try:
        return [i for i in qoutes_json if i['id'] == id_][0]
    except:
        return 'Not Found!'


def get_qoutes_from_author(author):
    result = [i for i in qoutes_json if str(
        i['author']).lower() == author.lower()]
    try:
        return random.choice(result)
    except:
        return f"No qoutes found from {author}"


def get_random_qoute():
    return random.choice(qoutes_json)


class Qoute(Resource):
    def get(self):
        return get_random_qoute()

    def post(self):
        author = request.form['author']
        if author:
            return get_qoutes_from_author(author)
        return "Not Found!"


class QouteID(Resource):
    def get(self, qoute_id):
        return qoute_by_id(qoute_id)

    def delete(self, qoute_id):

        return


api.add_resource(Qoute, '/random')
api.add_resource(QouteID, '/<int:qoute_id>')


if __name__ == '__main__':
    app.run(debug=True)
    # write_new_qoute(
    #     {'author': 'abdul', 'quote': 'Observation is the secret to discovery!'})
    # pprint.pprint(get_qoutes_by_author('Steve Jobs'))
    # add_id()
    # print(qoute_by_id('1'))
