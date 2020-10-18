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
    
    # Class constructor
    def __init__(self, resource_type, region):
        self.resource_type = resource_type
        self.region = region

    # Returns a filtered list of all resource names & ID's for the resource type specified  
    def get_lambda_names_ids(self, filter_tags):
        self.filter_tags = filter_tags
        resource_inventory = dict()
        
        if self.filter_tags.get('conjunction') == 'AND':
            
            def _and_tfff(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') in tag_dict:
                    resource_inventory[function_name] = function_arn
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'
            
            def _and_ttff(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key1')] == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_name] = function_arn
                    else:
                        resource_inventory['No matching resource'] = 'No matching resource'
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'

            def _and_tftf(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') and self.filter_tags.get('tag_key2') in tag_dict:
                    resource_inventory[function_name] = function_arn
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'
            
            def _and_tftt(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') and self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key2')] == self.filter_tags.get('tag_value2'):
                        resource_inventory[function_name] = function_arn
                    else:
                        resource_inventory['No matching resource'] = 'No matching resource'
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'
            
            def _and_tttf(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') and self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key1')] == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_name] = function_arn
                    else:
                        resource_inventory['No matching resource'] = 'No matching resource'
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'
            
            def _and_tttt(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') and self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key1')] == self.filter_tags.get('tag_value1'):
                        if tag_dict[self.filter_tags.get('tag_key2')] == self.filter_tags.get('tag_value2'):
                            resource_inventory[function_name] = function_arn
                        else:
                            resource_inventory['No matching resource'] = 'No matching resource'
                    else:
                        resource_inventory['No matching resource'] = 'No matching resource'
                else:
                        resource_inventory['No matching resource'] = 'No matching resource'

            def _and_ffff(tag_dict, function_name, function_arn):
                resource_inventory[function_name] = function_arn

            # "AND" Truth table check for tag_key1, tag_value1, tag_key2, tag_value2
            and_valid_combos = {
                (True, False, False, False): _and_tfff,
                (True, True, False, False): _and_ttff,
                (True, False, True, False): _and_tftf,
                (True, False, True, True): _and_tftt,
                (True, True, True, False): _and_tttf,
                (True, True, True, True): _and_tttt,
                (False, False, False, False): _and_ffff
            }
                
            try:
                client = boto3.client(self.resource_type, region_name=self.region)
                # Get all the Lambda functions in the region
                my_functions = client.list_functions()
                for item in my_functions['Functions']:
                    try:
                        # Get all the tags for a given Lambda function
                        response = client.list_tags(
                            Resource=item['FunctionArn']
                        )
                        if response.get('Tags'):
                            and_valid_combos[(self.filter_tags.get('tag_key1'),
                                self.filter_tags.get('tag_value1'),
                                self.filter_tags.get('tag_key2'),
                                self.filter_tags.get('tag_value2'))](response.get('Tags'), item['FunctionName'], item['FunctionArn'])
                    
                    except botocore.exceptions.ClientError as error:
                            log.error("Boto3 API returned error: {}".format(error))
            except botocore.exceptions.ClientError as error:
                            log.error("Boto3 API returned error: {}".format(error))

        if self.filter_tags.get('conjunction') == 'OR':

            def _or_tfff_tftf_fftf(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') or self.filter_tags.get('tag_key2') in tag_dict:
                    resource_inventory[function_name] = function_arn
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'
            
            def _or_tttf(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key1') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key1')] == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_name] = function_arn
                elif self.filter_tags.get('tag_key2') in tag_dict:
                    resource_inventory[function_name] = function_arn
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'

            def _or_tftt(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key2')] == self.filter_tags.get('tag_value2'):
                        resource_inventory[function_name] = function_arn
                elif self.filter_tags.get('tag_key1') in tag_dict:
                    resource_inventory[function_name] = function_arn
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'

            def _or_fftt(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key2')] == self.filter_tags.get('tag_value2'):
                        resource_inventory[function_name] = function_arn
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'
            
            def _or_ttff(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key1') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key1')] == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_name] = function_arn
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'

            def _or_tttt(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key1') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key1')] == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_name] = function_arn
                elif  self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key2')] == self.filter_tags.get('tag_value2'):
                        resource_inventory[function_name] = function_arn
                else:
                    resource_inventory['No matching resource'] = 'No matching resource'
            
            def _or_ffff(tag_dict, function_name, function_arn):
                resource_inventory[function_name] = function_arn

            # "OR" Truth table check for tag_key1, tag_value1, tag_key2, tag_value2
            or_valid_combos = {
                (False, False, True, False): _or_tfff_tftf_fftf,
                (False, False, True, True): _or_fftt,
                (True, False, False, False): _or_tfff_tftf_fftf,
                (True, False, True, False): _or_tfff_tftf_fftf,
                (True, False, True, True): _or_tftt,
                (True, True, False, False): _or_ttff,
                (True, True, True, False): _or_tttf,
                (True, True, True, True): _or_tttt,
                (False, False, False, False): _or_ffff
            }
                
            try:
                client = boto3.client(self.resource_type, region_name=self.region)
                # Get all the Lambda functions in the region
                my_functions = client.list_functions()
                for item in my_functions['Functions']:
                    try:
                        # Get all the tags for a given Lambda function
                        response = client.list_tags(
                            Resource=item['FunctionArn']
                        )
                        if response.get('Tags'):
                            or_valid_combos[(self.filter_tags.get('tag_key1'),
                                self.filter_tags.get('tag_value1'),
                                self.filter_tags.get('tag_key2'),
                                self.filter_tags.get('tag_value2'))](response.get('Tags'), item['FunctionName'], item['FunctionArn'])
                    
                    except botocore.exceptions.ClientError as error:
                            log.error("Boto3 API returned error: {}".format(error))
            except botocore.exceptions.ClientError as error:
                            log.error("Boto3 API returned error: {}".format(error))
            
        return resource_inventory            


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