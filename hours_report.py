import requests
from urllib.parse import urljoin
import pandas as pd
from datetime import datetime

USER_PROFILE_ID = 58
API_TOKEN = '7M8AE85Ko65VoqR5P1kEnoch0rIwk3AxEsorWNmt'

BASE_URL = 'https://internal.api.vitruvi.cc'
PODUCTION_REPORT_URL = 'api/v1/raw/production/productionreport'
PODUCTION_REPORT_LINE_URL = 'api/v1/raw/production/productionreportline'
WORK_ITEM_URL = 'api/v1/raw/wbs/workitem'
WORK_ITEM_QUANTITY_URL = 'api/v1/raw/wbs/workitemquantity'
PODUCTION_REPORT_QUANTITY_URL = 'api/v1/raw/production/productionreportquantity'
QUANTITY_DESCRIPTION_URL = 'api/v1/raw/core/quantitydescription'

headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {API_TOKEN}'
}



# PR
url = urljoin(BASE_URL, PODUCTION_REPORT_URL)
params = {
    'created_by_id': USER_PROFILE_ID,
    'submitted_date__gte': (datetime.now().date() - timedelta(weeks=8)).strftime('%Y-%m-%d')
}

response = requests.get(url, params=params, headers=headers)
pr_data = response.json()
pr_df = pd.json_normalize(pr_data['results'])

pr_id_lst = set(pr_df['id'].tolist())
pr_id_str = ','.join(map(str, pr_id_lst))


# PRL
url = urljoin(BASE_URL, PODUCTION_REPORT_LINE_URL)

params = {
    'production_report_id__in': pr_id_str
}
response = requests.get(url, params=params, headers=headers)
prl_data = response.json()
prl_df = pd.json_normalize(prl_data['results'])

prl_id_lst = set(prl_df['id'].tolist())
prl_id_str = ','.join(map(str, prl_id_lst))

wi_id_lst = set(prl_df['work_item_id'].tolist())
wi_id_str = ','.join(map(str, wi_id_lst))

# Work Items
url = urljoin(BASE_URL, WORK_ITEM_URL)
params = {
    'id__in': wi_id_str
}

response = requests.get(url, params=params, headers=headers)
wi_data = response.json()
wi_df = pd.json_normalize(wi_data['results'])



# WIQ
url = urljoin(BASE_URL, WORK_ITEM_QUANTITY_URL)

params = {
    'work_item_id__in': wi_id_str
}
response = requests.get(url, params=params, headers=headers)
wiq_data = response.json()
wiq_df = pd.json_normalize(wiq_data['results'])


# PRQ

url = urljoin(BASE_URL, PODUCTION_REPORT_QUANTITY_URL)
params = {
    'production_report_line_id__in': prl_id_str
}

response = requests.get(url, params=params, headers=headers)
prq_data = response.json()
prq_df = pd.json_normalize(prq_data['results'])

quantity_descriotion_id_lst = set(prq_df['quantity_description_id'].tolist())
quantity_descriotion_id_str = ','.join(map(str, quantity_descriotion_id_lst))

# Quantity_description

url = urljoin(BASE_URL, QUANTITY_DESCRIPTION_URL)

params = {
    'id__in': quantity_descriotion_id_str
}

response = requests.get(url, params=params, headers=headers)
quantity_description_data = response.json()
quantity_description_df = pd.json_normalize(quantity_description_data['results'])

