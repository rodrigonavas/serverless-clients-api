import simplejson as json
import boto3
from decimal import Decimal
from flask_lambda import FlaskLambda
from flask import request

app = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('clients')


@app.route('/')
def test():
    data = {
        'message': 'Hello, world!'
    }
    return json_response(data)


@app.route('/clients', methods=['GET', 'POST'])
def put_or_list_students():

    print('Request: ')
    print(request)

    if request.method == 'GET':
        clients = table.scan()['Items']
        return json_response(clients)
    else:
        print('Request get data: ')
        print(request.json)

        data = json.loads(json.dumps(request.json), parse_float=Decimal)

        table.put_item(Item=data)
        return json_response({'message': 'Client register created'})


@app.route('/clients/<document>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_clients(document):

    print('Request: ')
    print(request)

    key = {'document': document}

    if request.method == 'GET':
        client = table.get_item(Key=key)['Item']
        if client:
            return json_response(client)
        else:
            return json_response({"message": "Client registers not found"}, 404)
    elif request.method == 'PATCH':
        print('Request get data: ')
        print(request.json)

        data = json.loads(json.dumps(request.json), parse_float=Decimal)

        attribute_updates = {each: {'Value': value, 'Action': 'PUT'}
                             for each, value in data.items()}

        table.update_item(Key=key, AttributeUpdates=attribute_updates)
        return json_response({'message': 'Client register updated'})
    else:
        table.delete_item(Key=key)
        return json_response({'message': 'Client register deleted'})


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
