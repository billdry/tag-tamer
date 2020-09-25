#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Getter delivering Tag Group attributes.  Returns output as dictionaries & lists

# Import AWS module for python
import boto3
# Import Collections module to manipulate dictionaries
import collections

# Define get_tag_groups class
class get_tag_groups:

    #Class constructor
    def __init__(self, region):
        self.tag_groups = {}
        self.region = region
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        #self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('tag_tamer_tag_groups')
    
    #Returns a dictionary of actual_tag_group_name:actual_tag_group_key key:value pairs
    def get_tag_group_names(self):
        tag_group_names={}
        sorted_tag_group_names={}
        
        scan_response = self.table.scan(
            #IndexName='tag_group_name-index',
            #TableName='tag_groups',
            ProjectionExpression="key_name, tag_group_name"
            )        
        try:
            for item in scan_response["Items"]:
                tag_group_names[item["tag_group_name"]] = item["key_name"]
        except:
            tag_group_names["No Tag Groups Found"] = "No Tag Groups Found"
        
        sorted_tag_group_names = collections.OrderedDict(sorted(tag_group_names.items()))
        
        return sorted_tag_group_names 
    
    #Returns a dictionary of tag_group_key:actual_tag_group_key
    #& tag_group_values:list[actual_tag_group_values] for the specified Tag Group
    def get_tag_group_key_values(self, tag_group_name):
        tag_group_key_values = {}
        sorted_tag_group_values = list()

        get_item_response = self.table.get_item(Key={'tag_group_name': tag_group_name})

        try:
            if len(get_item_response["Item"]["key_name"]):
                tag_group_key_values['tag_group_key'] = get_item_response["Item"]["key_name"]
                sorted_tag_group_values = get_item_response["Item"]["key_values"]
                sorted_tag_group_values.sort(key=str.lower)
                tag_group_key_values['tag_group_values'] = sorted_tag_group_values
        except:
                tag_group_key_values['tag_group_key'] = "No Tag Group Key Found"
                tag_group_key_values['tag_group_values'] = "No Tag Group Values Found" 
        
        return tag_group_key_values

    #Returns a list of 3-item groups where every 3-item group includes actual_tag_group_name, actual_tag_group_key
    #& a list[actual_tag_group_values]
    def get_all_tag_groups_key_values(self):
        all_tag_groups_info = list()
        
        inventory = get_tag_groups("us-east-1")
        tag_groups_keys = inventory.get_tag_group_names()
        
        for tag_group_name, tag_group_key in tag_groups_keys.items():
            this_tag_group_info = list()
            this_tag_group_key_values = inventory.get_tag_group_key_values(tag_group_name)
            this_tag_group_info.append(tag_group_name)
            this_tag_group_info.append(tag_group_key)
            this_tag_group_info.append(this_tag_group_key_values['tag_group_values'])
            all_tag_groups_info.append(this_tag_group_info)

        return all_tag_groups_info