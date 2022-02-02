import json
import urllib.parse
import boto3

print('Loading function')

#s3_client = boto3.client('s3')

def create_bucket_policy(s3bucket):
    
    
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowSSLRequestsOnly",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": ["arn:aws:s3:::{}/*".format(s3bucket), "arn:aws:s3:::{}".format(s3bucket)],
                "Condition": {
                    "Bool": {
                    "aws:SecureTransport": "false"
                           }
                    }
            }
        ]
    }
    

    #json.dumps(bucket_policy)
    #data=json.loads(policystring)

    print(bucket_policy)


def lambda_handler(event, context):
    create_bucket_policy("mayank")
