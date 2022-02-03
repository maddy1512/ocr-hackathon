import os
import random, string
from datetime import datetime, timedelta


def generate_isin(n=10):
    isin_data = []
    for i in range(n):
        x = "".join(random.choices(string.ascii_uppercase, k=2))
        x = x + "".join(random.choices(string.digits, k=10))
        x = "__label__ISIN " + x
        isin_data.append(x)
    return isin_data

def gen_datetime(min_year=2009, max_year=datetime.now().year, n = 10):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    formats = ["%x", "%c", "%d-%m-%y", "%d/%m/%y", "%d/%m/%Y", "%m/%d/%Y", "%m-%d-%Y", "%d-%m-%Y", "%d %B %Y", "%d %b %Y", "%d-%b-%Y", "%d %m %Y %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S"]
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    dates_str = []
    for i in range(n):
        d = start + (end - start) * random.random()
        size = len(formats)
        str_d = "__label__DATE "+d.strftime(formats[random.randint(0,size-1)])
        dates_str.append(str_d)
    return dates_str

def gen_amount(n=10):
    curr = ["USD", "ACK", "GBP", "CNY", "EUR", "INR"]
    curr_len = len(curr)
    amounts = []
    for i in range(n):
        rounded_number = str(round(random.uniform(1, 1000000), 2))
        currency = curr[random.randint(0,curr_len-1)]
        final_amt = "__label__AMOUNT "+rounded_number +" " +currency
        amounts.append(final_amt)
    return amounts
def gen_other_alpha_l(n=1):
    n = random.randint(1,5)
    x = ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
    x = "__label__OTHER " + x
    return [x]

def gen_other_alpha_u(n=1):
    n = random.randint(1,5)
    x = ''.join(random.choice(string.ascii_uppercase) for _ in range(n))
    x = "__label__OTHER " + x
    return [x]

def gen_other_alpha_n(n=1):
    n = random.randint(1,5)
    x = ''.join(random.choice(string.digits) for _ in range(n))
    x = "__label__OTHER " + x
    return [x]

function_list = [generate_isin, gen_datetime, gen_amount]
function_list_oth = [gen_other_alpha_l, gen_other_alpha_n, gen_other_alpha_u]

len_of_fun = len(function_list)
len_of_fun_oth = len(function_list_oth)
data = []
for i in range(400000):
    data.extend(function_list[random.randint(0,len_of_fun-1)](n=1))
for i in range(200000):
    data.extend(function_list_oth[random.randint(0,len_of_fun_oth-1)](n=1))
lines = "\n".join(data)
f = open("train.txt", "a+")
f.write(lines)