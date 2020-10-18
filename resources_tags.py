#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Getter & setter for AWS resources & tags.

# Import AWS module for python
import boto3, botocore
# Import collections to use ordered dictionaries for storage
from collections import OrderedDict
# Import AWS Lambda resources & tags getters & setters
from lambda_resources_tags import * 
# Import logging module
import logging
# Import Python's regex module to filter Boto3's API responses 
import re

# Instantiate logging for this module using its file name
log = logging.getLogger(__name__)

# Define resources_tags class to get/set resources & their assigned tags
class resources_tags:
    
    #Class constructor
    def __init__(self, resource_type, unit, region):
        # EBS uses the "ec2" Boto3 client
        if resource_type == "ebs":
            self.resource_type = "ec2"
        else:
            self.resource_type = resource_type
        self.unit = unit
        self.region = region

    #Returns a sorted list of all resources for the resource type specified  
    def get_resources(self, **filter_tags):
        
        self.filter_tags = dict()
        #if filter_tags.get('tag_key1') or filter_tags.get('tag_key2'):
        self.filter_tags = filter_tags
        log.debug("The received filter tags are: {}".format(self.filter_tags))
        
        client = boto3.client(self.resource_type, region_name=self.region)

        def _get_filtered_resources(client_command):
            
            filters_list = list()

            # Issue Boto3 method using client, client command & filters list
            def _boto3_get_method():
                try:
                    filtered_resources = getattr(client, client_command)(
                        Filters=filters_list
                    )
                    log.debug("The filtered resources are: {}".format(filtered_resources))
                    return filtered_resources
                    
                except botocore.exceptions.ClientError as error:
                    errorString = "Boto3 API returned error: {}"
                    log.error(errorString.format(error))
                    filtered_resources = dict()
                    return filtered_resources
            
            # Add any selected tag keys and values to the AWS resource filter "filters_list"
            if self.filter_tags.get('conjunction') == 'AND':
                if self.filter_tags.get('tag_key1'):
                    tag_dict = dict()
                    tag_value_list = list()
                    if self.filter_tags.get('tag_value1'):
                        tag_dict['Name'] = 'tag:' + self.filter_tags.get('tag_key1')
                        tag_value_list.append(self.filter_tags.get('tag_value1'))
                    else:
                        tag_dict['Name'] = 'tag-key'
                        tag_value_list.append(self.filter_tags.get('tag_key1'))
                    tag_dict['Values'] = tag_value_list
                    filters_list.append(tag_dict)
                if self.filter_tags.get('tag_key2'):
                    tag_dict = dict()
                    tag_value_list = list()
                    if self.filter_tags.get('tag_value2'):
                        tag_dict['Name'] = 'tag:' + self.filter_tags.get('tag_key2')
                        tag_value_list.append(self.filter_tags.get('tag_value2'))
                    else:
                        tag_dict['Name'] = 'tag-key'
                        tag_value_list.append(self.filter_tags.get('tag_key2'))
                    tag_dict['Values'] = tag_value_list
                    filters_list.append(tag_dict)
                
                requested_resources = _boto3_get_method()
                returned_dict = dict()
                returned_dict['results_1'] = requested_resources
                return returned_dict

            elif self.filter_tags.get('conjunction') == 'OR':
                tag1_matching_resources = dict()
                tag2_matching_resources = dict()
                if self.filter_tags.get('tag_key1'):
                    tag_dict = dict()
                    tag_value_list = list()
                    if self.filter_tags.get('tag_value1'):
                        tag_dict['Name'] = 'tag:' + self.filter_tags.get('tag_key1')
                        tag_value_list.append(self.filter_tags.get('tag_value1'))
                    else:
                        tag_dict['Name'] = 'tag-key'
                        tag_value_list.append(self.filter_tags.get('tag_key1'))
                    tag_dict['Values'] = tag_value_list
                    filters_list.append(tag_dict)
                    tag1_matching_resources = _boto3_get_method()
                if self.filter_tags.get('tag_key2'):
                    filters_list = list()
                    tag_dict = dict()
                    tag_value_list = list()
                    if self.filter_tags.get('tag_value2'):
                        tag_dict['Name'] = 'tag:' + self.filter_tags.get('tag_key2')
                        tag_value_list.append(self.filter_tags.get('tag_value2'))
                    else:
                        tag_dict['Name'] = 'tag-key'
                        tag_value_list.append(self.filter_tags.get('tag_key2'))
                    tag_dict['Values'] = tag_value_list
                    filters_list.append(tag_dict)
                    tag2_matching_resources = _boto3_get_method()
            
                returned_dict = dict()
                # Place Boto3 filtered results into a dictionary return package
                if tag1_matching_resources and tag2_matching_resources:
                    returned_dict['results_1'] = tag1_matching_resources
                    returned_dict['results_2'] = tag2_matching_resources
                    return returned_dict
                elif tag1_matching_resources and not tag2_matching_resources:
                    returned_dict['results_1'] = tag1_matching_resources
                    return returned_dict
                elif not tag1_matching_resources and tag2_matching_resources:
                    returned_dict['results_1'] = tag2_matching_resources
                    return returned_dict
                else:
                    return None

            else:
                    return None

        def _get_named_resources(client_command):
            try:
                named_resources = getattr(client, client_command)(
                    Filters=[
                        {
                            'Name': 'tag-key',
                            'Values': [
                                'name',
                                'Name'
                            ]
                        }
                    ]
                )
                log.debug("The named resources are: {}".format(named_resources))
                return named_resources

            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {}"
                log.error(errorString.format(error))
                named_resources = dict()
                return named_resources

        named_resource_inventory = dict()
        if self.unit == 'instances':
            if self.filter_tags.get('tag_key1') or self.filter_tags.get('tag_key2'):
                try:
                    filtered_resources = _get_filtered_resources('describe_instances')
                    for _, results in filtered_resources.items():
                        for item in results['Reservations']:
                            for resource in item['Instances']:
                                named_resource_inventory[resource['InstanceId']] = 'no name found'
                                for tag in resource['Tags']:
                                    if(tag['Key'].lower() == 'name'):
                                        named_resource_inventory[resource['InstanceId']] = tag['Value']

                except botocore.exceptions.ClientError as error:
                    log.error("Boto3 API returned error: {}".format(error))
            else:
                try:
                    named_resources = _get_named_resources('describe_instances')
                    selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                    for resource in selected_resource_type.instances.all():
                        named_resource_inventory[resource.id] = 'no name found'
                    for item in named_resources['Reservations']:
                        for resource in item['Instances']:
                            for tag in resource['Tags']:
                                if(tag['Key'].lower() == 'name'):
                                    named_resource_inventory[resource['InstanceId']] = tag['Value']
                    
                except botocore.exceptions.ClientError as error:
                    log.error("Boto3 API returned error: {}".format(error))

        elif self.unit == 'volumes':
            if self.filter_tags.get('tag_key1') or self.filter_tags.get('tag_key2'):
                try:
                    filtered_resources = _get_filtered_resources('describe_volumes')
                    for _, results in filtered_resources.items():
                        for item in results['Volumes']:
                            named_resource_inventory[item['VolumeId']] = 'no name found'
                            for tag in item['Tags']:
                                if(tag['Key'].lower() == 'name'):
                                    named_resource_inventory[item['VolumeId']] = tag['Value']

                except botocore.exceptions.ClientError as error:
                    log.error("Boto3 API returned error: {}".format(error))
            else:
                try:
                    named_resources = _get_named_resources('describe_volumes')
                    selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                    for resource in selected_resource_type.volumes.all():
                        named_resource_inventory[resource.id] = 'no name found'
                    for item in named_resources['Volumes']:
                            for tag in item['Tags']:
                                if(tag['Key'].lower() == 'name'):
                                    named_resource_inventory[item['VolumeId']] = tag['Value']
                    
                except botocore.exceptions.ClientError as error:
                    errorString = "Boto3 API returned error: {}"
                    log.error(errorString.format(error))

        elif self.unit == 'buckets':
            if self.filter_tags.get('tag_key1') or self.filter_tags.get('tag_key2'):
                for resource in selected_resource_type.buckets.all(): 
                    log.debug("This bucket name is: {}".format(resource))
                    try:
                        response = client.get_bucket_tagging(
                            Bucket=resource.name
                        )
                    except botocore.exceptions.ClientError as error:
                        errorString = "Boto3 API returned error: {} {}"
                        log.error(errorString.format(resource.name, error))
                        response = dict()
                    if 'TagSet' in response:
                        for tag in response['TagSet']:
                            if self.filter_tags.get('tag_key1'):
                                if self.filter_tags.get('tag_value1'):
                                    if tag.get('Key') == self.filter_tags.get('tag_key1') and tag.get('Value') == self.filter_tags.get('tag_value1'):
                                        named_resource_inventory[resource.name] = resource.name
                                else:
                                    if tag.get('Key') == self.filter_tags.get('tag_key1'):
                                        named_resource_inventory[resource.name] = resource.name
                            if self.filter_tags.get('tag_key2'):
                                if self.filter_tags.get('tag_value2'):
                                    if tag.get('Key') == self.filter_tags.get('tag_key2') and tag.get('Value') == self.filter_tags.get('tag_value2'):
                                        named_resource_inventory[resource.name] = resource.name
                                else:
                                    if tag.get('Key') == self.filter_tags.get('tag_key2'):
                                        named_resource_inventory[resource.name] = resource.name
            else:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for resource in selected_resource_type.buckets.all():   
                    named_resource_inventory[resource.name] = resource.name
                log.debug("The buckets list is: {}".format(named_resource_inventory)) 

        elif self.unit == "functions":
            functions_inventory = lambda_resources_tags(self.resource_type, self.region)
            named_resource_inventory = functions_inventory.get_lambda_names_ids(self.filter_tags)
        
        # Sort the resources based on the resource's name
        ordered_inventory = OrderedDict()
        ordered_inventory = sorted(named_resource_inventory.items(), key=lambda item: item[1])
        return ordered_inventory
            
    # Returns a nested dictionary of every resource & its key:value tags for the chosen resource type
    # No input arguments
    def get_resources_tags(self):

        # Instantiate dictionaries to hold resources & their tags
        tagged_resource_inventory = {}
        sorted_tagged_resource_inventory = {}

        # Interate through resources & inject resource ID's with user-defined tag key:value pairs per resource into a nested dictionary
        # indexed by resource ID
        if self.unit == 'instances':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for item in selected_resource_type.instances.all():
                    resource_tags = {}
                    sorted_resource_tags = {}
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                resource_tags[tag["Key"]] = tag["Value"]
                    except:
                        resource_tags["No Tags Found"] = "No Tags Found"
                    sorted_resource_tags = OrderedDict(sorted(resource_tags.items()))
                    tagged_resource_inventory[item.id] = sorted_resource_tags
            except:
                tagged_resource_inventory["No Resource Found"] = {"No Tags Found": "No Tags Found"}
        elif self.unit == 'volumes':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for item in selected_resource_type.volumes.all():
                    resource_tags = {}
                    sorted_resource_tags = {}
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                resource_tags[tag["Key"]] = tag["Value"]
                    except:
                        resource_tags["No Tags Found"] = "No Tags Found"
                    sorted_resource_tags = OrderedDict(sorted(resource_tags.items()))
                    tagged_resource_inventory[item.id] = sorted_resource_tags
            except:
                tagged_resource_inventory["No Resource Found"] = {"No Tags Found": "No Tags Found"}
        elif self.unit == 'buckets':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for item in selected_resource_type.buckets.all():
                    resource_tags = {}
                    sorted_resource_tags = {}
                    try:
                        for tag in selected_resource_type.BucketTagging(item.name).tag_set:
                            if not re.search("^aws:", tag["Key"]):
                                resource_tags[tag["Key"]] = tag["Value"]
                    except:
                        resource_tags["No Tags Found"] = "No Tags Found"
                    sorted_resource_tags = OrderedDict(sorted(resource_tags.items()))
                    tagged_resource_inventory[item.name] = sorted_resource_tags
            except:
                tagged_resource_inventory["No Resource Found"] = {"No Tags Found": "No Tags Found"}
        elif self.unit == 'functions':
            functions_inventory = lambda_resources_tags(self.resource_type, self.region)
            tagged_resource_inventory = functions_inventory.get_lambda_resources_tags()

        sorted_tagged_resource_inventory = OrderedDict(sorted(tagged_resource_inventory.items()))

        return sorted_tagged_resource_inventory

    # Getter method retrieves every tag:key for object's resource type
    # No input arguments
    def get_tag_keys(self):

        sorted_tag_keys_inventory = list()

        if self.unit == 'instances':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for item in selected_resource_type.instances.all():
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                sorted_tag_keys_inventory.append(tag["Key"])
                    except:
                        sorted_tag_keys_inventory.append("No tag keys found")
            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {} {}"
                log.error(errorString.format(self.unit, error))
                sorted_tag_keys_inventory.append("No tag keys found")
        elif self.unit == 'volumes':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for item in selected_resource_type.volumes.all():
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                sorted_tag_keys_inventory.append(tag["Key"])
                    except:
                        sorted_tag_keys_inventory.append("No Tags Found")
            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {} {}"
                log.error(errorString.format(self.unit, error))
                sorted_tag_keys_inventory.append("No Tags Found")
        elif self.unit == 'buckets':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for item in selected_resource_type.buckets.all():
                    try:
                        for tag in selected_resource_type.BucketTagging(item.name).tag_set:
                            if not re.search("^aws:", tag["Key"]):
                                sorted_tag_keys_inventory.append(tag["Key"])
                    except:
                        sorted_tag_keys_inventory.append("No Tags Found")
            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {} {}"
                log.error(errorString.format(self.unit, error))
                sorted_tag_keys_inventory.append("No Tags Found")
        elif self.unit == 'functions':
            functions_inventory = lambda_resources_tags(self.resource_type, self.region)
            sorted_tag_keys_inventory = functions_inventory.get_lambda_tag_keys()

        #Remove duplicate tags & sort
        sorted_tag_keys_inventory = list(set(sorted_tag_keys_inventory))
        sorted_tag_keys_inventory.sort(key=str.lower)

        return sorted_tag_keys_inventory

    # Getter method retrieves every tag:value for object's resource type
    # No input arguments
    def get_tag_values(self):

        sorted_tag_values_inventory = list()

        if self.unit == 'instances':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for item in selected_resource_type.instances.all():
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                sorted_tag_values_inventory.append(tag["Value"])
                    except:
                        sorted_tag_values_inventory.append("No Tags Found")
            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {} {}"
                log.error(errorString.format(self.unit, error))
                sorted_tag_values_inventory.append("No Tags Found")
        elif self.unit == 'volumes':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for item in selected_resource_type.volumes.all():
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                sorted_tag_values_inventory.append(tag["Value"])
                    except:
                        sorted_tag_values_inventory.append("No Tags Found")
            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {} {}"
                log.error(errorString.format(self.unit, error))
                sorted_tag_values_inventory.append("No Tags Found")
        elif self.unit == 'buckets':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for item in selected_resource_type.buckets.all():
                    try:
                        for tag in selected_resource_type.BucketTagging(item.name).tag_set:
                            if not re.search("^aws:", tag["Key"]):
                                sorted_tag_values_inventory.append(tag["Value"])
                    except:
                        sorted_tag_values_inventory.append("No Tags Found")
            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {} {}"
                log.error(errorString.format(self.unit, error))
                sorted_tag_values_inventory.append("No Tags Found")
        elif self.unit == 'functions':
            functions_inventory = lambda_resources_tags(self.resource_type, self.region)
            sorted_tag_values_inventory = functions_inventory.get_lambda_tag_values()

        #Remove duplicate tags & sort
        sorted_tag_values_inventory = list(set(sorted_tag_values_inventory))
        sorted_tag_values_inventory.sort(key=str.lower)

        return sorted_tag_values_inventory

    #Setter method to update tags on user-selected resources 
    def set_resources_tags(self, resources_to_tag, chosen_tags):

        resources_updated_tags = {}

        if self.unit == 'instances':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for resource_id in resources_to_tag:
                        resource_tag_list = []
                        instance = selected_resource_type.Instance(resource_id)
                        resource_tag_list = instance.create_tags(
                            Tags=chosen_tags
                        )
                resources_updated_tags[resource_id] = resource_tag_list
            except:
                resources_updated_tags["No Resources Found"] = "No Tags Applied"
        elif self.unit == 'volumes':
            try:
                selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                for resource_id in resources_to_tag:
                        resource_tag_list = []
                        volume = selected_resource_type.Volume(resource_id)
                        resource_tag_list = volume.create_tags(
                            Tags=chosen_tags
                        )
                resources_updated_tags[resource_id] = resource_tag_list
            except:
                resources_updated_tags["No Resources Found"] = "No Tags Applied"
        elif self.unit == 'buckets':
            for resource_id in resources_to_tag:
                tag_set_dict = dict()
                resource_tag_list = list()
                current_applied_tags = dict()
                try:
                    client = boto3.client(self.resource_type, region_name=self.region)
                    current_applied_tags = client.get_bucket_tagging(
                        Bucket=resource_id
                    )
                    log.debug("The existing tags for {} are {}".format(resource_id, current_applied_tags))
                except botocore.exceptions.ClientError as error:
                    errorString = "Boto3 API returned error: {} {}"
                    log.error(errorString.format(resource_id, error))

                if current_applied_tags.get('TagSet'):
                    for current_tag in current_applied_tags['TagSet']:
                        for new_tag in chosen_tags:
                            if new_tag['Key'] != current_tag['Key']:
                                chosen_tags.append(current_tag)
                tag_set_dict['TagSet'] = chosen_tags
                log.debug("The chosen tags for {} are {}".format(resource_id, tag_set_dict))
                try:
                    selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
                    bucket_tagging = selected_resource_type.BucketTagging(resource_id)
                    resource_tag_list = bucket_tagging.put(
                        Tagging=tag_set_dict
                    )
                    resources_updated_tags[resource_id] = resource_tag_list
                    log.debug("These tags are applied to the {} bucket: {}".format(resource_id, resource_tag_list))
                except botocore.exceptions.ClientError as error:
                    errorString = "Boto3 API returned error: {} {}"
                    log.error(errorString.format(resource_id, error))
                    resources_updated_tags["No Resources Found"] = "No Tags Applied"
        elif self.unit == 'functions':
            functions_inventory = lambda_resources_tags(self.resource_type, self.region)
            resources_updated_tags = functions_inventory.set_lambda_resources_tags(resources_to_tag, chosen_tags)
        
        return resources_updated_tags             