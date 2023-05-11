from main import local_entry_point

test_request = {
    "object_name": "Account",
    "saving_option": "latest_and_historic",
    "bucket": "internalforecast-data-bronze",
}

local_entry_point(test_request)
