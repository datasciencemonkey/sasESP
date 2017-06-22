__author__ = 'sgangichetty'

import pandas as pd

from dbOperations import insert_records_to_db

# Read CSV file as-is and assign customer ID
raw_data = pd.read_csv('sampled_down_dataset_fitsaddress.csv')

# Assign Customer_ID and adjust for sqlite data type handlers

raw_data['customer_id'] = 57685898 + raw_data.index  # Starting value - User specified
raw_data['fraud'] = raw_data.fraud.astype(float)
raw_data['existing_ecom_customer'] = raw_data.existing_ecom_customer.astype(float)
raw_data['customer_id'] = raw_data.customer_id.astype(float)
raw_data['ZipCode'] = raw_data.ZipCode.astype(str)
raw_data['CCNumber'] = raw_data.CCNumber.astype(str)
raw_data['CVV2'] = raw_data.CVV2.astype(str)

# raw_data['total_session_length'] = raw_data.total_session_length.round(2)
# raw_data['time_on_cart'] = raw_data.time_on_cart.round(2)
# raw_data['total_visit_clicks'] = raw_data.total_visit_clicks.astype(int)
# raw_data['pageview_pre_purchase_visits'] = raw_data.pageview_pre_purchase_visits.astype(int)
# raw_data['product_view_count'] = raw_data.product_view_count.astype(int)

# Write to DB & ignore column x at the same time

write_df = raw_data.ix[:, raw_data.columns != 'x']

# Function Call to write to db
insert_records_to_db(write_df, 'transactions.db')

# Now, generate a stream
