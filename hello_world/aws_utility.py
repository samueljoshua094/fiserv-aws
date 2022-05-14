from typing import Any
import boto3
import os

from botocore.exceptions import ClientError

try:
    DYNAMO_TABLE_NAME1 = os.getenv('DYNAMO_TABLE_NAME1')
    REGION_NAME = os.getenv('REGION_NAME')
except Exception as error:
    print("Exception occurred while getting environment variable" + error)


def delete_s3_file(bucket, key):
    try:
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, key).delete()
    except Exception as e:
        raise Exception(e)


def get_file_from_s3(bucket_name, file_name, with_delete=False):
    try:
        s3 = boto3.client("s3")
        file_from_s3 = s3.get_object(Bucket=bucket_name, Key=file_name)
        file_content = file_from_s3["Body"].read().decode('utf-8-sig')

        if with_delete:
            delete_s3_file(bucket_name, file_name)

        return file_content, file_name

    except Exception as e:
        raise Exception(e)


def upload_to_s3(file_content, bucket_name, file_name):
    try:
        s3_resource = boto3.resource('s3')
        object_handler = s3_resource.Object(bucket_name, file_name)
        object_handler.put(Body=bytes(file_content, encoding="utf-8"))
    except Exception as e:
        raise Exception(e)


def send_sns_message(sns_topic_arn, sns_subject, sns_message):
    try:
        sns_client = boto3.client('sns')
        sns_client.publish(TopicArn=sns_topic_arn, Message=sns_message, Subject=sns_subject)
    except Exception as e:
        raise Exception(e)


def upload_to_dynamo(table_name, data_to_push):
    try:
        dynamodb_resource = boto3.resource('dynamodb')
        dynamodb_table = dynamodb_resource.Table(table_name)
        dynamodb_table.put_item(Item=data_to_push)
    except Exception as e:
        raise Exception(e)


def save_file_csv(bucket_name, file_name):
    try:
        print(f"Trigger is due to file: {file_name} in bucket: {bucket_name}")
        s3 = boto3.client("s3", region_name=REGION_NAME)
        dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)
        productTable: Any = dynamodb.Table(DYNAMO_TABLE_NAME1)
        s3 = boto3.client("s3")
        resp = s3.get_object(Bucket=bucket_name, Key=file_name)
        data = resp['Body'].read().decode('utf-8-sig')
        products = data.strip().split('\n')
        number = 1
        for prod in products:
            number = number + 1
            product = prod.split(',')
            productTable.put_item(
                Item={
                    "id": number,
                    "productName": product[0],
                    "qunatity": product[1],
                    "price": product[2],
                    "quantityleft": product[3]
                }
            )
            print("Data inserted into database")
    except Exception as e:
        raise Exception(e)

    def transfer_file(source_bucket,
                      destination_bucket, filename):
        try:
            s3_resource = boto3.resource('s3')
            source = {
                'Bucket': source_bucket,
                'Key': filename
            }
            s3_resource.meta.client.copy(source, destination_bucket, filename)
        except ClientError as e:
            print(e)
            raise Exception(e)
