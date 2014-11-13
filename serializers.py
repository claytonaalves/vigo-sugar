import datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")

