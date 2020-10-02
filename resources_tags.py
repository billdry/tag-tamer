#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Getter & setter for resources & tags.

# Import AWS module for python
import boto3, botocore
# Import Collections module to manipulate dictionaries
import collections
# Import Python's regex module to filter Boto3's API responses 
import re
# Import Collections to use ordered dictionaries for storage
from collections import OrderedDict

# Define resources_tags class to get/set resources & their assigned tags
class resources_tags:
    
    #Class constructor
    def __init__(self, resource_type, unit, region):
        self.resource_type = resource_type
        self.unit = unit
        self.region = region

    #Returns a sorted list of all resources for the resource type specified  
    def get_resources(self):
        selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
        client = boto3.client(self.resource_type, region_name=self.region)
        sorted_resource_inventory = list()
        named_resource_inventory = dict()

        if self.unit == 'instances':
            try:
                named_instances = client.describe_instances(
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
                for resource in selected_resource_type.instances.all():
                    named_resource_inventory[resource.id] = 'Unnamed'
                for reservation in named_instances['Reservations']:
                    for instance in reservation['Instances']:
                        for tag in instance['Tags']:
                            if(tag['Key'].lower() == 'name'):
                                named_resource_inventory[instance['InstanceId']] = tag['Value']
                ordered_inventory = OrderedDict()
                ordered_inventory = sorted(named_resource_inventory.items(), key=lambda item: item[1])
                return ordered_inventory
                
            except botocore.exceptions.ClientError as error:
                errorString = "Boto3 API returned error: {}"
                errorString.format(error)
                print(errorString)
                sorted_resource_inventory.append("No Resources Found")

        elif self.unit == 'volumes':
            try:
                for resource in selected_resource_type.volumes.all():
                    sorted_resource_inventory.append(resource.id)
            except:
               sorted_resource_inventory.append("No Resources Found")
        elif self.unit == 'buckets':
            try:
                for resource in selected_resource_type.buckets.all():
                    sorted_resource_inventory.append(resource.name)
            except:
               sorted_resource_inventory.append("No Resources Found")

        #Remove duplicates & sort
        sorted_resource_inventory = list(set(sorted_resource_inventory))
        sorted_resource_inventory.sort(key=str.lower)
        return sorted_resource_inventory
        

    #Returns a nested dictionary of every resource & its key:value tags for the chosen resource type
    def get_resources_tags(self):

        selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
        
        # Instantiate dictionaries to hold resources & their tags
        tagged_resource_inventory = {}
        sorted_tagged_resource_inventory = {}

        # Interate through resources & inject resource ID's with user-defined tag key:value pairs per resource into a nested dictionary
        # indexed by resource ID
        if self.unit == 'instances':
            try:
                for item in selected_resource_type.instances.all():
                    resource_tags = {}
                    sorted_resource_tags = {}
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                resource_tags[tag["Key"]] = tag["Value"]
                    except:
                        resource_tags["No Tags Found"] = "No Tags Found"
                    sorted_resource_tags = collections.OrderedDict(sorted(resource_tags.items()))
                    tagged_resource_inventory[item.id] = sorted_resource_tags
            except:
                tagged_resource_inventory["No Resource Found"] = {"No Tags Found": "No Tags Found"}
        elif self.unit == 'volumes':
            try:
                for item in selected_resource_type.volumes.all():
                    resource_tags = {}
                    sorted_resource_tags = {}
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                resource_tags[tag["Key"]] = tag["Value"]
                    except:
                        resource_tags["No Tags Found"] = "No Tags Found"
                    sorted_resource_tags = collections.OrderedDict(sorted(resource_tags.items()))
                    tagged_resource_inventory[item.id] = sorted_resource_tags
            except:
                tagged_resource_inventory["No Resource Found"] = {"No Tags Found": "No Tags Found"}
        elif self.unit == 'buckets':
            try:
                for item in selected_resource_type.buckets.all():
                    resource_tags = {}
                    sorted_resource_tags = {}
                    try:
                        for tag in selected_resource_type.BucketTagging(item.name).tag_set:
                            if not re.search("^aws:", tag["Key"]):
                                resource_tags[tag["Key"]] = tag["Value"]
                    except:
                        resource_tags["No Tags Found"] = "No Tags Found"
                    sorted_resource_tags = collections.OrderedDict(sorted(resource_tags.items()))
                    tagged_resource_inventory[item.name] = sorted_resource_tags
            except:
                tagged_resource_inventory["No Resource Found"] = {"No Tags Found": "No Tags Found"}

        sorted_tagged_resource_inventory = collections.OrderedDict(sorted(tagged_resource_inventory.items()))

        return sorted_tagged_resource_inventory

    #Getter method retrieves the value of every tag for a supplied resource type
    def get_tag_values(self):

        selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)
        sorted_tag_values_inventory = list()

        if self.unit == 'instances':
            try:
                for item in selected_resource_type.instances.all():
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                sorted_tag_values_inventory.append(tag["Value"])
                    except:
                        sorted_tag_values_inventory.append("No Tags Found")
            except:
               sorted_tag_values_inventory.append("No Tags Found")
        elif self.unit == 'volumes':
            try:
                for item in selected_resource_type.volumes.all():
                    try:
                        for tag in item.tags:
                            if not re.search("^aws:", tag["Key"]):
                                sorted_tag_values_inventory.append(tag["Value"])
                    except:
                        sorted_tag_values_inventory.append("No Tags Found")
            except:
                sorted_tag_values_inventory.append("No Tags Found")
        elif self.unit == 'buckets':
            try:
                for item in selected_resource_type.buckets.all():
                    try:
                        for tag in selected_resource_type.BucketTagging(item.name).tag_set:
                            if not re.search("^aws:", tag["Key"]):
                                sorted_tag_values_inventory.append(tag["Value"])
                    except:
                        sorted_tag_values_inventory.append("No Tags Found")
            except:
                sorted_tag_values_inventory.append("No Tags Found")

        #Remove duplicate tags & sort
        sorted_tag_values_inventory = list(set(sorted_tag_values_inventory))
        sorted_tag_values_inventory.sort(key=str.lower)

        return sorted_tag_values_inventory

    #Setter method to update tags on user-selected resources 
    def set_resources_tags(self, resources_to_tag, chosen_tags):

        selected_resource_type = boto3.resource(self.resource_type, region_name=self.region)

        resources_updated_tags = {}

        if self.unit == 'instances':
            try:
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
            try:
                tag_set_dict = {}
                tag_set_dict['TagSet'] = chosen_tags

                for resources_to_tag in resources_to_tag:
                    resource_tag_list = []
                    bucket_tagging = selected_resource_type.BucketTagging(resource_id)
                    resources_to_tag = bucket_tagging.put(
                        Tagging=tag_set_dict
                    )
                resources_updated_tags[resource_id] = resource_tag_list
            except:
                resources_updated_tags["No Resources Found"] = "No Tags Applied"
        
        return resources_updated_tags             