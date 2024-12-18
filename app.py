#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from ec2_stack.ec2_stack import Ec2AthenaStack
from ec2_stack.ec2_medium_stack import EC2WithAthenaAccessStack


app = cdk.App()
EC2WithAthenaAccessStack(app, "EC2WithAthenaAccessStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    env=cdk.Environment(account='548097210593', region='us-west-2'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
