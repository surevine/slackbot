import json
import os
import logging
import urllib
import boto3
import time
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.resource("ec2")

def lambda_handler(event, context):

    logger.info(event)
    operation = event["operation"]
    service_name = event["target"]

    target_instance = get_instance_by_name(service_name)

    if target_instance is None:
        return { "response": "Service not found" }

    print("Operation: " + operation + " Service: " + service_name + " Instance: " + target_instance.id)

    for tag in target_instance.tags:

        if 'dependants' in tag['Key']:
            dependant_names = [x.strip() for x in tag['Value'].split(',')]
            dependant_instances = get_instances_by_name(dependant_names)

            for dependant in dependant_instances:
                perform_operation(operation, dependant)

    perform_operation(operation, target_instance)

    return {  "response": "Success" }


def get_instance_by_name(instance_name):
    return next(iter(ec2.instances.filter(Filters=get_name_filter([instance_name]))), None)


def get_instances_by_name(instance_name_list):
    return ec2.instances.filter(Filters=get_name_filter(instance_name_list))


def get_name_filter(name_list):
    return [{
        'Name':'tag:Name', 
        'Values': name_list}]
    

def perform_operation(operation, instance):
    
    try:
        if operation == "start":
            response = start(instance)
        elif operation == "stop":
            response = stop(instance)
        else:
            response = "Command not recognised"
    except Exception as e:
        logger.error(e)
        response = "Failed to " + operation + " instance " + instance.id

    return response


def start(instance):
    try:
        instance.start()
        logger.info("Starting " + instance.id)
        logger.info(instance.tags)
    except Exception as e:
        logger.error(e)
        raise Exception("failed to start")


def stop(instance):
    try:
        instance.stop()
        logger.info("Stopping " + instance.id)
        logger.info(instance.tags)
    except:
        raise Exception("Service not found")
   