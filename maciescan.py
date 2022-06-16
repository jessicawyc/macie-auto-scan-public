import json
import boto3
import os
import datetime

def lambda_handler(event, context):
    #读取security hub imported finding,不能用于insight
    finding=event['detail']['findings'][0]
    Title=finding["Title"]
    if Title != 'Block Public Access settings are disabled for the S3 bucket':
        return ('Skipping for the wrong finding' )
    else:
        s3arn = finding["Resources"][0]['Id']
        region = finding["Resources"][0]['Region']
        AccountId=finding['AwsAccountId']
        s3name=s3arn[13:]
        print(s3name)
        x = datetime.datetime.now()
        jobname=s3name+'at'+str(x)
 #trigger macie to start a scan
        client = boto3.client('macie2',region_name=region)
        response = client.create_classification_job(
        description='auto scan a new public s3 from securityhub alert to check data',
        initialRun=True,
        jobType='ONE_TIME',
        name=jobname,
        s3JobDefinition={
            'bucketDefinitions': [
                {
                    'accountId': AccountId,
                    'buckets': [ s3name ]
                }
            ]})
    return(response)     

