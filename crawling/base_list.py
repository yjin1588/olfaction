from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

def crawler(url):
    bases = []
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.body.find('table')
    for item in table.find_all('tr'):
        link = item.find('a')
        if link:
            bases.append(link.string)
    return bases

def save_csv(item_list, file_name):
    csv_file = open(file_name, 'w', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['base_type'])
    for item in item_list:
        csv_writer.writerow([item])
    csv_file.close()
    print('save {} file'.format(file_name))

url = 'http://www.thegoodscentscompany.com/peb-az.html'
save_name = 'dataset/base_list.csv'
base_list = crawler(url)
#print(base_list)
save_csv(base_list, save_name)
