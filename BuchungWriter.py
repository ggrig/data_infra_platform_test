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
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['osmid'] is not None:
                try:
                    row['osmid'] = str(i['properties']['osmid'])
                    row['osmid'] = row['osmid'].replace("'", "")
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['osmid'] = i['properties']['osmid']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['highway'] is not None:
                try:
                    row['highway'] = str(i['properties']['highway'])
                    row['highway'] = row['highway'].replace("'", "")
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['highway'] = i['properties']['highway']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['maxspeed'] is not None:
                try:
                    row['maxspeed'] = str(i['properties']['maxspeed'])
                    row['maxspeed'] = row['maxspeed'].replace("'", "")
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['maxspeed'] = i['properties']['maxspeed']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['name'] is not None:
                try:
                    row['name'] = str(i['properties']['name'])
                    row['name'] = row['name'].replace("'", "")
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['name'] = i['properties']['name']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['oneway'] is not None:
                try:
                    row['oneway'] = bool(i['properties']['oneway'])
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['oneway'] = i['properties']['oneway']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['reversed'] is not None:
                try:
                    row['reversed'] = bool(i['properties']['reversed'])
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['reversed'] = i['properties']['reversed']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['length'] is not None:
                try:
                    row['length'] = float(i['properties']['length'])
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['length'] = i['properties']['length']
# - - - - - - - - - - - - - - - - - - - -
            if i['geometry']['coordinates'] is not None:
                try:
                    row['geometry'] = str(i['geometry']['coordinates'])
                    row['geometry'] = row['geometry'].replace("'", "")
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['geometry'] = i['geometry']['coordinates']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['lanes'] is not None:
                try:
                    row['lanes'] = str(i['properties']['lanes'])
                    row['lanes'] = row['lanes'].replace("'", "")
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['lanes'] = i['properties']['lanes']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['ref'] is not None:
                try:
                    row['ref'] = str(i['properties']['ref'])
                    row['ref'] = row['ref'].replace("'", "")
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['ref'] = i['properties']['ref']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['access'] is not None:
                try:
                    row['access'] = str(i['properties']['access'])
                    row['access'] = row['access'].replace("'", "")
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['access'] = i['properties']['access']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['bridge'] is not None:
                try:
                    row['bridge'] = bool(i['properties']['bridge'])
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['bridge'] = i['properties']['bridge']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['tunnel'] is not None:
                try:
                    row['tunnel'] = bool(i['properties']['tunnel'])
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['tunnel'] = i['properties']['tunnel']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['width'] is not None:
                try:
                    row['width'] = float(i['properties']['width'])
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
                row['width'] = i['properties']['width']
