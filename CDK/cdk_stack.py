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

from utilities.helpers import get_env_files_path, get_image_folder_path, list_files_in_directory

from configuration.config import Config


class EcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config:Config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logger.info(f"Docker file path {get_image_folder_path()}")
        image = DockerImageAsset(self, 'CustomDockerImage',
            directory=get_image_folder_path()
        )

        logger.info(image.image_uri)
        logger.info(image.repository.repository_arn)
        logger.info(image.image_tag)
        
        vpc = ec2.Vpc(
            self, config.vpc_name,
            max_azs=2,
            nat_gateways=1,  # Enable a NAT gateway for internet access for private subnets
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                )
            ]        
        )

        cluster = ecs.Cluster(
            self, 'TestECSCluster',
            vpc=vpc
        )

        task_role = iam.Role(self,'TestDataAccessRole',
            role_name='TestDataAccessRole',
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAthenaFullAccess"),
                # iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                # iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                # iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAthenaFullAccess"),
            ]
        )


        # custom_image = image = ecs.ContainerImage.from_ecr_repository(repository=image.repository, tag=image.image_tag)
        # Deploy a Fargate Service with custom Docker image and Athena access
        # ecs_patterns.ApplicationLoadBalancedFargateService(
        #     self, "MyFargateService",
        #     cluster=cluster,
        #     task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
        #         image=custom_image,
        #         container_name='MyContainer',
        #         execution_role=task_role
        #     ),
        #     desired_count=2,
        #     public_load_balancer=True
        # )

        test_construct = EcsTaskBase(self,
                                "data_retriever",
                                cluster=cluster,
                                repo=image.repository,
                                image_tag=image.image_tag,
                                dotenv_file=".env",
                                role=task_role,
                            )
