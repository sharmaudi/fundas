from app.util.Screener import Screener


def get_screener_dicts(screener_code=None, bse_code=None, company_info=None):

    if not screener_code:
        screener_code = company_info.screener_code
        bse_code = company_info.bse_code

    scr = None
    try:
        scr = Screener(screener_code)
    except:
        try:
            scr = Screener(bse_code)
        except Exception as e:
            raise e
    d1 = scr.company_data_standalone
    d2 = scr.company_data
    std = _process_screener_dict(d1)
    con = _process_screener_dict(d2)

    if std:
        std = std['stats']

    if con:
        con = con['stats']

    return {
        'standalone': std,
        'consolidated': con
    }


def _process_screener_dict(d1):
    d2 = {key: value for (key, value) in d1['warehouse_set'].items()}
    del d1['announcement_set']
    del d1['annualreport_set']
    del d1['companyrating_set']
    del d1['number_set']
    del d1['warehouse_set']
    # del d2['analysis']
    return {
        'info': d1,
        'stats': d2
    }
