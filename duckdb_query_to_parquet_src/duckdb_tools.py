import duckdb
from config import logger


def run_sql_save_res_to_parquet(sql_query, output_filename):
    "runs a duckdb query and saves the result as parquet file"

    export_sql = f"COPY ({sql_query}) TO '/tmp/{output_filename}' (FORMAT PARQUET);"
    duckdb.sql(export_sql)
    logger.info(f"Query results saved to '{output_filename}' in tmp.")
