import requests,zipfile, io
import pandas as pd
import concurrent.futures


def download_bse_bhavcopy(date, save_location):
    date_str = date.strftime('%d%m%y')
    date_str_file = date.strftime('%d%m%Y')
    url = "http://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.zip".format(date_str)
    r = requests.get(url)

    if r.status_code >= 500:
        count = 0
        print(f"Received Error code {r.status_code} while downloading for date ${date_str} from url {url}. Retrying..")
        while r.status_code >= 500:
            count += 1
            print(f"[{date_str}] Retry {count}")
            r = requests.get(url)
            if count >= 10:
                break

    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print(z.namelist())
        dt = f"EQ{date_str_file}.csv"
        df = pd.read_csv(z.open(f"EQ{date_str}.CSV"))
        df = df[df.SC_TYPE == 'Q']

        df = df.set_index('SC_CODE')
        df = df[['SC_NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'NO_OF_SHRS']]
        df['DATE'] = date_str_file

        date_str = date.strftime('%d%b%Y').upper()
        df.to_csv(f"{save_location}/BSEEQ{date_str}.csv")
    else:
        raise ValueError(f"Received Error code {r.status_code} while downloading for date ${date_str} from url ${url}")


def download_nse_bhavcopy(date, save_location):
    date_str = date.strftime('%d%b%Y').upper()
    date_str_file = date.strftime('%d%m%Y')

    year = date.strftime('%Y')
    month = date.strftime('%b').upper()
    name = f"cm{date_str}bhav"
    zip_name = f"{name}.csv.zip"
    csv_name = f"{name}.csv"
    url = f"http://www.nseindia.com/content/historical/EQUITIES/{year}/{month}/{zip_name}"
    r = requests.get(url)

    if r.status_code >= 500:
        count = 0
        print(f"Received Error code {r.status_code} while downloading for date ${date_str} from url {url}. Retrying..")
        while r.status_code >= 500:
            count += 1
            print(f"[{date_str}] Retry {count}")
            r = requests.get(url)
            if count >= 10:
                break

    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print(z.namelist())
        df = pd.read_csv(z.open(csv_name))

        df = df.set_index('SYMBOL')
        df = df.query('SERIES == "EQ" or SERIES == "BE"')
        df = df[['ISIN', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TOTTRDQTY']]
        df['DATE'] = date_str_file
        df.to_csv(f"{save_location}/NSEEQ{date_str}.csv")
    else:
        raise ValueError(f"Received Error code {r.status_code} while downloading for date ${date_str} from url ${url}")


def get_bse_bhavcopy(start=None, end=None, periods=5, save_location='.'):
    if not end:
        end = pd.datetime.today()

    if not start:
        datelist = pd.bdate_range(end=end, periods=periods).tolist()
    else:
        datelist = pd.bdate_range(start=start, end=end).tolist()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_score = {}
        error_list = []

        for d in datelist:
            date_str = d.strftime('%d%m%y')
            future_score.update({executor.submit(download_bse_bhavcopy, d, save_location): date_str})

        for future in concurrent.futures.as_completed(future_score):
            date_str = future_score[future]
            try:
                future.result()
                print(f"{date_str} is done")
            except Exception as exc:
                print(f"{date_str} generated error: ${exc}")


def get_nse_bhavcopy(start=None, end=None, periods=5, save_location='.'):
    if not end:
        end = pd.datetime.today()

    if not start:
        datelist = pd.bdate_range(end=end, periods=periods).tolist()
    else:
        datelist = pd.bdate_range(start=start, end=end).tolist()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_score = {}
        error_list = []

        for d in datelist:
            date_str = d.strftime('%d%m%y')
            future_score.update({executor.submit(download_nse_bhavcopy, d, save_location): date_str})

        for future in concurrent.futures.as_completed(future_score):
            date_str = future_score[future]
            try:
                future.result()
                print(f"{date_str} is done")
            except Exception as exc:
                print(f"{date_str} generated error: ${exc}")