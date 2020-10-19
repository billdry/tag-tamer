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
        tag_key1_state = True if self.filter_tags.get('tag_key1') else False
        tag_value1_state = True if self.filter_tags.get('tag_value1') else False
        tag_key2_state = True if self.filter_tags.get('tag_key2') else False
        tag_value2_state = True if self.filter_tags.get('tag_value2') else False
        resource_inventory = dict()

        def _intersection_union_invalid(tag_dict, function_name, function_arn):
            resource_inventory['No matching resource'] = 'No matching resource'
        
        if self.filter_tags.get('conjunction') == 'AND':
            
            def _intersection_tfff(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') in tag_dict:
                    resource_inventory[function_arn] = function_name
            
            def _intersection_fftf(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key2') in tag_dict:
                    resource_inventory[function_arn] = function_name
                     
            def _intersection_fftt(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict.get(self.filter_tags.get('tag_key2')) == self.filter_tags.get('tag_value2'):
                        resource_inventory[function_arn] = function_name             
            
            def _intersection_ttff(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') in tag_dict:
                    if tag_dict.get(self.filter_tags.get('tag_key1')) == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_arn] = function_name                   

            def _intersection_tftf(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') in tag_dict and self.filter_tags.get('tag_key2') in tag_dict:
                    resource_inventory[function_arn] = function_name
                         
            def _intersection_tftt(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') in tag_dict and self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict.get(self.filter_tags.get('tag_key2')) == self.filter_tags.get('tag_value2'):
                        resource_inventory[function_arn] = function_name
                            
            def _intersection_tttf(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') in tag_dict and self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict.get(self.filter_tags.get('tag_key1')) == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_arn] = function_name
                         
            def _intersection_tttt(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') in tag_dict and self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict.get(self.filter_tags.get('tag_key1')) == self.filter_tags.get('tag_value1'):
                        if tag_dict.get(self.filter_tags.get('tag_key2')) == self.filter_tags.get('tag_value2'):
                            resource_inventory[function_arn] = function_name                   

            def _intersection_ffff(tag_dict, function_name, function_arn):
                resource_inventory[function_arn] = function_name

            # "AND" Truth table check for tag_key1, tag_value1, tag_key2, tag_value2
            intersection_combos = {
                (False, False, False, True): _intersection_union_invalid,
                (False, True, False, False): _intersection_union_invalid,
                (False, True, False, True): _intersection_union_invalid,
                (True, False, False, True): _intersection_union_invalid,
                (True, True, False, True): _intersection_union_invalid,
                (False, True, True, False): _intersection_union_invalid,
                (False, False, True, False): _intersection_fftf,
                (False, False, True, True): _intersection_fftt,
                (True, False, False, False): _intersection_tfff,
                (True, True, False, False): _intersection_ttff,
                (True, False, True, False): _intersection_tftf,
                (True, False, True, True): _intersection_tftt,
                (True, True, True, False): _intersection_tttf,
                (True, True, True, True): _intersection_tttt,
                (False, False, False, False): _intersection_ffff
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
                    except botocore.exceptions.ClientError as error:
                            log.error("Boto3 API returned error: {}".format(error))
                    intersection_combos[(tag_key1_state,
                        tag_value1_state,
                        tag_key2_state,
                        tag_value2_state)](response.get('Tags'), item['FunctionName'], item['FunctionArn'])
            except botocore.exceptions.ClientError as error:
                log.error("Boto3 API returned error: {}".format(error))
            

        if self.filter_tags.get('conjunction') == 'OR':

            def _union_tfff_tftf_fftf(tag_dict, function_name, function_arn):
                if self.filter_tags.get('tag_key1') in tag_dict or self.filter_tags.get('tag_key2') in tag_dict:
                    print(function_name)
                    print(self.filter_tags.get('tag_key1'))
                    print(self.filter_tags.get('tag_key2'))
                    print(tag_dict)
                    resource_inventory[function_arn] = function_name
                
            def _union_tttf(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key1') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key1')] == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_arn] = function_name
                elif self.filter_tags.get('tag_key2') in tag_dict:
                    resource_inventory[function_arn] = function_name

            def _union_tftt(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key2')] == self.filter_tags.get('tag_value2'):
                        resource_inventory[function_arn] = function_name
                elif self.filter_tags.get('tag_key1') in tag_dict:
                    resource_inventory[function_arn] = function_name

            def _union_fftt(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key2')] == self.filter_tags.get('tag_value2'):
                        resource_inventory[function_arn] = function_name
            
            def _union_ttff(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key1') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key1')] == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_arn] = function_name

            def _union_tttt(tag_dict, function_name, function_arn):
                if  self.filter_tags.get('tag_key1') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key1')] == self.filter_tags.get('tag_value1'):
                        resource_inventory[function_arn] = function_name
                elif  self.filter_tags.get('tag_key2') in tag_dict:
                    if tag_dict[self.filter_tags.get('tag_key2')] == self.filter_tags.get('tag_value2'):
                        resource_inventory[function_arn] = function_name
            
            def _union_ffff(tag_dict, function_name, function_arn):
                resource_inventory[function_arn] = function_name

            # "OR" Truth table check for tag_key1, tag_value1, tag_key2, tag_value2
            or_combos = {
                (False, False, False, True): _intersection_union_invalid,
                (False, True, False, False): _intersection_union_invalid,
                (False, True, False, True): _intersection_union_invalid,
                (False, True, True, True): _intersection_union_invalid,
                (True, True, False, True): _intersection_union_invalid,
                (False, False, True, False): _union_tfff_tftf_fftf,
                (False, False, True, True): _union_fftt,
                (True, False, False, False): _union_tfff_tftf_fftf,
                (True, False, True, False): _union_tfff_tftf_fftf,
                (True, False, True, True): _union_tftt,
                (True, True, False, False): _union_ttff,
                (True, True, True, False): _union_tttf,
                (True, True, True, True): _union_tttt,
                (False, False, False, False): _union_ffff
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
                        or_combos[(tag_key1_state,
                            tag_value1_state,
                            tag_key2_state,
                            tag_value2_state)](response.get('Tags'), item['FunctionName'], item['FunctionArn'])
                    
                    except botocore.exceptions.ClientError as error:
                            log.error("Boto3 API returned error: {}".format(error))
            except botocore.exceptions.ClientError as error:
                            log.error("Boto3 API returned error: {}".format(error))
            
        return resource_inventory            


    # method - get_lambda_resources_tags
    # Returns a nested dictionary of every resource & its key:value tags for the chosen resource type
    # No input arguments
    def get_lambda_resources_tags(self):
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
                tagged_resource_inventory[item['FunctionArn']] = sorted_resource_tags
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

    # method - set_lambda_resources_tags
    # Setter method to update tags on user-selected resources 
    # 2 inputs - list of resource Lambda arns to tag, list of individual tag key:value dictionaries
    def set_lambda_resources_tags(self, resources_to_tag, chosen_tags):
        resources_updated_tags = dict()
        tag_dict = dict()
        # for Lambda Boto3 API covert list of tags dicts to single key:value tag dict 
        for tag in chosen_tags:
            tag_dict[tag['Key']] = tag['Value']
       
        for resource_arn in resources_to_tag:
            try:
                client = boto3.client(self.resource_type, region_name=self.region)
                try:
                    response = client.tag_resource(
                        Resource=resource_arn,
                        Tags=tag_dict
                    )
                except botocore.exceptions.ClientError as error:
                    log.error("Boto3 API returned error: {}".format(error))
                    resources_updated_tags["No Resources Found"] = "No Tags Applied"
            except botocore.exceptions.ClientError as error:
                    log.error("Boto3 API returned error: {}".format(error))
                    resources_updated_tags["No Resources Found"] = "No Tags Applied"
        return resources_updated_tags

        