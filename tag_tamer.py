#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Tag Tamer Admin UI

# Import Collections module to manipulate dictionaries
import collections
from collections import defaultdict
# Import getter/setter module for AWS Config
import config
from config import config
# Import getter/setter module for AWS resources & tags
import resources_tags
from resources_tags import resources_tags
# Import getter/setter module for AWS IAM
import iam
from iam import roles
# Import getter module for TagOption Groups
import get_tag_groups
from get_tag_groups import get_tag_groups
# Import setter module for TagOption Groups
import set_tag_groups
from set_tag_groups import set_tag_group
# Import getter/setter module for AWS Service Catalog
import service_catalog
from service_catalog import service_catalog
# Import flask framework module & classes to build API's
import flask
from flask import Flask, request, render_template, jsonify
from flask_wtf.csrf import CSRFProtect
# Import JSON parser
import json
# Import logging module
import logging

# Read in Tag Tamer solution parameters
tag_tamer_parameters_file = open('tag_tamer_parameters.json', "rt")
tag_tamer_parameters = json.load(tag_tamer_parameters_file)


# logLevel options are DEBUG, INFO, WARNING, ERROR or CRITICAL
logLevel = tag_tamer_parameters['parameters']['logging_level']
logging.basicConfig(filename='tag_tamer.log',format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
# Set the base/root logging level for tag_tamer.py & all imported modules
logging.getLogger().setLevel(logLevel)
log = logging.getLogger('tag_tamer_main')
# Raise logging level for WSGI tool kit "werkzeug" that's German for "tool"
logging.getLogger('werkzeug').setLevel('ERROR')

# Instantiate flask API application
app = flask.Flask(__name__)
app.secret_key = b'\xf9\xca\xf7{z\xb18\\\xa2g\xa2\xfb \xc4\xd4\xf8'
app.config["DEBUG"] = True
csrf = CSRFProtect(app)
csrf.init_app(app)

# Get user-specified AWS regions
selected_regions = tag_tamer_parameters['parameters']['selected_regions']
region = selected_regions[0]
log.debug('The selected AWS region is: \"%s\"', region)

##Output EC2 inventory as JSON for tobywan@
@app.route('/ec2-tags', methods=['GET'])
def ec2_tags():
    inventory = resources_tags("ec2", "instances", region)
    sorted_tagged_inventory = inventory.get_resources_tags()
    return jsonify(sorted_tagged_inventory)

# Get response delivers Tag Tamer home page HTML
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  

# Get response delivers Tag Tamer actions page HTML showing user choices as clickable buttons
@app.route('/actions', methods=['GET'])
def actions():
    return render_template('actions.html')    

# Get response delivers HTML UI to select AWS resource types that Tag Tamer will find
# Post action initiates tag finding for user selected AWS resource types
@app.route('/find-tags', methods=['POST'])
def find_tags():
    return render_template('find-tags.html')    

# Pass Get response to found-tags HTML UI
@app.route('/found-tags', methods=['POST'])
def found_tags():
    if request.form.get('resource_type') == "ebs":
        resource_type = 'ec2'
        unit = 'volumes'
    elif request.form.get('resource_type') == "ec2":
        resource_type = 'ec2'
        unit = 'instances'
    elif request.form.get('resource_type') == "s3":
        resource_type = 's3'
        unit = 'buckets'
    inventory = resources_tags(resource_type, unit, region)
    sorted_tagged_inventory = inventory.get_resources_tags()
    return render_template('found-tags.html', inventory=sorted_tagged_inventory)

# Delivers HTML UI to select AWS resource types to manage Tag Groups for
@app.route('/type-to-tag-group', methods=['POST'])
def type_to_tag_group():
    return render_template('type-to-tag-group.html') 

# Post response to get tag groups attributes UI
@app.route('/get-tag-group-names', methods=['POST'])
def get_tag_group_names():
    all_tag_groups = get_tag_groups(region)
    tag_group_names = all_tag_groups.get_tag_group_names()
    
    if request.form.get('resource_type') == "ebs":
        resource_type = 'ebs'
    elif request.form.get('resource_type') == "ec2":
        resource_type = 'ec2'
    elif request.form.get('resource_type') == "s3":
        resource_type = 's3'

    return render_template('display-tag-groups.html', inventory=tag_group_names, resource_type=resource_type)

# Post method to display edit UI for chosen tag group
@app.route('/edit-tag-group', methods=['POST'])
def edit_tag_group():
    if request.form.get('resource_type') == "ebs":
        resource_type = 'ec2'
        unit = 'volumes'
    elif request.form.get('resource_type') == "ec2":
        resource_type = 'ec2'
        unit = 'instances'
    elif request.form.get('resource_type') == "s3":
        resource_type = 's3'
        unit = 'buckets'
    inventory = resources_tags(resource_type, unit, region)
    sorted_tag_values_inventory = inventory.get_tag_values()

    if request.form.get('tag_group_name'):    
        selected_tag_group_name = request.form.get('tag_group_name')
        tag_group = get_tag_groups(region)
        tag_group_key_values = tag_group.get_tag_group_key_values(selected_tag_group_name)
        return render_template('edit-tag-group.html', resource_type=resource_type, selected_tag_group_name=selected_tag_group_name, selected_tag_group_attributes=tag_group_key_values, selected_resource_type_tag_values_inventory=sorted_tag_values_inventory)
    elif request.form.get('new_tag_group_name'):
        selected_tag_group_name = request.form.get('new_tag_group_name')
        tag_group_key_values = {}
        return render_template('edit-tag-group.html', resource_type=resource_type, selected_tag_group_name=selected_tag_group_name, selected_tag_group_attributes=tag_group_key_values, selected_resource_type_tag_values_inventory=sorted_tag_values_inventory)
    else:
        return render_template('type-to-tag-group.html')

# Post method to add or update a tag group
@app.route('/add-update-tag-group', methods=['POST'])
def add_update_tag_group():
    new_tag_group_name = request.form.get('new_tag_group_name')
    if new_tag_group_name:
        tag_group_name = request.form.get('new_tag_group_name')
        tag_group_key_name = request.form.get('new_tag_group_key_name')
        tag_group_action = "create"
    else:
        tag_group_name = request.form.get('selected_tag_group_name')
        tag_group_key_name = request.form.get('selected_tag_group_key_name')
        tag_group_action = "update"

    tag_group_value_options = []
    form_contents = request.form.to_dict()
    for key, value in form_contents.items():
        if value == "checked":
            tag_group_value_options.append(key)
    if request.form.get("new_tag_group_values"):
        new_tag_group_values = request.form.get("new_tag_group_values").split(",")
        new_tag_group_values = [value.strip(" ") for value in new_tag_group_values]
        tag_group_value_options.extend(new_tag_group_values)

    tag_group = set_tag_group(region)
    if tag_group_action == "create":
        new_tag_group = tag_group.create_tag_group(tag_group_name, tag_group_key_name, tag_group_value_options)
    else:
        updated_tag_group = tag_group.update_tag_group(tag_group_name, tag_group_key_name, tag_group_value_options)

    tag_groups = get_tag_groups(region)
    tag_group_key_values = tag_groups.get_tag_group_key_values(tag_group_name)

    if request.form.get('resource_type') == "ebs":
        resource_type = 'ec2'
        unit = 'volumes'
    elif request.form.get('resource_type') == "ec2":
        resource_type = 'ec2'
        unit = 'instances'
    elif request.form.get('resource_type') == "s3":
        resource_type = 's3'
        unit = 'buckets'
    inventory = resources_tags(resource_type, unit, region)
    sorted_tag_values_inventory = inventory.get_tag_values()

    return render_template('edit-tag-group.html', resource_type=resource_type, selected_tag_group_name=tag_group_name, selected_tag_group_attributes=tag_group_key_values, selected_resource_type_tag_values_inventory=sorted_tag_values_inventory)

# Delivers HTML UI to select AWS resource type to tag using Tag Groups
@app.route('/select-resource-type', methods=['POST'])
def select_resource_type():
    return render_template('select-resource-type.html') 

# Delivers HTML UI to assign tags from Tag Groups to chosen AWS resources
@app.route('/tag_resources', methods=['POST'])
def tag_resources():
    inbound_resource_type = request.form.get('resource_type')
    if request.form.get('resource_type') == "ebs":
        resource_type = 'ec2'
        unit = 'volumes'
    elif request.form.get('resource_type') == "ec2":
        resource_type = 'ec2'
        unit = 'instances'
    elif request.form.get('resource_type') == "s3":
        resource_type = 's3'
        unit = 'buckets'
    chosen_resource_inventory = resources_tags(resource_type, unit, region)
    chosen_resource_ids = chosen_resource_inventory.get_resources()
    
    tag_group_inventory = get_tag_groups(region)
    tag_groups_all_info = tag_group_inventory.get_all_tag_groups_key_values()

    return render_template('tag-resources.html', resource_type=inbound_resource_type, resource_inventory=chosen_resource_ids, tag_groups_all_info=tag_groups_all_info) 

# Delivers HTML UI to assign tags from Tag Groups to chosen AWS resources
@app.route('/apply-tags-to-resources', methods=['POST'])
def apply_tags_to_resources():
    resources_to_tag = []
    resources_to_tag = request.form.getlist('resources_to_tag')
    
    form_contents = request.form.to_dict()
    form_contents.pop("resources_to_tag")
   
    if request.form.get('resource_type') == "ebs":
        resource_type = 'ec2'
        unit = 'volumes'
    elif request.form.get('resource_type') == "ec2":
        resource_type = 'ec2'
        unit = 'instances'
    elif request.form.get('resource_type') == "s3":
        resource_type = 's3'
        unit = 'buckets'
    chosen_resources_to_tag = resources_tags(resource_type, unit, region) 
    form_contents.pop("resource_type")

    chosen_tags = []
    for key, value in form_contents.items():
        if value:
            tag_kv = {}
            tag_kv["Key"] = key
            tag_kv["Value"] = value
            chosen_tags.append(tag_kv)
    chosen_resources_to_tag.set_resources_tags(resources_to_tag, chosen_tags)
    
    updated_sorted_tagged_inventory = {}
    all_sorted_tagged_inventory = chosen_resources_to_tag.get_resources_tags()
    for resource_id in resources_to_tag:
        updated_sorted_tagged_inventory[resource_id] = all_sorted_tagged_inventory[resource_id]
    
    return render_template('updated-tags.html', inventory=updated_sorted_tagged_inventory)

# Retrieves AWS Service Catalog products & Tag Groups
@app.route('/get-service-catalog', methods=['GET'])
def get_service_catalog():

    #Get the Tag Group names & associated tag keys
    tag_group_inventory = dict()
    tag_groups = get_tag_groups(region)
    tag_group_inventory = tag_groups.get_tag_group_names()

    #Get the Service Catalog product templates
    sc_product_ids_names = dict()
    #sc_product_names = list()
    sc_products = service_catalog(region)
    sc_product_ids_names = sc_products.get_sc_product_templates()
    

    return render_template('update-service-catalog.html', tag_group_inventory=tag_group_inventory, sc_product_ids_names=sc_product_ids_names)

# Updates AWS Service Catalog product templates with TagOptions using Tag Groups
@app.route('/set-service-catalog', methods=['POST'])
def set_service_catalog():
    selected_tag_groups = list()
    selected_tag_groups = request.form.getlist('tag_groups_to_assign')
    sc_product_templates = list()
    sc_product_templates = request.form.getlist('chosen_sc_product_template_ids')

    #sc_products = service_catalog()

    #Get the Service Catalog product templates
    sc_product_ids_names = dict()
    #sc_product_names = list()
    sc_products = service_catalog(region)
    sc_product_ids_names = sc_products.get_sc_product_templates()

    #Assign every tag in selected Tag Groups to selected SC product templates
    updated_product_temp_tagoptions = defaultdict(list)
    sc_response = dict()
    for sc_prod_template_id in sc_product_templates:
        for tag_group_name in selected_tag_groups:
            sc_response.clear()
            sc_response = sc_products.assign_tg_sc_product_template(tag_group_name, sc_prod_template_id)
            updated_product_temp_tagoptions[sc_prod_template_id].append(sc_response)

    return render_template('updated-service-catalog.html', sc_product_ids_names=sc_product_ids_names, updated_product_temp_tagoptions=updated_product_temp_tagoptions)

# Retrieves AWS Config Rules & Tag Groups
@app.route('/find-config-rules', methods=['GET'])
def find_config_rules():

    #Get the Tag Group names & associated tag keys
    tag_group_inventory = dict()
    tag_groups = get_tag_groups(region)
    tag_group_inventory = tag_groups.get_tag_group_names()

    #Get the AWS Config Rules
    config_rules_ids_names = dict()
    config_rules = config(region)
    config_rules_ids_names = config_rules.get_config_rules_ids_names()
    
    return render_template('find-config-rules.html', tag_group_inventory=tag_group_inventory, config_rules_ids_names=config_rules_ids_names)

# Updates AWS Config's required-tags rule using Tag Groups
@app.route('/update-config-rules', methods=['POST'])
def set_config_rules():
    selected_tag_groups = list()
    selected_tag_groups = request.form.getlist('tag_groups_to_assign')
    selected_config_rules = list()
    selected_config_rules = request.form.getlist('chosen_config_rule_ids')
    config_rule_id = selected_config_rules[0]

    tag_groups = get_tag_groups(region)
    tag_group_key_values = dict()
    tag_groups_keys_values = dict()
    tag_count=1
    for group in selected_tag_groups:
        # A Required_Tags Config Rule instance accepts up to 6 Tag Groups
        if tag_count < 7:
            tag_group_key_values = tag_groups.get_tag_group_key_values(group)
            key_name = "tag{}Key".format(tag_count)
            value_name = "tag{}Value".format(tag_count)
            tag_groups_keys_values[key_name] = tag_group_key_values['tag_group_key']
            tag_group_values_string = ",".join(tag_group_key_values['tag_group_values'])
            tag_groups_keys_values[value_name] = tag_group_values_string
            tag_count+=1

    config_rules = config(region)
    config_rules.set_config_rules(tag_groups_keys_values, config_rule_id)
    updated_config_rule = config_rules.get_config_rule(config_rule_id)

    return render_template('updated-config-rules.html', updated_config_rule=updated_config_rule)  

# Retrieves AWS IAM Roles & Tag Groups
@app.route('/select-roles-tags', methods=['GET'])
def select_roles_tags():
    tag_group_inventory = get_tag_groups(region)
    tag_groups_all_info = tag_group_inventory.get_all_tag_groups_key_values()

    iam_roles = roles(region)
    #Initially get AWS SSO Roles
    path_prefix = "/aws-reserved/sso.amazonaws.com/"
    roles_inventory = iam_roles.get_roles(path_prefix)

    return render_template('tag-roles.html', roles_inventory=roles_inventory, tag_groups_all_info=tag_groups_all_info)

# Assigns selected tags to roles for tagging newly created AWS resources
@app.route('/set-roles-tags', methods=['POST'])
def set_roles_tags():
    role_name = request.form.get('roles_to_tag')
    form_contents = request.form.to_dict()
    form_contents.pop('roles_to_tag')

    chosen_tags = list()
    for key, value in form_contents.items():
        if value:
            tag_kv = {}
            tag_kv["Key"] = key
            tag_kv["Value"] = value
            chosen_tags.append(tag_kv)

    role_to_tag = roles(region)
    role_to_tag.set_role_tags(role_name, chosen_tags)

    return render_template('actions.html')

app.run()          