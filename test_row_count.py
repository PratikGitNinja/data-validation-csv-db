import pytest
import pandas as pd

#  Row count validation between source and target csv file
def test_row_count_in_target_csv(source,target):

    df_filtered = source[source['customer_age'] >= 18]

    assert len(target) == len(df_filtered), "The length of target data is not as per expectation."

# Row count validation between source and target tables.
def test_row_count_in_target_table(db_connect):

    db_connect.execute("Select count(*) from customers")
    src = db_connect.fetchone()[0]
    
    db_connect.execute("Select count(*) from transactions")
    trg = db_connect.fetchone()[0]
    
    assert src == trg, "Source and target are not containing same data."

# Checking Null value in the target csv file.
def test_null_value_validation(target):

    assert target['customer_id'].isnull().sum() == 0, "There are null value in the customer_id column."
    assert target['amount_in_usd'].isnull().sum() == 0, "There are null value in the amount_in_usd column."

# Check the duplicate value in target location.
def test_no_duplicate_value_in_target(target):

    assert target.duplicated(['customer_id']).sum() == 0, f"The customer_id {target['customer_id']} is duplicate."

# To check the data types:
@pytest.mark.skip(reason="Currently we have data in csv hence don't have proper data to validate.")
def test_validate_data_type(target):

    assert target['customer_id'] == 'int64', "Incorrect datatype of customer_id."
    assert target['amount_in_usd'] == 'float64', "Incorrect data type of amount_in_usd."
    assert target['customer_age'] == 'int64', "Incoorect datatype of customer_age."

# To check transformation logic amount_in_usd = amount_in_inr / 83.
def test_validate_amount_in_usd(target,source):
    
    source['estimated_amount'] = source['amount_in_inr'] / 83
    merged = pd.merge(source,target,on='customer_id')

    merged['estimated_amount'] = merged['estimated_amount'].round(2)
    merged['amount_in_usd'] = merged['amount_in_usd'].round(2)

    mismatch = merged[merged['estimated_amount'] != merged['amount_in_usd']]
    assert mismatch.empty, f"Amount transformation mismatch: {mismatch}"

# To check the schema of the target.
def test_schema_of_target(target):

    expected_columns = ['customer_id', 'customer_name', 'amount_in_usd', 'customer_age', 'signup_date']
    assert list(target.columns) == expected_columns, "Target schema mismatch"

# To check the referential integrity.
def test_referential_integrity(target, source):

    src_ref = set(source[source['customer_age'] >= 18]['customer_id'])
    trg_ref = set(target['customer_id'])

    missing_id = src_ref - trg_ref
    assert not missing_id, f"Missing records in target: {missing_id}"

# To check the range of age is valid or not.
def test_range_of_age_in_target(target):
    assert target['customer_age'].between(18,100).all(), "Invalid age"

