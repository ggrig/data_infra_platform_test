from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack
)

from constructs import Construct

class EC2WithAthenaAccessStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Define the IAM role for the EC2 instance
        role = iam.Role(self, "InstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAthenaFullAccess")
            ]
        )

        # Create the EC2 instance
        instance = ec2.Instance(self, "MyInstance",
            instance_type=ec2.InstanceType("x2gd.medium"),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=vpc,
            role=role,
            user_data=ec2.UserData.custom('''
                #!/bin/bash
                yum update -y
                yum install -y git
                amazon-linux-extras install python3.8 -y
                curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                unzip awscliv2.zip
                sudo ./aws/install
            ''')
        )

        # Optionally, you can add security group rules here to allow SSH access
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Allow SSH access from anywhere")
