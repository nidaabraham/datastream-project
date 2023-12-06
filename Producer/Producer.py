import json
import base64
import boto3

def lambda_handler(event, context):
    
    kinesis = boto3.client('kinesis')
    stream_name = "datastream_1"
    partition_key = '123'
    
    data = json.loads(event["body"])
    
    print(data)
    
    try:
        for record in data:
            payload = bytes(json.dumps(record), 'utf-8')
            response = kinesis.put_record(StreamName=stream_name, Data=payload, PartitionKey=partition_key)
            print(response)
            
            return {
                'statusCode': 200,
                'body': json.dumps('Good')
            }
    except Exception as e:
        print("Error", e)
        return {
                'statusCode': 403,
                'body': json.dumps('Not good', e)
            }
