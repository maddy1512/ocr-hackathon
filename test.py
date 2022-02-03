import nltk
import re
from pprint import pprint
# # Reka setup with stopword directory
# stop_dir = "SmartStoplist.txt"
# rake_object = RAKE.Rake(stop_dir)
#
# # Sample text to test RAKE
from nltk.tag import StanfordNERTagger


def ie_preprocess(document):
    document = ' '.join([i for i in document.split()])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


def extract_Org(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if (chunk.label() == 'ORGANIZATION') or (chunk.label() == 'PERSON'):
                    names.append(' '.join([c[0] for c in chunk]))
    return names


def merge(s):
    # initialization of string to ""
    new = ""

    new = " ".join(s)

    # return string
    return new


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


text = """
From: Fax
To:0099898989
Uper Firm
Uper Firm Limited
Telephone: +9199008899
E-Mail:
-fundadmin@pertiem.co
29-03-2019
Fund Order Id : BR62323
SUBSCRIPTION
Fund
ISIN
Amount
HSS DBS. F.
IS1134334560
1001.20 USD
Dynamic Fund
IS1134334560
5001.23 USD
NY Fund
IS1134334560
6505.98 USD
Total
12508.41USD
Regards,
Uper Firm
INTERNAL
"""

# Extract keywords
# keywords = rake_object.run(text)
# print ("keywords: ", keywords)
match = re.search(r'[\w\.-]+@[\w\.-]+', text)
email = match.group(0)

st = text.find("Fund order id")
match = re.search(r'(O|o)rder (I|i)d.*', text)
order_id = ""
if match:
    order_id = match.group(0)
    if ":" in order_id:
        order_id = order_id.split(": ")[1]
# print(order_id)
total_grp = re.search(r"(?<=Total\n).*", text)
total = ""
if total_grp:
    total = total_grp.group(0)
# print(total)

r = re.compile(
    r'(\+\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\+\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\+\d{3}[-\.\s]??\d{4}|\+\d{2}[-\.\s]??\d{4}[-\.\s]\d{6})')
phone_numbers = r.findall(text)
phone_number = ""
if phone_numbers:
    if len(phone_numbers) > 0:
        phone_number = phone_numbers[0]

date_strings = re.search("(\d+\-\d+\-\d+)", text)
date_str = ""
if date_strings:
    date_str = date_strings.group(0)

# print(date_str)

lines = text.split("\n")
line_num_of_isin = None
for num, line in enumerate(lines, 1):
    if "ISIN" in line:
        line_num_of_isin = num
        break
# st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
fund_name = ""
isin_data = ""
# if line_num_of_isin:
#     isin_data = lines[line_num_of_isin]
#     fund_name = merge(extract_Org(isin_data))
#     if fund_name:
#         isin_data = isin_data.replace(fund_name, "")
#         isin_data = isin_data.replace(total, "").replace(" ", "")
        # print(isin_data)
data_dict = {"date": date_str, "amount": total, "phone_number": phone_number, "email": email,
             "order_id": order_id}
end_line_num = line_num_of_isin
for num, line in enumerate(lines, 0):
    if "Total" in line:
        end_line_num = num
        break

statements = lines[line_num_of_isin+1:end_line_num]
statement_dict=[]
for i in range(0,len(statements),3):
    stat = {"fund_name":statements[i],"isin":statements[i+1],"amount":statements[i+2]}
    statement_dict.append(stat)
data_dict["statements"] = statement_dict
pprint(data_dict)