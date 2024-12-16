# https://www.builtydata.com/
# author: Harut Grigoryan
#
# This file defines the basic CDK construct with 
# - a test's ECS service
# - the corresponding ECS task definition
# - the logging group 

from aws_cdk import (
        aws_ecs as ecs,
        aws_ecr as ecr,
        aws_logs as logs,
        aws_ec2 as ec2,
        RemovalPolicy
)

import os
import json
from constructs import Construct
from utilities.env_manager import list_env_variables
from dotenv import load_dotenv

import logging
logger = logging.getLogger(__name__)


class EcsTaskBase(Construct):

    def __init__(self, scope: Construct, id:str,
                cluster:ecs.Cluster,
                repo:ecr.Repository,
                image_tag:str,
                dotenv_file:str,
                role = None,
                **kwargs):
        super().__init__(scope, id, **kwargs)

        # os.environ.pop('IDENTITY', None)
        # os.environ.pop('STORAGE_TYPE', None)
        # os.environ.pop('BASE_URL', None)
        # os.environ.pop('CRAWLER_NAME', None)
        # todo - remove all environment variables hardcoded in the code like we did above and replace by the next block
        # Ahmed-(lxth0rz) 24/05/2024: Get a list of all environment variable names
        env_vars = list(os.environ.keys())
        # Iterate over the list and remove each environment variable
        for var in env_vars:
            os.environ.pop(var, None)

        load_dotenv(dotenv_file)

        # env_vars = list_env_variables()
        # # Iterate over the list and remove each environment variable
        # logger.error("Removing environment variables")
        # for var in env_vars:
        #     logger.error(var)


        task_id = "test_task"

        log_id = f'{task_id}-Log'
        log_group_name = f'{task_id}-Log-Group'
        container_id = f'{task_id}-Container'
        stream_prefix = "ecs"

        logger.debug(task_id)
        logger.debug(log_id)
        logger.debug(log_group_name)
        logger.debug(container_id)

        task_definition = ecs.FargateTaskDefinition(self,
                                                    task_id,
                                                    execution_role=role,
                                                    task_role=role,
                                                    cpu=256,
                                                    memory_limit_mib=512)

        # logger.info(f"Repo Name: {repo.repository_name}")
        # logger.info(f"ARN: {repo.repository_arn}")
        # logger.info(f"URI: {repo.repository_uri}")
        # logger.info(f"TAG: {image_tag}")

        image = ecs.ContainerImage.from_ecr_repository(repository=repo, tag=image_tag)

        logger.info(f"Image name: {image.image_name}")

        logDetail = logs.LogGroup(self, log_id, log_group_name=log_group_name, retention=logs.RetentionDays.ONE_MONTH, removal_policy=RemovalPolicy.DESTROY)

        logging = ecs.LogDriver.aws_logs(stream_prefix = stream_prefix, log_group=logDetail)

        # environment = {
        #                 "IDENTITY"      : os.getenv('IDENTITY', ''),
        #                 "STORAGE_TYPE"  : os.getenv('STORAGE_TYPE', ''),
        #                 "BASE_URL"      : os.getenv('BASE_URL', ''),
        #                 "CRAWLER_NAME"  : os.getenv('CRAWLER_NAME', '')
        #         }
        # Ahmed-(lxth0rz) 24/05/2024: Create a dictionary with all environment variables
        # Create a dictionary with all environment variables
        environment = {key: os.getenv(key, '') for key in os.environ.keys()}

        container = task_definition.add_container(container_id,
                                                  image=image,
                                                  environment=environment,
                                                  logging=logging)

        service_id = f"{task_id}-Service"
        service = ecs.FargateService(self,
                                     id=service_id,
                                     desired_count=1,
                                     service_name=service_id,
                                     task_definition=task_definition,
                                     cluster=cluster,
                                     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                                     assign_public_ip=False
                           )

