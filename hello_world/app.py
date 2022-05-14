import constants
import urllib
import aws_utility
import time
import os
import boto3

print("Getting Values from environment variable")
try:
    DYNAMO_TABLE_NAME = os.getenv('DYNAMO_TABLE_NAME')
    SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')
    ERROR_BUCKET = os.getenv('ERROR_BUCKET')
except Exception as error:
    print("Exception occurred while getting environment variable" + error)


def lambda_handler(event, context):
    for record in event['Records']:

        if record['eventSource'] != 'aws:s3':
            print('Trigger is not from s3. Skipping Processing')
            return
        try:
            start_time = time.strftime('%Y%m%d_%H%M%S')
            print("Getting bucket name and filename")
            bucket_name = record['s3']['bucket']['name']
            # Get key replacing %xx of url-encoded value by equivalent character
            file_name = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding="utf-8")
            aws_utility.save_file_csv(bucket_name, file_name)
            aws_utility.send_sns_message(SNS_TOPIC_ARN, constants.SUCCESS_SNS_SUBJECT, "Data inserted Successfully")
        except Exception as e:
            end_time = time.strftime('%Y%m%d_%H%M%S')
            print(f'Error summarizing file: {file_name}.', e)
            aws_utility.transfer_file(bucket_name, ERROR_BUCKET, file_name)
            aws_utility.delete_s3_file(bucket_name, file_name)
            error_message = f'Error occurred while processing the file: {file_name}. ' \
                            f'Please check error file in Bucket: {ERROR_BUCKET} with FileName: {file_name}.' \
                            f'\n\nThe error message encountered was {str(e)}'

            print("Sending notification message in mail")
            aws_utility.send_sns_message(SNS_TOPIC_ARN, constants.FAILED_SNS_SUBJECT, error_message)
            dynamo_data = {'id': start_time, 'EndTime': end_time, 'FileName': file_name, 'Status': 'Failure',
                           'FailureReason': str(e), 'ErrorPhase': 'Summarizing transaction and inserting to RDS'}

            print("Uploading fail message in DynamoDB")
            aws_utility.upload_to_dynamo(DYNAMO_TABLE_NAME, dynamo_data)
