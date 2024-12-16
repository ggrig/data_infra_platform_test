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

vpc_name = os.getenv ("VPC_NAME" , "")

class Ec2AthenaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a new VPC with public subnets
        vpc = ec2.Vpc(self, "TestVpc",
                      max_azs=2,
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              name="Public",
                              subnet_type=ec2.SubnetType.PUBLIC,
                          ),
                      ])

        # Create an IAM role for the EC2 instance with permissions to access Athena
        instance_role = iam.Role(self, "Ec2InstanceRole",
                                 assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                                 managed_policies=[
                                     iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAthenaFullAccess"),
                                 ])

        # Add additional policies if needed
        instance_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")  # Assuming you need S3 access for Athena
        )

        # Define a Security Group for the EC2 instance to allow SSH and HTTP access
        sg = ec2.SecurityGroup(self, "EC2SecurityGroup",
                               vpc=vpc,
                               description="Allow SSH and web access",
                               allow_all_outbound=True)
        
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH Access")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP Access")

        # Launch an Amazon Linux EC2 instance
        ec2.Instance(self, "TestInstance",
                     instance_type=ec2.InstanceType("t2.micro"),
                     machine_image=ec2.MachineImage.latest_amazon_linux(),
                     vpc=vpc,
                     role=instance_role,
                     security_group=sg)
