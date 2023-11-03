import requests
import pandas as pd

# The API endpoint URL
url = 'https://internal.api.vitruvi.cc/api/v1/production/production_reports/'
params = {
    'created_by': 58,
    'created_from': '2023-07-23'
}
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 7M8AE85Ko65VoqR5P1kEnoch0rIwk3AxEsorWNmt'
}

# Make the GET request
response = requests.get(url, params=params, headers=headers)
pr_data = response.json()
pr_df = pd.json_normalize(pr_data['results'])
pr_df.set_index('id', inplace=True)


prl_url = 'https://internal.api.vitruvi.cc/api/v1/production/production_report_lines/'
res = list()
for pr_id in pr_df.index.values.tolist():
    url = prl_url + f'{pr_id}' + '/'
    response = requests.get(url, headers=headers)
    res.append(response.json())
prl_df = pd.json_normalize(res)


prq_ids = [id for sublist in prl_df['quantities'].dropna().tolist() for id in sublist]
prq_url = 'https://internal.api.vitruvi.cc/api/v1/production/production_report_quantities/'
res = list()
for prq_id in prq_ids:
    url = prl_url + f'{pr_id}' + '/'
    response = requests.get(url, headers=headers)
    res.append(response.json())
prq_df = pd.json_normalize(res)




