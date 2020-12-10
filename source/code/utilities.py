#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
# Tag Tamer utility functions

# Return the Boto3 resource type & unit to the caller
def get_resource_type_unit(type):
    if type:
        if type == "ebs":
            resource_type = 'ebs'
            unit = 'volumes'
        elif type == "ec2":
            resource_type = 'ec2'
            unit = 'instances'
        elif type == "lambda":
            resource_type = 'lambda'
            unit = 'functions'
        elif type == "s3":
            resource_type = 's3'
            unit = 'buckets'
        else:
            resource_type = 'ec2'
            unit = 'instances'
        return resource_type, unit
    
