
# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

## SSH Connection

```
ssh -i ~/.ssh-keys/hgrig-key.pem ec2-user@ec2-54-245-18-16.us-west-2.compute.amazonaws.com
```


# References

[Getting started with AWS Glue interactive sessions](https://docs.aws.amazon.com/glue/latest/dg/interactive-sessions.html)  
[Author AWS Glue jobs with PyCharm Using AWS Glue Interactive Sessions](https://www.youtube.com/watch?v=04LMQxDxjGM&list=PL7bE4nSzLSWeYCSb-WekhEXzRcI5Fu6Hu&ab_channel=DataEngUncomplicated)  
[AWS Glue: Write Parquet With Partitions to AWS S3](https://www.youtube.com/watch?v=Pr4DNEq19EM&ab_channel=DataEngUncomplicated)  
[Getting Started with Jupyter Notebooks in VS Code](https://www.youtube.com/watch?v=suAkMeWJ1yE&ab_channel=VisualStudioCode)  
[How to install and run Pyspark locally integrated with VSCode via Jupyter Notebook (on Windows).](https://medium.com/@marcelopedronidasilva/how-to-install-and-run-pyspark-locally-integrated-with-vscode-via-jupyter-notebook-on-windows-ff209ac8621f)  
