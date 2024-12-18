rom aws_cdk import (
    core,
    aws_s3 as s3,
    aws_iam as iam,
    aws_glue as glue
)

class GlueIcebergJobStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 bucket for the CSV files and Iceberg table storage
        data_bucket = s3.Bucket(self, "DataBucket")

        # IAM Role for Glue Job
        glue_role = iam.Role(self, "GlueJobRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
                # Add additional policies as needed
            ]
        )

        # Glue Job
        glue_job = glue.CfnJob(self, "GlueJob",
            role=glue_role.role_arn,
            command={
                "name": "glueetl",
                "scriptLocation": f"s3://{data_bucket.bucket_name}/scripts/glue-job-script.py"
            },
            glue_version="2.0",
            default_arguments={
                "--job-language": "python",
                "--additional-python-modules": "pydeequ==1.0.2",  # Add necessary Python modules
                "--enable-glue-datacatalog": ""
            }
        )


# Glue Python Job 1

# from awsglue.context import GlueContext
# from awsglue.utils import getResolvedOptions
# from pyspark.context import SparkContext
# from pyspark.sql import SparkSession

# args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# sc = SparkContext()
# glueContext = GlueContext(sc)
# spark = glueContext.spark_session

# spark.conf.set("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
# spark.conf.set("spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog")
# spark.conf.set("spark.sql.catalog.glue_catalog.type", "glue")
# spark.conf.set("spark.sql.catalog.glue_catalog.warehouse", "s3://your-bucket-name/iceberg/")

# df = spark.read.format("csv").option("header", "true").load("s3://your-bucket-name/path-to-csv/")
# df.write.format("iceberg").mode("append").partitionBy("partition_column").save("glue_catalog.db_name.table_name")


# Glue Python Job 2

# from awsglue.context import GlueContext
# from awsglue.transforms import *
# from awsglue.utils import getResolvedOptions
# from pyspark.context import SparkContext
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col

# sc = SparkContext()
# glueContext = GlueContext(sc)
# spark = glueContext.spark_session
# spark.conf.set("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
# spark.conf.set("spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog")
# spark.conf.set("spark.sql.catalog.my_catalog.type", "hadoop")
# spark.conf.set("spark.sql.catalog.my_catalog.warehouse", "s3://your-bucket-name/iceberg/")

# # Read CSV file
# df = spark.read.format("csv").option("header", "true").load("s3://your-bucket-name/path-to-csv/")

# # Write to Iceberg table with partitioning
# df.write.format("iceberg").mode("append").partitionBy("partition_column").save("my_catalog.db_name.table_name")
