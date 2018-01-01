import os
from datetime import datetime
from pathlib import Path

import requests

res = requests.post('https://q.zerodha.com/?next=', data={
    'username': 'RA5229',
    'password': 'Chandamama11'
})

session = res.cookies['session']

tradebook = 'https://q.zerodha.com/report/tradebook/'

t = datetime.now()
to_date = t.strftime('%d/%m/%Y')

data = {
    'select_report': 'ALL-EQ',
    'symbol': '',
    'from_date': '01/10/2016',
    'to_date': to_date,
    'submit': 'Download'
}

cookies = {
    'session': session
}

local_filename = '/Users/Udit/Dropbox/Watchlist/tradebook.xlsx'

file = Path(local_filename)

if file.is_file():
    print("File already exists. Removing")
    os.remove(local_filename)

print("Downloading tradebook with data {}".format(data))
t_res = requests.post(tradebook, data=data, cookies=cookies, stream=True)
print(t_res.status_code)
with open(local_filename, 'wb') as f:
    for chunk in t_res.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
print("Tradebook downloaded")