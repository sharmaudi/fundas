import calendar
from datetime import date
from datetime import datetime

import numpy as np
from simplejson import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):

        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                # noinspection PyTypeChecker
                millis = int(
                    calendar.timegm(obj.timetuple()) * 1000 +
                    obj.microsecond / 1000
                )
                return millis

            if isinstance(obj, date):
                millis = int(
                    calendar.timegm(obj.timetuple()) * 1000

                )
                return millis
            if isinstance(obj, np.int64):
                val = int(obj)
                return val
            if isinstance(obj, np.bool_):
                val = np.bool_(obj)
                if val:
                    return True
                else:
                    return False

            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
