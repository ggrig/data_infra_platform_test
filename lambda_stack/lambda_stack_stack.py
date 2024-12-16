from aws_cdk import (
  aws_iam as iam,
  aws_rds as rds,
  aws_sqs as sqs,
  aws_sns as sns,
  aws_ec2 as ec2,
  aws_s3  as s3,
  aws_logs as logs,
  aws_kms as kms,
  aws_cloudwatch         as cloudwatch,
  aws_cloudwatch_actions as cloudwatch_actions,
  aws_secretsmanager    as secretsmanager,
  aws_s3_notifications  as s3n,
  aws_sns_subscriptions as subs,
  aws_lambda            as lfn,
  aws_stepfunctions     as sfn,
  aws_apigateway        as apigw,
  Aspects, CfnOutput, Stack, SecretValue, Tags, Fn, Aws, CfnMapping, Duration, RemovalPolicy,
  App, RemovalPolicy, Size
)

from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion

from constructs import Construct
from dotenv import load_dotenv
load_dotenv(override=True)

import os
athena_table = os.environ['ATHENA_TABLE_NAME_2']

class LambdaStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "LambdaStackQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        
        lambda_data_access_role = iam.Role(self,'TestDataAccessRole',
            role_name='TestDataAccessRole',
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAthenaFullAccess"),
            ]
        )        

        data_access_lambda_layer = PythonLayerVersion(
                self,
                'DataAccessLambdaLayer',
                entry='./lambda_layer',
                compatible_runtimes=[lfn.Runtime.PYTHON_3_8],
                removal_policy=RemovalPolicy.DESTROY,
            )

        lambda_function = lfn.Function(self, "lambda",
                                    runtime=lfn.Runtime.PYTHON_3_8,
                                    handler="handler.handler",
                                    code=lfn.Code.from_asset("./lambda"),
                                    timeout=Duration.seconds(450),
                                    role=lambda_data_access_role,
                                    environment={
                                        "ATHENA_TABLE_NAME_2": athena_table,
                                    },
                                    # vpc=vpc_hrs,
                                    # vpc_subnets=vpc_subnets_selection,
                                    layers = [data_access_lambda_layer],
                                    memory_size = 256,
                                    ephemeral_storage_size = Size.mebibytes(1024)
                            )