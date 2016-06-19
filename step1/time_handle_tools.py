
ERROR_DATE = ['20130931'] 

def add_zero(num):
    if num < 10:
        return '0' + str(num)
    else:
        return str(num)

list_day = [add_zero(x) for x in range(1, 32)]
list_month = ['08', '09', '10', '11']

list_date = ['2013' + m + d for m in list_month for d in list_day]
list_date = [d for d in list_date if d not in ERROR_DATE]

# the list of date from 2013-08-01 to 2013-11-14 in %Y%m%d
list_date = list_date[:-17]


def time_handle(sec_str):
    '''
    handle the the time to %H%M%S
    Input: the result of int everyday time in sql
    '''
    if sec_str == 'NULL':
        return None
    if len(sec_str) <= 6 and len(sec_str) >= 2:
        return (6 - len(sec_str)) * '0' + sec_str
    else:
        return None

