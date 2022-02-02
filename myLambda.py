import json
import boto3

def create_bucket_policy(bucketName):
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowSSSLRequestsOnly",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": ["arn:aws:s3:::{}/*".format(bucketName), "arn:aws:s3:::{}".format(bucketName)],
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                }
            }
        ]
    }
    policy_string = json.dumps(bucket_policy)
    
    s3 = boto3.client('s3')
    s3.put_bucket_policy(
        Bucket=bucketName,
        Policy=policy_string
    )
        

def lambda_handler(event, context):
    create_bucket_policy("qa-mayank-koli-platform-challenge")
    return {
        'statusCode': 200,
        'body': json.dumps('Policy Implement')
    }