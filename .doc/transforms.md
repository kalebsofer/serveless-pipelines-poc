### Transform ERD


::: mermaid
graph LR
    raw_resource[raw_resource] --> bronze_employee[bronze_employee]
    raw_resourceType[raw_resourceType] --> bronze_resourceType[bronze_resourceType]
    raw_businessUnit[raw_businessUnit] --> bronze_businessUnit[bronze_businessUnit]
    raw_deliveryElement[raw_deliveryElement] --> bronze_deliveryElement[bronze_deliveryElement]
    raw_referenceData[raw_referenceData] --> bronze_referenceData[bronze_referenceData]
    raw_resourcedActivity[raw_resourcedActivity] --> bronze_resourcedActivity[bronze_resourcedActivity]
    raw_activityAssignment[raw_activityAssignment] --> bronze_activityAssignment[bronze_activityAssignment]
    raw_account[raw_account] --> bronze_account[bronze_account]
    raw_deliveryGroup[raw_deliveryGroup] --> bronze_deliveryGroup[bronze_deliveryGroup]
    raw_activityAssignmentDemand[raw_activityAssignmentDemand] --> bronze_activityAssignmentDemand[bronze_activityAssignmentDemand]
    bronze_employee --> silver_employee[silver_employee]
    bronze_resourceType --> silver_employee
    bronze_businessUnit --> silver_employee
    bronze_activityAssignment --> silver_activityAssignment[silver_activityAssignment]
    bronze_deliveryGroup --> silver_activityAssignment
    bronze_account --> silver_activityAssignment
    bronze_activityAssignment --> silver_employeeAssignment[silver_employeeAssignment]
    bronze_resourcedActivity --> silver_employeeAssignment
    bronze_deliveryElement --> silver_employeeAssignment
    bronze_deliveryGroup --> silver_employeeAssignment
    bronze_referenceData --> silver_employeeAssignment
    bronze_employee --> silver_activeEmployeeWeek[silver_activeEmployeeWeek]
    silver_employeeAssignment --> gold_probability[gold_probability]
    silver_activeEmployeeWeek --> gold_probability
    gold_probability --> gold_employeeAssignments[gold_employeeAssignments]
    silver_employee --> gold_employeeAssignments
:::


### Query Explanations:


**Silver_employeeAssignment**
1. It first reads employee assignment data Bronze and calculates the assignment_end_dt based on the values of p1_end_dt, p2_end_dt, and p3_end_dt.
2. Then, it sorts the employee data by employee_id and assignment_id while keeping only the latest record of each assignment based on the last_modified_dt.
3. After that, it extracts year and week information from the assignment start and end dates and calculates start_yr_wk and end_yr_wk by combining the year and week numbers.
4. Next, it joins the latest employee assignments with three other tables - bronze_resourcedActivity, bronze_deliveryElement, and bronze_deliveryGroup - using LEFT JOINs. It also joins with a reference data table called bronze_referenceData to get additional information about the probability.
5. It filters the results to only include rows where the delivery_element_id is not NULL.
6. Finally, it selects all columns from the joined and filtered data to be stored in the Silver_employeeAssignment table.

**Silver_activeEmployeeWeek**

1. It starts by generating a recursive date series, called date_series, starting from the minimum employee start date found in the bronze_employee table. The date series increments by one week at a time and continues until it reaches a date that is 5 years ahead of the current date.
2. Next, it creates another temporary table called active_dates. It reads employee data from Bronze and joins it with the generated date_series. It only keeps rows where the date in the date_series falls within the employee's start and end dates (or when the end date is NULL, meaning the employee is still active).
3. It then extracts the year and week from the active dates in the active_dates table.
4. Finally, it selects the distinct combinations of employee_id, year, and week from the active_dates table and orders the results by employee_id, year, and week. This gives us a table containing active employees and their respective active weeks, which is stored in the Silver_activeEmployeeWeek table.

**Gold_probability**

1. It starts by creating a recursive temporary table called expand_weeks. This table reads employee assignment data from silver_employeeAssignments. It expands the range of weeks between the start and end weeks for each employee assignment.
2. Next, it creates another temporary table called yr_weeks that selects the employee_id, delivery_group_name, start_yr, start_wk, utilisation_percentage, probability_desc, and probability_enum from the expand_weeks table.
3. Then, it creates a temporary table called merged. It reads active employee week data from silver_activeEmployeeWeek and LEFT JOINs it with the yr_weeks table based on employee_id, year, and week. If the delivery_group_name is NULL, it replaces it with 'Chalet - Derived'. 4.If the utilisation_percentage is NULL, it replaces it with 100.
4. Finally, it selects all columns from the merged table and stores the results in the Gold_probability table. This table will contain employee probability and utilisation information for each active employee and their respective weeks.


**Gold_P1_employeeAssignments**

1. It starts by creating a temporary table called probability that filters out rows from the Gold_probability table where the probability_enum is either NULL or not in the list ('P0', 'P2', 'P3').
2. Next, it creates another temporary table called sum_util, which calculates the sum of utilisation_percentage for each employee, year, week, and yr_week combination.
3. It then creates a temporary table called merged_with_sum by joining the probability table with the sum_util table on employee_id, year, and week.
4. After that, it creates a temporary table called util_adjusted which adjusts the utilisation_percentage based on the sum_util_percentage. If the sum_util_percentage is greater than 100, the utilisation_percentage is scaled down proportionally.
5. Next, it creates a temporary table called additional_rows for cases where the sum_util_percentage is less than 100. It calculates the remaining utilisation percentage (100 - sum_util_percentage) and assigns it to a delivery group called 'Chalet - Derived'.
6. Then, it creates a temporary table called assignments by combining rows from both util_adjusted and additional_rows tables using UNION ALL.
7. Finally, it joins the assignments table with the silver_employee table (read from a parquet file) on employee_id, and filters the results to only include employee types: 'Employee UK', 'Contractor', and 'Partner Agency Team'. It selects columns from both tables and orders the results by employee_id, year, and week. The resulting table, Gold_P1_employeeAssignments, will contain the adjusted utilisation information for each employee for their respective weeks.

**Gold_P2_employeeAssignments & Gold_P3_employeeAssignments**

Do the same as above but filter on different probability_enum.
