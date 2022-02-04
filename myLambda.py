import json
import boto3

#Creating client connection with s3 service and create s3SSLEnable policy
s3 = boto3.client('s3')

def checkExistingPolicy(bucketName):
    try:
        response = s3.get_bucket_policy(
            Bucket=bucketName,
        )
        if response is not None:
            print("{} bucket has already policy enabled so appending new policy in it.".format(bucketName))
            
            # #Appending s3SSL policy into exisitng policy
            user_policy = {
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
            # Converting actual into dict
            respToDict = json.loads(response['Policy'])
            # print(type(respToDict))
            
            a_user_policy = user_policy.copy()
            respToDict['Statement'].append(a_user_policy)
            
            #Converting dict to str as policy accept in string only
            newPol = json.dumps(respToDict)
            resp = s3.put_bucket_policy(Bucket=bucketName,Policy=newPol)
            # print(resp)
            return 500 
    except s3.exceptions.from_code('NoSuchBucketPolicy') as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            create_bucket_policy(bucketName)
            # print("Policy has been enabled for " + bucketName)
            return 204
    
def create_bucket_policy(bucketName):
    try:
        #Policy Content
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
        #Convert Policy into json
        policy_string = json.dumps(bucket_policy)
        
    except Exception as e:
        print(e)
    resp = s3.put_bucket_policy(Bucket=bucketName,Policy=policy_string)
    status = resp['ResponseMetadata']['HTTPStatusCode']
    return status


def lambda_handler(event, context):
    status = checkExistingPolicy("qa-mayank-koli-platform-challenge")
    if status == 204:
        return {'body': json.dumps('Policy Implement')}
    elif status == 500:
        return {'body': json.dumps('Appended in existing Policy')}
    else:
        return {'body': json.dumps('Error in Policy or code')}
    
