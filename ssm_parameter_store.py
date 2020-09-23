#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Getter & setter for AWS SSM Parameter Store

# Import AWS module for python
import botocore
import boto3
# Import JSON
import json
# Import logging module
import logging

log = logging.getLogger(__name__)

# Define AWS SSM Parameter Store class to get/set items using Boto3
class ssm_parameter_store:
    
    #Class constructor
    def __init__(self, region):
        self.region = region
        self.ssm_client = boto3.client('ssm', region_name=self.region)

    def form_parameter_hierarchies(self, ssm_parameter_path, ssm_parameter_names):
        # List comprehension to create the fully qualified SSM parameter names
        parameter_list = [ssm_parameter_path + name for name in ssm_parameter_names]
        return parameter_list

    # Argument: List of SSM Parameter names including hierarchy paths
    # Returns: SSM Parameter Dictionaries
    def ssm_get_parameter_details(self, parameter_names):
        try:
            get_parameter_response = self.ssm_client.get_parameters(
                Names=parameter_names,
                WithDecryption=True
            )
            #print("the parameter response is: ", get_parameter_response)
            parameter_dictionary = dict()
            for parameter in get_parameter_response['Parameters']:
                parameter_dictionary[parameter['Name']] = parameter['Value']
            
            #print(parameter_dictionary)
            
            return parameter_dictionary

        except botocore.exceptions.ClientError as error:
            errorString = "Boto3 API returned error: {}"
            log.error(errorString.format(error))
