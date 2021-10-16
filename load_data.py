import requests
import pandas as pd
import json


def load_file_to_dynamo(file_path, separator):

    df = pd.read_csv(file_path, sep=separator)
    df = df.convert_dtypes()

    df['document'] = df['document'].astype(str)

    df = df.head(3)

    json_string = df.to_json(orient='records')
    request = json.loads(json_string)

    with open('sample.json', 'w') as outfile:
        json.dump(request,  outfile)

    url = 'https://a54xl41d56.execute-api.us-east-2.amazonaws.com/Prod/clients'
    headers = {'Content-Type': 'application/json'}

    for register in request:
        r = requests.post(url, data=json.dumps(register), headers=headers)
        print(r.text)
    

if __name__ == '__main__':

    load_file_to_dynamo('db_client_registers.csv', ',')