# - - - - - - - - - - - - - - - - - - - -
            if i['properties']['junction'] is not None:
                try:
                    row['junction'] = str(i['properties']['junction'])
                    row['junction'] = row['junction'].replace("'", "")
                except Exception as ex:
                    logger.exception(ex)
                    continue
            else:
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
            values += "null," if row['osmid'] is None else f"CAST('{row['osmid']}' AS varchar),"
            values += "null," if row['highway'] is None else f"CAST('{row['highway']}' AS varchar),"
            values += "null," if row['maxspeed'] is None else f"CAST('{row['maxspeed']}' AS varchar),"
            values += "null," if row['name'] is None else f"CAST('{row['name']}' AS varchar),"
            values += "null," if row['oneway'] is None else f"CAST({row['oneway']} AS boolean),"
            values += "null," if row['reversed'] is None else f"CAST({row['reversed']} AS boolean),"
            values += "null," if row['length'] is None else f"CAST({row['length']} AS double),"
            values += "null," if row['geometry'] is None else f"CAST('{row['geometry']}' AS varchar),"
            values += "null," if row['lanes'] is None else f"CAST('{row['lanes']}' AS varchar),"
            values += "null," if row['ref'] is None else f"CAST('{row['ref']}' AS varchar),"
            values += "null," if row['access'] is None else f"CAST('{row['access']}' AS varchar),"
            values += "null," if row['bridge'] is None else f"CAST({row['bridge']} AS boolean),"
            values += "null," if row['tunnel'] is None else f"CAST({row['tunnel']} AS boolean),"
            values += "null," if row['width'] is None else f"CAST({row['width']} AS double),"
            values += "null" if row['junction'] is None else f"CAST('{row['junction']}' AS varchar)"
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

    # client = boto3.client("athena", region_name = 'us-west-2')

    a = [
        {
            "id": "(39076461, 274283981, 0)",
            "type": "Feature",
            "properties": {
                "osmid": 25161349,
                "highway": "motorway",
                "lanes": "2",
                "maxspeed": "50 mph",
                "name": "Cross Island Parkway",
                "oneway": True,
                "ref": "CI",
                "reversed": False,
                "length": 819.5016661477803,
                "bridge": None,
                "access": None,
                "tunnel": None,
                "width": None,
                "junction": None,
                "est_width": None,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": (
                    (-73.7947484, 40.7863451),
                    (-73.794615, 40.7863898),
                    (-73.7944856, 40.7864343),
                    (-73.7943563, 40.7864809),
                    (-73.7942289, 40.7865266),
                    (-73.7940993, 40.7865739),
                    (-73.7939726, 40.7866211),
                    (-73.7938448, 40.786671),
                    (-73.7937196, 40.7867213),
                    (-73.793594, 40.7867723),
                    (-73.793465, 40.7868253),
                    (-73.7933444, 40.7868769),
                    (-73.7932188, 40.7869306),
                    (-73.7930954, 40.786984),
                    (-73.7929753, 40.7870377),
                    (-73.7928501, 40.7870933),
                    (-73.7927279, 40.7871496),
                    (-73.7926059, 40.7872061),
                    (-73.7909163, 40.7880014),
                    (-73.790792, 40.7880566),
                    (-73.7906687, 40.7881112),
                    (-73.7905452, 40.788166),
                    (-73.7904232, 40.7882185),
                    (-73.7903022, 40.7882687),
                    (-73.7901731, 40.788322),
                    (-73.7900483, 40.7883727),
                    (-73.7899209, 40.7884227),
                    (-73.7897938, 40.7884715),
                    (-73.7896694, 40.7885183),
                    (-73.7895408, 40.7885667),
                    (-73.7894104, 40.7886139),
                    (-73.7892832, 40.7886587),
                    (-73.7891563, 40.7887019),
                    (-73.7890238, 40.7887451),
                    (-73.7888912, 40.788787),
                    (-73.7887632, 40.7888264),
                    (-73.7886299, 40.7888655),
                    (-73.7884982, 40.788904),
                    (-73.7883607, 40.7889423),
                    (-73.7882291, 40.7889779),
                    (-73.7880942, 40.7890128),
                    (-73.7879575, 40.7890464),
                    (-73.7878231, 40.7890787),
                    (-73.7876873, 40.7891097),
                    (-73.7875503, 40.7891395),
                    (-73.7874134, 40.7891683),
                    (-73.7872765, 40.789195),
                    (-73.78714, 40.7892213),
                    (-73.7870025, 40.7892452),
                    (-73.7868924, 40.7892625),
                    (-73.7867858, 40.7892791),
                    (-73.7866664, 40.7892952),
                    (-73.7865266, 40.7893131),
                    (-73.7863885, 40.7893301),
                    (-73.7862474, 40.7893469),
                    (-73.7861069, 40.7893617),
                    (-73.7859633, 40.7893759),
                ),
            },
        }#,
        # {
        #     "id": "(39076461, 42854803, 0)",
        #     "type": "Feature",
        #     "properties": {
        #         "osmid": 25161578,
        #         "highway": "motorway_link",
        #         "lanes": None,
        #         "maxspeed": None,
        #         "name": None,
        #         "oneway": True,
        #         "ref": None,
        #         "reversed": False,
        #         "length": 268.1440952459794,
        #         "bridge": None,
        #         "access": None,
        #         "tunnel": None,
        #         "width": None,
        #         "junction": None,
        #         "est_width": None,
        #     },
        #     "geometry": {
        #         "type": "LineString",
        #         "coordinates": (
        #             (-73.7947484, 40.7863451),
        #             (-73.7933159, 40.7867884),
        #             (-73.7931917, 40.7868285),
        #             (-73.7930816, 40.7868672),
        #             (-73.792978, 40.7869061),
        #             (-73.7928878, 40.7869409),
        #             (-73.7928086, 40.7869726),
        #             (-73.7927378, 40.7870027),
        #             (-73.7926698, 40.7870305),
        #             (-73.7921607, 40.7872621),
        #             (-73.7921252, 40.7872747),
        #             (-73.7920916, 40.7872822),
        #             (-73.7920535, 40.7872824),
        #             (-73.7920208, 40.7872736),
        #             (-73.791997, 40.7872539),
        #             (-73.7919229, 40.7871641),
        #         ),
        #     },
        # }
    ]

    awq = BuchungWriter(context='')
    
    logger.info(awq.run(a))