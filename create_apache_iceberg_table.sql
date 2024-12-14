CREATE DATABASE athena_iceberg_db;

CREATE TABLE osm_data (
  osmid STRING,
  highway STRING,
  maxspeed STRING,
  name STRING,
  oneway BOOLEAN,
  reversed BOOLEAN,
  length DOUBLE,
  geometry STRING,
  lanes STRING,
  ref STRING,
  access STRING,
  bridge BOOLEAN,
  tunnel BOOLEAN,
  width DOUBLE,
  junction STRING
)
PARTITIONED BY (highway, bucket(16, osmid))  -- Using `bucket(16, osmid)` as a secondary partition key
LOCATION 's3://apache-iceberg-table/apache-iceberg-folder'  -- Change to your actual S3 bucket and path
TBLPROPERTIES (
  'table_type'='ICEBERG',
  'format'='parquet',
  'write_compression'='snappy',
  'optimize_rewrite_delete_file_threshold'='10'
);