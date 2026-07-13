import csv
import json  

headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
 ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
 ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
 ]
with open('sample.csv')as f:
    f.csv=csv.reader(f)
    header=next(f.csv)
    for row in f.csv:
        print(row) 
    f_csv=csv.writer(f)
    f.csv.write

    f_csv=csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)

data={
    'name':'ACME',
    'shares':100,
    'price':542.23
}

with open('data.json','w')as f:
    json.dump(data,f)
with open('data.json','r')as f:
    data=json.load(f)
    print(data)