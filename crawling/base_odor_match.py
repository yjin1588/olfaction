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
            base_name = link.string
            path = link.get('onclick').split("'")[1]
            detail_html = urlopen(path)
            detail = BeautifulSoup(detail_html, 'html.parser')
            main_type = detail.body.find('td', {"class":"qinfr2"})
            if main_type:
                main_type = main_type.string.split(': ')[1]
            else:
                pass
            types = detail.body.find_all('td', {"class":"radw5"})
            type_list = []
            for type in types:
                for t in type.find_all('a'):
                    type_list.append(t.string)
            bases.append([base_name, main_type, type_list])
    return bases

def save_csv(item_list, file_name):
    csv_file = open(file_name, 'w', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['base_type, main_odor, other_odor'])
    for item in item_list:
        csv_writer.writerow(item)
    csv_file.close()
    print('save {} file'.format(file_name))

url = 'http://www.thegoodscentscompany.com/peb-az.html'
save_name = 'dataset/base_odor_match.csv'
base_list = crawler(url)
print(base_list)
save_csv(base_list, save_name)
