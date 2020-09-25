#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Getter & setter for AWS IAM

# Import AWS module for python
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Define AWS Config class to get/set IAM Roles using Boto3
class roles:
    
    #Class constructor
    def __init__(self, region):
        self.region = region
        self.iam_resource = boto3.resource('iam', region_name=self.region)
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        self.table = self.dynamodb.Table('tag_tamer_roles')

    #Return the list of IAM Roles for the specified path prefix
    def get_roles(self, path_prefix):
        raw_roles_inventory = self.iam_resource.roles.filter(
            PathPrefix=path_prefix
        )
        roles_inventory = list()
        for raw_role in raw_roles_inventory:
            roles_inventory.append(raw_role.role_name)

        roles_inventory.sort(key=str.lower)

        return roles_inventory

    #Get a specified role and assigned tags 
    def get_role_tags(self, role_arn):
        response = dict()
        response = self.table.get_item(
            Key={
                'role_arn': role_arn
            },
            ProjectionExpression="tags"
        )
        tags = list()
        tags = response['Item']['tags']
        return tags

    #Create a new role to tags mapping
    def set_role_tags(self, role_name, tags):
        role = self.iam_resource.Role(role_name)
        put_item_response = self.table.put_item(
            Item={
                "role_arn": role.arn,
                "tags": tags,
            },
            ReturnValues='NONE'
        )
        return put_item_response
