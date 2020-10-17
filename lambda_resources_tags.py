#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# Getters & Setters for AWS Lambda function resource tags
#  This class supports the main "resources_tags" class
# Included class & methods
# class - lambda_resources_tags
#  method - get_lambda_names_ids
#  method - get_lambda_resources_tags
#  method - get_lambda_tag_keys
#  method - get_lambda_tag_values
#  method - set_lambda_resources_tags


# Import AWS module for python
import boto3, botocore
# Import collections to use ordered dictionaries for storage
from collections import OrderedDict
# Import logging module
import logging
# Import Python's regex module to filter Boto3's API responses 
import re

# Instantiate logging for this module using its file name
log = logging.getLogger(__name__)

# Define resources_tags class to get/set resources & their assigned tags
class lambda_resources_tags:
    
    #Class constructor
    def __init__(self, resource_type, region):
        self.resource_type = resource_type
        self.region = region

    #Returns a sorted list of all resources for the resource type specified  
    def get_lambda_names_ids(self):
        pass

    # method - get_lambda_resources_tags
    # Returns a nested dictionary of every resource & its key:value tags for the chosen resource type
    # No input arguments
    def get_lambda_resources_tags(self, **filter_tags):
        # Instantiate dictionaries to hold resources & their tags
        tagged_resource_inventory = dict()
        try:
            client = boto3.client(self.resource_type, region_name=self.region)
            # Get all the Lambda functions in the region
            my_functions = client.list_functions()
            for item in my_functions['Functions']:
                resource_tags = {}
                sorted_resource_tags = {}
                function_arn = item['FunctionArn']
                try:
                    # Get all the tags for a given Lambda function
                    response = client.list_tags(
                        Resource=function_arn
                    )
                    for tag_key, tag_value in response['Tags'].items():       
                        if not re.search("^aws:", tag_key):
                            resource_tags[tag_key] = tag_value

                except botocore.exceptions.ClientError as error:
                    log.error("Boto3 API returned error: {}".format(error))
                    resource_tags["No Tags Found"] = "No Tags Found"
                sorted_resource_tags = OrderedDict(sorted(resource_tags.items()))
                tagged_resource_inventory[item['FunctionName']] = sorted_resource_tags
        except botocore.exceptions.ClientError as error:
            log.error("Boto3 API returned error: {}".format(error))
            tagged_resource_inventory["No Resource Found"] = {"No Tags Found": "No Tags Found"}
        return tagged_resource_inventory

    # method - get_lambda_tag_keys
    # Getter method retrieves every tag:key for object's resource type
    # No input arguments
    def get_lambda_tag_keys(self):
        tag_keys_inventory = list()
        try:
            client = boto3.client(self.resource_type, region_name=self.region)
            # Get all the Lambda functions in the region
            my_functions = client.list_functions()
            for item in my_functions['Functions']:
                function_arn = item['FunctionArn']
                try:
                    # Get all the tags for a given Lambda function
                    response = client.list_tags(
                        Resource=function_arn
                    )
                    try:
                        # Add all tag keys to the list
                        for tag_key, _ in response['Tags'].items():       
                            if not re.search("^aws:", tag_key):
                                tag_keys_inventory.append(tag_key)
                    except:
                        tag_keys_inventory.append("No tag keys found")

                except botocore.exceptions.ClientError as error:
                    log.error("Boto3 API returned error: {}".format(error))
                    tag_keys_inventory.append("No tag keys found")
                
        except botocore.exceptions.ClientError as error:
            log.error("Boto3 API returned error: {}".format(error))
            tag_keys_inventory.append("No tag keys found")
        return tag_keys_inventory


    # method - get_lambda_tag_values
    # Getter method retrieves every tag:value for object's resource type
    # No input arguments
    def get_lambda_tag_values(self):
        tag_values_inventory = list()
        try:
            client = boto3.client(self.resource_type, region_name=self.region)
            # Get all the Lambda functions in the region
            my_functions = client.list_functions()
            for item in my_functions['Functions']:
                function_arn = item['FunctionArn']
                try:
                    # Get all the tags for a given Lambda function
                    response = client.list_tags(
                        Resource=function_arn
                    )
                    try:
                        # Add all tag keys to the list
                        for tag_key, tag_value in response['Tags'].items():       
                            # Exclude any AWS-applied tags which begin with "aws:"
                            if not re.search("^aws:", tag_key):
                                tag_values_inventory.append(tag_value)
                    except:
                        tag_values_inventory.append("No tag values found")

                except botocore.exceptions.ClientError as error:
                    log.error("Boto3 API returned error: {}".format(error))
                    tag_values_inventory.append("No tag values found")
                
        except botocore.exceptions.ClientError as error:
            log.error("Boto3 API returned error: {}".format(error))
            tag_values_inventory.append("No tag values found")
        return tag_values_inventory

    def set_lambda_resources_tags(self):
        pass