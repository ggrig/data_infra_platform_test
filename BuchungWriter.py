import os
import boto3
import datetime

from AthenaWriter import AthenaWriter

import logging
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv(override=True)

from string import Template

ATHENA_TABLE_NAME_2 = os.environ['ATHENA_TABLE_NAME_2']

class BuchungWriter(AthenaWriter):
    def __init__(self, context):
        super(BuchungWriter, self).__init__(
            context=context,
            athena_db=os.environ['ATHENA_DB'],
            athena_table_name=os.environ['ATHENA_TABLE_NAME_2']
        )
        # if not self.create_table_if_not_exists(self.client):
        #     logger.error('query execution error')
    
    # def create_table_if_not_exists(self, client):
    #     current_path = os.getcwd()
    #     query_path = os.path.join(current_path, 'sql/iisap_meetago_buchung.sql')
    #     f = open(query_path, "r")
    #     sql = f.read()
    #     f.close()
    #     query = Template(sql).substitute(
    #         athena_table_name_2 = ATHENA_TABLE_NAME_2
    #     )
    #     # response = client.start_query_execution(
    #     #     QueryString=query,
    #     #     ResultConfiguration={"OutputLocation": os.environ['ATHENA_OUTPUT_LOCATION']}
    #     # )
    #     response = client.start_query_execution(
    #         QueryString=query
    #     )        
    #     query_execution_id = response["QueryExecutionId"]
    #     return super()._has_query_succeeded(query_execution_id)
    
    def payload_to_rows(self, payload:list):
        if not isinstance(payload, list): return []

        rows = []

        for i in payload:
            
            row = {}

            row['osmid']    = i['properties']['osmid']
            row['highway']  = i['properties']['highway']
            row['maxspeed'] = i['properties']['maxspeed']
            row['name']     = i['properties']['name']
            row['oneway']   = i['properties']['oneway']
            row['reversed'] = i['properties']['reversed']
            row['length']   = i['properties']['length']
            row['geometry'] = i['geometry']['coordinates']
            row['lanes']    = i['properties']['lanes']
            row['ref']      = i['properties']['ref']
            row['access']   = i['properties']['access']
            row['bridge']   = i['properties']['bridge']
            row['tunnel']   = i['properties']['tunnel']
            row['width']    = i['properties']['width']
            row['junction'] = i['properties']['junction']
            
            rows.append(row)

        return rows
    
    def build_the_query(self, rows:list):
        logger.info(f'BuchungWriter build recieves {len(rows)} rows')

        if 0 == len(rows): return '', 0
        values = ''
        count = 0

        for row in rows: 
            if not 'osmid' in row: continue
            if not 'highway' in row: continue
            if not 'maxspeed' in row: continue
            if not 'name' in row: continue
            if not 'oneway' in row: continue
            if not 'reversed' in row: continue
            if not 'length' in row: continue
            if not 'geometry' in row: continue
            if not 'lanes' in row: continue
            if not 'ref' in row: continue
            if not 'access' in row: continue
            if not 'bridge' in row: continue
            if not 'tunnel' in row: continue
            if not 'width' in row: continue
            if not 'junction' in row: continue
                
            count += 1
            if count > 1: values += ","
            values += "("
            values += "null," if row['osmid'] is None else f"CAST({row['osmid']} AS string),"
            values += "null," if row['highway'] is None else f"CAST({row['highway']} AS string),"
            values += "null," if row['maxspeed'] is None else f"CAST({row['maxspeed']} AS string),"
            values += "null," if row['name'] is None else f"CAST({row['name']} AS string),"
            values += "null," if row['oneway'] is None else f"CAST({row['oneway']} AS boolean),"
            values += "null," if row['reversed'] is None else f"CAST({row['reversed']} AS boolean),"
            values += "null," if row['length'] is None else f"CAST({row['length']} AS double),"
            values += "null," if row['geometry'] is None else f"CAST({row['geometry']} AS string),"
            values += "null," if row['lanes'] is None else f"CAST({row['lanes']} AS string),"
            values += "null," if row['ref'] is None else f"CAST({row['ref']} AS string),"
            values += "null," if row['access'] is None else f"CAST({row['access']} AS string),"
            values += "null," if row['bridge'] is None else f"CAST({row['bridge']} AS boolean),"
            values += "null," if row['tunnel'] is None else f"CAST({row['tunnel']} AS boolean),"
            values += "null," if row['width'] is None else f"CAST({row['width']} AS double),"
            values += "null," if row['junction'] is None else f"CAST({row['junction']} AS string),"
            values += ")"

        if not count: return '', 0
        
        query = f"""
            INSERT INTO {self.athena_db}.{self.athena_table_name} (
                osmid,
                highway,
                maxspeed,
                name,
                oneway,
                reversed,
                length,
                geometry,
                lanes,
                ref,
                access,
                bridge,
                tunnel,
                width,
                junction 
            )
            VALUES {values}
        """ 

        logger.info(f'Buchung query has been built: {count}')
        # logger.info(f'Buchung query: {query}')

        return query, count
    
if __name__ == '__main__':
    logging.basicConfig(
        filename='log-BuchungWriter.log', 
        # encoding='utf-8', 
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    client = boto3.client("athena", region_name = 'eu-central-1')

    awq = BuchungWriter(client=client)
    
    logger.info(awq.run([(839624, datetime.datetime(2024, 4, 11, 15, 0, 47), 1080048016, None, 'MEETAGO', 0, datetime.date(2019, 3, 22), None, 5, datetime.date(2019, 4, 3), datetime.date(2019, 4, 4), '7040 - Siemens AG', 'Barbara Detmer', None, None, None, 'MEETAGO', 'EUR', 100000, None, None, 1, None, 21200, 21200, None, None, 990163, None, None, False, '7040 - Siemens AG , Barbara Detmer', None, None, None, 839624, None, None, None, None, None, None, None, None, None, None, None, None)]))