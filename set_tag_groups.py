#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Setter updating tag groups in DynamoDB

# Import AWS module for python
import botocore
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Import logging module
import logging
log = logging.getLogger(__name__)

#This class instantiates & updates Tag Tamer Tag Groups
class set_tag_group:

    #Class constructor
    def __init__(self, region):
        self.region = region
        self.tag_groups = {}
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        self.table = self.dynamodb.Table('tag_tamer_tag_groups')
    
    #Setter to instantiate a new Tag Group adding its tag key & range of tag values
    def create_tag_group(self, tag_group_name, tag_group_key_name, tag_group_value_options):
        if(len(tag_group_name) and len(tag_group_key_name)):
            try:
                put_item_response = self.table.put_item(
                    Item={
                        "tag_group_name": tag_group_name,
                        "resource_type": "all",
                        "key_name": tag_group_key_name,
                        "key_values": tag_group_value_options
                    },
                    ReturnValues='NONE',
                )
                log.info('Successfully created Tag Group \"%s\" with Key \"%s\" & possible values \"%s\"', tag_group_name, tag_group_key_name, tag_group_value_options)

            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {}"
                log.error(errorString.format(error))
                put_item_response = errorString.format(error)
        else:
            print("Please provide a value for Tag Group name and Tag Key name")
            log.warning("Please provide a value for Tag Group name and Tag Key name")
            put_item_response = "Please provide a value for Tag Group name and Tag Key name"
        return put_item_response


    #Setter to update a tag's possible range of values
    def update_tag_group(self, tag_group_name, tag_group_key_name, tag_group_value_options):
        try:
            update_item_response = self.table.update_item(
                Key={
                    "tag_group_name": tag_group_name
                },
                UpdateExpression="set resource_type = :rt, key_name = :kn, key_values = :kv",
                ExpressionAttributeValues={
                    ":rt": "all",
                    ":kn": tag_group_key_name,
                    ":kv": tag_group_value_options
                },
                ReturnValues='NONE',
            )
            log.info('Successfully updated Tag Group \"%s\" with Key \"%s\" to possible values \"%s\"', tag_group_name, tag_group_key_name, tag_group_value_options)

        except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {}"
                log.error(errorString.format(error))
                update_item_response = errorString.format(error)
        return update_item_response

