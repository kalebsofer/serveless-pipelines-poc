from main import local_entry_point

test_request = {
    "bigquery_query": "SELECT year FROM `forecasting-test-382708.dev_temp_tables.gold_test_1` LIMIT 1000",
    "result_table_name": "test_bq_query",
    "result_dataset_name": "internal_forecast_bronze",
}

local_entry_point(test_request)
