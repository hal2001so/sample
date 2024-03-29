import json
import os
import boto3

ddb= boto3.resource('dynamodb')
table= ddb.Table(os.environ['HITS_TABLE_NAME'])
_lambda= boto3.client('lambda')

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    table.update_item(
        Key={'path': event['path']},
        UpdateExpression='ADD hits :incr',
        ExpressionAttributesValues={':incr': 1}
    )

    resp = _lambda.invoke(
        FunctionName=os.environ['DOWNSTREAM_FUNCTION_NAME'], # Calls the downstream function name value from the hitcounter construct after logging the hit in Dynamodb.
        Payload=json.dumps(event),
    )

    body = resp['Payload'].read()

    print('downstream response: {}'.format(body))
    return json.loads(body)