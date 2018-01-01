import json
import datetime
from time import mktime


class TimestampEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, datetime.datetime):
            r_obj = int(mktime(obj.timetuple()))
            print(r_obj)
            return r_obj

        return json.JSONEncoder.default(self, obj)
