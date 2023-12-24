import requests
from urllib.parse import urljoin
import pandas as pd
from datetime import datetime, timedelta

STEP = 10000

def main():

    base_url = "https://lit-fibre.api.vitruvi.cc/api/v1/raw/engineering/designelement"

    payload={}
    headers = {
    'Authorization': 'Bearer UXRpFnPRr3eGAKgS3ug9Yb3F11b14JzSbRlPfCjj'
    }

    # start_url = base_url + f'?limit={STEP}'

    # cnt = 0
    next_url = base_url+ f'?limit={STEP}'
    res_df = None
    while next_url:
        response = requests.request("GET", next_url, headers=headers, data=payload)
        response_json = response.json()
        if response.status_code != 200:
            print(f'response.status_code {response.status_code}')
        next_url = response_json.get('next')
        print(f'next_url: {next_url}')

        pr_df = pd.json_normalize(response_json['results'])
        if 'cf_values.cbt_live_ports' not in pr_df.columns:
            continue
        
        selected_df = pr_df[['label', 'cf_values.cbt_live_ports']].dropna()
        selected_df = selected_df.loc[pd.notna(pr_df['cf_values.cbt_live_ports'])]
        if res_df is not None:
            res_df = pd.concat([res_df, selected_df], ignore_index=True)
        else:
            res_df = selected_df

        # cnt+= 1
        # if cnt > 10:
        #     break
    filename = '/tmp/des.csv'
    res_df.to_csv(filename, index=False)

if __name__=='__main__':
    main()
