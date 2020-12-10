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

log = logging.getLogger(__name__)

# Function to return the authenticated user's user pool group ARN's
def get_user_group_arns(user_name, user_pool_id, region):
    try:
        cognito_idp_groups = dict()
        cognito_idp_client = boto3.client('cognito-idp', region_name=region)
        cognito_idp_groups = cognito_idp_client.admin_list_groups_for_user(
            Username=user_name,
            UserPoolId=user_pool_id
        )
        # initially support one Cognito user pool group per user
        group_role_arn = cognito_idp_groups['Groups'][0]['RoleArn'] if cognito_idp_groups.get('Groups') else False
    except botocore.exceptions.ClientError as error:
        log.error("Boto3 API returned error: {}".format(error))
        group_role_arn = False
    return group_role_arn

# Inputs: cognito_id_token = user's returned id_token JWT
def get_user_credentials(cognito_id_token, user_pool_id, identity_pool_id, region):
    user_credentials = dict()
    idp_name = 'cognito-idp.' + region + '.amazonaws.com/' + user_pool_id

    try:
        cognito_identity_client = boto3.client('cognito-identity', region_name=region)
        identity_id_response = cognito_identity_client.get_id(
            IdentityPoolId=identity_pool_id,
            Logins={
                idp_name: cognito_id_token
            }
        )
        log.debug('The Cognito identity is: %s', identity_id_response)
        identity_id = identity_id_response['IdentityId']
        cognito_identity_response = cognito_identity_client.get_credentials_for_identity(
            IdentityId=identity_id,
            Logins={
                idp_name: cognito_id_token
            }
        )
        log.debug('The Cognito user credentials are: %s', cognito_identity_response)
        user_credentials['AccessKeyId'] = cognito_identity_response['Credentials']['AccessKeyId']
        user_credentials['SecretKey'] = cognito_identity_response['Credentials']['SecretKey']
        user_credentials['SessionToken'] = cognito_identity_response['Credentials']['SessionToken']

    except botocore.exceptions.ClientError as error:
            log.error("Boto3 API returned error: {}".format(error))
            user_credentials['AccessKeyId'] = None
            user_credentials['SecretKey'] = None
            user_credentials['SessionToken'] = None
    return user_credentials