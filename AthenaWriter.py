import os
import boto3
import time
import traceback
import json

import logging
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv(override=True)

def execute_athena_query(athena_client, query):
    # logger.info(f'query = {query}')
    try:
        # Execute the query
        response = athena_client.start_query_execution(
            QueryString=query,
            ResultConfiguration = { 'OutputLocation': 's3://athena-results-ggrig/athena-results'}
        )
        
        # Get the query execution ID
        query_execution_id = response['QueryExecutionId']
        
        # Wait for the query to complete
        query_status = None
        while query_status not in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            query_status = response['QueryExecution']['Status']['State']
            if query_status == 'FAILED':
                logger.error("Query execution failed.")
                logger.error(response['QueryExecution']['Status']['AthenaError']['ErrorMessage'])
                logger.error(query)
                break
            if query_status == 'CANCELLED':
                logger.info("Query execution  was cancelled.")
                break
            time.sleep(1)
            
        # Get the results
        if query_status == 'SUCCEEDED':
            results = athena_client.get_query_results(
                QueryExecutionId=query_execution_id
            )
            
            logger.info(f'Athena write SUCCEEDED {results}')

    except Exception as ex:
        logger.error(f'{str(ex)}')

# def athena_test(athena_client):
#     query = """
#     INSERT INTO det_landing_finance_and_controlling.confirmed_invoices 
#     VALUES ( 
#               'case_no_05052024',
#               CAST('2013-12-14' AS DATE)
#           )
#     """
#     execute_athena_query(athena_client=athena_client, query=query)

class AthenaWriter():

    # see https://www.learnaws.org/2022/01/16/aws-athena-boto3-guide/

    def __init__(self, context:str, athena_db:str, athena_table_name:str):

        self.output_location=os.environ['ATHENA_OUTPUT_LOCATION']
        self.athena_db = athena_db
        self.athena_table_name = athena_table_name
        self.records_processed = 0
        self.context = context
        
        self.init_athena_client(self.context)
        # athena_test(self.athena_client)

    def init_athena_client(self, context):
        if context == 'unittest':
            logger.info(f'context = {context}')
            self.athena_client = boto3.client("athena", region_name = 'us-west-2')
            return

        # sts_connection = boto3.client('sts')
        # acct_b = sts_connection.assume_role(
        #     RoleArn="arn:aws:iam::431647458188:role/hrs-data-prod-Finance-ca-role",
        #     RoleSessionName="cross_acct_lambda"
        # )
        
        # ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
        # SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
        # SESSION_TOKEN = acct_b['Credentials']['SessionToken']
        
        # self.athena_client = boto3.client('athena',aws_access_key_id=ACCESS_KEY,
        #     aws_secret_access_key=SECRET_KEY,
        #     aws_session_token=SESSION_TOKEN, region_name = 'eu-central-1')
        
        ACCESS_KEY = os.environ['ACCESS_KEY']
        SECRET_KEY = os.environ['SECRET_KEY']

        self.athena_client = boto3.client('athena',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name = 'us-west-2')
        
    # def _has_query_succeeded(self, execution_id):
    #     if not execution_id:
    #         return False

    #     state = "RUNNING"
    #     max_execution = 60
    #     status = None

    #     while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
    #         response = self.athena_client.get_query_execution(QueryExecutionId=execution_id)
    #         if (
    #             "QueryExecution" in response
    #             and "Status" in response["QueryExecution"]
    #             and "State" in response["QueryExecution"]["Status"]
    #         ):
    #             status = response["QueryExecution"]["Status"]
    #             state = response["QueryExecution"]["Status"]["State"]
    #             if state == "SUCCEEDED":
    #                 return True

    #         time.sleep(10)
    #         # logger.info(f'query:{execution_id} state: {state}')
    #         max_execution -= 10

    #     logger.error(f'Timed Out Query: {execution_id} status: {status}')
    #     return False
 
    def payload_to_rows(self, payload):
            return payload
    
    def build_the_query(self, rows:list):
        return 'select current_date;', 0
    
    def run(self, payload):
        rows = self.payload_to_rows(payload = payload)
        query, count = self.build_the_query(rows = rows)

        if count == 0:
            logger.info('Nothing to send')
            return 200

        logger.info(f'Sending {count} records')

        try:
            # response = self.athena_client.start_query_execution(
            #     QueryString=query            
            # )

            # execution_id = response["QueryExecutionId"]

            # if not self._has_query_succeeded(execution_id=execution_id):
            #     logger.error(f'Query {execution_id} not succeeded')
            #     logger.error(json.dumps(response, indent=4))
            #     logger.error(query)
            #     return 400
            
            self.init_athena_client(self.context)
            execute_athena_query(athena_client=self.athena_client, query=query)

        except Exception as ex:
            logger.error(str(ex))
            logger.error(traceback.format_exc())
            logger.error(query)
            return 500

        return 200
