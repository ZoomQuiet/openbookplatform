import datetime
import time
    
def day_object_list(query_set, date_field, year, month, day):
    """
    Used for day related query_set dealing, return certain day's record-set :
    """
    try:
        date = datetime.date(*time.strptime(year+month+day, '%Y%m%d')[:3])
    except ValueError:
        return []
    now = datetime.datetime.now()
    lookup_kwargs = {
        '%s__range' % date_field: (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)),
    }
    return query_set.filter(**lookup_kwargs)

def month_object_list(query_set, date_field, year, month):
    try:
        date = datetime.date(*time.strptime(year+month, '%Y%m')[:3])
    except ValueError:
        return []
    first_day = date.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1)
    lookup_kwargs = {'%s__range' % date_field: (first_day, last_day)}
    return query_set.filter(**lookup_kwargs)
