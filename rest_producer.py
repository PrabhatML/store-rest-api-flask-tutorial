import requests
import csv

url = "http://api.plos.org/search?q=title:DNA"

response = requests.request("GET",url)

data =response.json()["response"]["docs"] 
# csv_data = []

for i in data:
    print(f'{i["id"]}-------{i["journal"]}----------{i["article_type"]}')
    # csv_data.append([i['id'],i['journal'],i['article_type']])

# with open("data.csv",'w') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerows(csv_data)