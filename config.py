#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Getter & setter for AWS Config Rules

# Import AWS module for python
import botocore
import boto3
# Import JSON
import json
# Import logging module
import logging

log = logging.getLogger(__name__)

# Define AWS Config class to get/set items using Boto3
class config:
    
    #Class constructor
    def __init__(self, region):
        self.region = region
        self.config_client = boto3.client('config', region_name=self.region)

    #Get REQUIRED_TAGS Config Rule name & input parameters
    def get_config_rule(self, config_rule_id):
        response = dict()
        all_config_rules = dict()
        try:
            response = self.config_client.describe_config_rules()
            all_config_rules = response['ConfigRules']

            required_tags_config_rules = dict()
            input_parameters_dict = dict()
            for rule in all_config_rules:
                if rule['Source']['SourceIdentifier'] == 'REQUIRED_TAGS':
                    input_parameters_dict = json.loads(rule['InputParameters'])
                    required_tags_config_rules['ConfigRuleName'] = rule['ConfigRuleName']
                    required_tags_config_rules['ComplianceResourceTypes'] = rule['Scope']['ComplianceResourceTypes']
                    for key, value in input_parameters_dict.items():
                        required_tags_config_rules[key] = value
                    input_parameters_dict.clear()
            
            return required_tags_config_rules

        except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {}"
                log.error(errorString.format(error))

    #Get REQUIRED_TAGS Config Rule names & ID's
    def get_config_rules_ids_names(self):
        response = dict()
        all_config_rules = dict()
        try:
            response = self.config_client.describe_config_rules()
            all_config_rules = response['ConfigRules']

            config_rules_ids_names = dict()
            for configRule in all_config_rules:
                if configRule['Source']['SourceIdentifier'] == 'REQUIRED_TAGS':
                    config_rules_ids_names[configRule['ConfigRuleId']] = configRule['ConfigRuleName']
                
            return config_rules_ids_names

        except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {}"
                log.error(errorString.format(error))

    #Set REQUIRED_TAGS Config Rule
    def set_config_rules(self, tag_groups_keys_values, config_rule_id):
        
        if len(tag_groups_keys_values):
            # convert selected Tag Groups into JSON for Boto3 input to
            # this Config Rule's underlying Lambda :
            input_parameters_json = json.dumps(tag_groups_keys_values)
            config_rule_current_parameters = dict()
            config_rule_current_parameters = self.get_config_rule(config_rule_id)
            try:
                self.config_client.put_config_rule(
                    ConfigRule={
                        'ConfigRuleId': config_rule_id,
                        'Scope': {
                            'ComplianceResourceTypes': config_rule_current_parameters['ComplianceResourceTypes']
                        },
                        'InputParameters': input_parameters_json,
                        'Source': {
                            'Owner': 'AWS',
                            'SourceIdentifier': 'REQUIRED_TAGS'
                        }    
                    }
                )
                log.debug('REQUIRED_TAGS Config Rule \"%s\" updated with these parameters: \"%s\"', config_rule_id, input_parameters_json)
            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {}"
                log.error(errorString.format(error))

        else:
            return log.warning("Please select at least one Tag Group")
