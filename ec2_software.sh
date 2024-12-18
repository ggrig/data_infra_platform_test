#!/bin/bash
yum update -y
yum install -y git
amazon-linux-extras install python3.8 -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install