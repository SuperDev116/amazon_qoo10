import json
from openpyxl import Workbook


with open('qoo10CategoryList.json', encoding='utf-8') as f:
    data = json.load(f)

print(data)

# Create a new workbook
workbook = Workbook()
sheet = workbook.active

# Write the headers
headers = list(data['ResultObject'][0].keys())
sheet.append(headers)

# Write the data to the worksheet
for item in data['ResultObject']:
    print(item['CATE_M_CD'])