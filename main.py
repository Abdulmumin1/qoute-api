import json
import os
from flask import Flask, request
from flask_restful import Resource, Api
import pprint
import random

app = Flask(__name__)
api = Api(app)

# qoutes_json = None
qoute_db = 'new_qoutes.json'
with open(qoute_db, 'r') as qts:
    qoutes_json = json.loads(qts.read())


def write_new_qoute(data):
    new = []
    with open(qoute_db, 'r') as qts:
        existing_qoutes = qts.read()
        new = json.loads(existing_qoutes) if existing_qoutes else []
        data = json.loads(data)
        data['id'] = new[-1]['id']+1
        new.append(data)
        json.dump(new, open(qoute_db, 'w'), indent=2)


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


def delete_qoute(id_):
    updated_qoutes = []
    with open(qoute_db, 'r') as qts:
        existing_qoutes = qts.read()
        existing_qoutes = json.loads(existing_qoutes)
        updated_qoutes = filter(
            lambda x: x['id'] != id_, existing_qoutes)
        json.dump(list(updated_qoutes), open(qoute_db, 'w'), indent=2)


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
        delete_qoute(qoute_id)
        return "Success", 201


class New(Resource):
    def post(self):
        data = request.form['data']
        print(request.form)
        write_new_qoute(data)
        return "sucess", 201


class Hello(Resource):
    def get(self):
        return """
        GET - <strong>/random</strong> get a random qoute
        POST - <strong>/random</strong> author="name" get random qoute from author
        POST - <strong>/new</strong> data={} post new qoute to database
        GET  - <strong>/:id</strong> get qoute with specific ID
        DELETE - <strong>/:id</strong> delte qoute with specific ID
        """


api.add_resource(Hello, '/')
api.add_resource(Qoute, '/random')
api.add_resource(New, '/new')
api.add_resource(QouteID, '/<int:qoute_id>')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    # write_new_qoute(
    #     {'author': 'abdul', 'quote': 'Observation is the secret to discovery!'})
    # pprint.pprint(get_qoutes_by_author('Steve Jobs'))
    # add_id()
    # print(qoute_by_id('1'))
    # delete_qoute(3)
