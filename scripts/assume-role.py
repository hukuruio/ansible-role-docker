import os

import boto3

region = 'eu-west-2'
aws_profile_name = 'mad-dev-token'
account_id = os.environ.get('ACCOUNT_ID')
aws_role_arn = f"arn:aws:iam::${account_id}:role/admin"

session = boto3.Session(profile_name=aws_profile_name)

sts_client = session.client('sts')
assumed_role_object = sts_client.assume_role(
    RoleArn=aws_role_arn,
    RoleSessionName="AssumeRoleSession1"
)

credentials = assumed_role_object['Credentials']
access_key_id = credentials['AccessKeyId']
secret_access_key = credentials['SecretAccessKey']
session_token = credentials['SessionToken']


session = boto3.Session(
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token,
)

bash_data = f"""#!/usr/bin/env bash
export AWS_ACCESS_KEY_ID={credentials['AccessKeyId']}
export AWS_SECRET_ACCESS_KEY={credentials['SecretAccessKey']}
export AWS_SESSION_TOKEN={credentials['SessionToken']}
export AWS_ACCESS_KEY={credentials['AccessKeyId']}
export AWS_SECRET_KEY=={credentials['SecretAccessKey']}
export AWS_SECURITY_TOKEN={credentials['SessionToken']}
export AWS_DEFAULT_REGION={region}
"""

print(bash_data)
