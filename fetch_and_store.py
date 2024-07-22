import os
import requests
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Admin SDK 초기화
cred = credentials.Certificate(os.path.expanduser('~/serviceAccountKey.json'))
firebase_admin.initialize_app(cred)
db = firestore.client()

# Global Exports 데이터 가져오기
def fetch_global_exports():
    url = "https://www.econdb.com/widgets/global-trade/data/?type=export&net=0&transform=0"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'plots' in data and len(data['plots']) > 0:
            series_data = data['plots'][0]['data']
            df = pd.DataFrame(series_data)
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            return df.to_dict(orient='records')
    return None

# SCFI 데이터 가져오기
def fetch_scfi():
    url = "https://www.econdb.com/widgets/shanghai-containerized-index/data/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'plots' in data and len(data['plots']) > 0:
            series_data = data['plots'][0]['data']
            df = pd.DataFrame(series_data)
            df['Date'] = pd.to_datetime(df['Date'])
            return df.to_dict(orient='records')
    return None

# Top Port Comparison 데이터 가져오기
def fetch_port_comparison():
    url = "https://www.econdb.com/widgets/top-port-comparison/data/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'plots' in data and len(data['plots']) > 0:
            series_data = data['plots'][0]['data']
            df = pd.DataFrame(series_data)
            return df.to_dict(orient='records')
    return None

# 데이터를 Firestore에 저장
def store_data():
    global_exports = fetch_global_exports()
    scfi = fetch_scfi()
    port_comparison = fetch_port_comparison()

    if global_exports:
        db.collection('data').document('global_exports').set({'data': global_exports})
    if scfi:
        db.collection('data').document('scfi').set({'data': scfi})
    if port_comparison:
        db.collection('data').document('port_comparison').set({'data': port_comparison})

if __name__ == "__main__":
    store_data()
