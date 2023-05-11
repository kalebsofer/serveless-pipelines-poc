from main import local_entry_point

test_request = {
    "duckdb_query": """
            SELECT 
                Id as id
                , KimbleOne__ResourceType__c as emp_type
                , KimbleOne__BusinessUnit__c as capability
                , case 
                    when KC_GradeAndRole__c[:4] = 'SFIA'
                        then KC_GradeAndRole__c[6]
                    when KC_GradeAndRole__c[1] = '_' and len(KC_GradeAndRole__c) > 1
                        then REGEXP_REPLACE(KC_GradeAndRole__c, '\D+', '')
                    else NULL
                end as sfia_level
                , case 
                    when KC_GradeAndRole__c[:4] = 'SFIA'
                        then KC_GradeAndRole__c[7:]
                    else NULL
                end as role
                , KimbleOne__Location__c as location
                , KimbleOne__StartDate__c as start_dt
                , KimbleOne__EndDate__c as end_dt
                , KimbleOne__StandardCost__c as std_cost
                , KimbleOne__StandardRevenue__c as std_revenue
                , current_timestamp as request_ts
            FROM read_json_auto('/tmp/KimbleOne__Resource__c/latest/data.jsonl', auto_detect=true, maximum_object_size = 100000000, sample_size=100000)
        """,
    "data_sources": [
        {
            "data_source_path_and_name": "KimbleOne__Resource__c/latest/data.jsonl",
            "data_source_bucket": "internalforecast-data-raw",
        },
    ],
    "result_name": "bronze_employee",
    "result_bucket": "internalforecast-data-bronze",
    "saving_option": "latest_and_historic",
    "create_bigquery_table": "TRUE",
    "bigquery_dataset_name": "internal_forecast_bronze",
}

local_entry_point(test_request)
