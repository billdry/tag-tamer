#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# Purpose - functions to retrieve information regarding Amazon Cognito 
# user pools & users

# Import AWS module for python
import botocore
import boto3
# Import logging module
import logging
# Import random number generator
import random

log = logging.getLogger(__name__)

# Function to return the temporary session credentials for given AWS IAM Role
def get_session_credentials(role_arn, user_name, region):
    session_credentials = dict()
    role_session_name = user_name + "-session-" + str(random.randint(1,100))
    try:
        client = boto3.client('sts', region_name=region)
        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
        )
        session_credentials = response['Credentials']
    except botocore.exceptions.ClientError as error:
        log.error("Boto3 API returned error: {}".format(error))
        session_credentials['AccessKeyId'] = None
        session_credentials['SecretKey'] = None
        session_credentials['SessionToken'] = None
    return session_credentials

