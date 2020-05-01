import datetime


def json_converter(o):
    if isinstance(o, datetime.date):
        return o.__str__()
