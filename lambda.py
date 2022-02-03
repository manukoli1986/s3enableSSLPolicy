import json
import boto3
# import botocore.exceptions



#Creating client connection with s3 service and create s3SSLEnable policy
s3 = boto3.client('s3')
    

def checkExistingPolicy(bucketName):
    try:
        response = s3.get_bucket_policy(
            Bucket=bucketName,
        )
        if response is not None:
            print("{} bucket has already policy enabled.".format(bucketName))
               
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
            res = json.loads(response['Policy'])
            appendedPolicy = res['Statement'].append(user_policy)
            resp = s3.put_bucket_policy(Bucket=bucketName,Policy=appendedPolicy)
            
            print(resp)
            

            return 500 
    except s3.exceptions.from_code('NoSuchBucketPolicy') as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            create_bucket_policy(bucketName)
            print("Policy has been enabled for " + bucketName)
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
    
checkExistingPolicy("qa-mayank-koli-platform-challenge")
# status = checkExistingPolicy("qa-mayank-koli-platform-challenge")
# if status == 204:
#     print("204")
# else:
#     print('Error in Policy or code')

# https://stackoverflow.com/questions/34898335/amazon-s3-modify-bucket-policy-using-boto-boto3
