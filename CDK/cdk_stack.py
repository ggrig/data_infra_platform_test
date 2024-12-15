# https://www.builtydata.com/
# author: Harut Grigoryan
#
# Here we define the CDK stack with 
# - the ECR image to be used by the ECS tasks
# - the ECS VPC and cluster
# - individual test services constructs

import os

from aws_cdk import (
        aws_ecs as ecs,
        aws_ecr as ecr,
        aws_iam as iam,
        aws_rds as rds,
        aws_sqs as sqs,
        aws_sns as sns,
        aws_ec2 as ec2,
        aws_s3  as s3,
        aws_logs as logs,
        aws_kms as kms,
        aws_autoscaling as autoscaling,
        aws_ecs_patterns as ecs_patterns,
        aws_cloudwatch         as cloudwatch,
        aws_cloudwatch_actions as cloudwatch_actions,
        aws_secretsmanager    as secretsmanager,
        aws_s3_notifications  as s3n,
        aws_sns_subscriptions as subs,
        aws_lambda            as lfn,
        aws_stepfunctions     as sfn,
        aws_apigateway        as apigw,
        Aspects, CfnOutput, Stack, SecretValue, Tags, Fn, Aws, CfnMapping, Duration,
        App, RemovalPolicy, Size
)

from constructs import Construct
from aws_cdk.aws_ecr_assets import DockerImageAsset

import logging
logger = logging.getLogger(__name__)

logging.basicConfig(
    filename='logs/ckd-stack.log',
    # encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from CDK.ecs_task_base import EcsTaskBase

from utilities.helpers import get_env_files_path, get_logic_folder_path, list_files_in_directory

from configuration.config import Config


class LogicStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config:Config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        image = DockerImageAsset(self, 'LogicDockerImage',
            directory=get_logic_folder_path()
        )

        logger.info(image.image_uri)
        logger.info(image.repository.repository_arn)
        logger.info(image.image_tag)
        
        vpc = ec2.Vpc.from_lookup(self, 'VPC',  vpc_name=f'{config.vpc_name}')

        cluster = ecs.Cluster(
            self, 'TestECSCluster',
            vpc=vpc
        )

        test_data_access_role = iam.Role(self,'TestDataAccessRole',
            role_name='TestDataAccessRole',
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"),
            ]
        )

        config_file_list = list_files_in_directory(get_env_files_path())
        # only 100 tests for now because of limited resources per stack.
        # for more info: https://github.com/builtyapp/logic/issues/11#issue-2304744616
        # config_file_list = config_file_list[:100]
        for config_file in config_file_list:

            if config_file == '.env':
                logger.info(f"Skipping {config_file}")
                continue

            test_name = f"test_{config_file}"
            test_construct = EcsTaskBase(self,
                                    test_name,
                                    cluster=cluster,
                                    repo=image.repository,
                                    image_tag=image.image_tag,
                                    dotenv_file=config_file,
                                    role=test_data_access_role
                                )
