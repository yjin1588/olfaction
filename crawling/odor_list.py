from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

def crawler(url):
    odors = []
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.body.find_all('td', {"class":"llstw26"}):
        odors.append(item.text.strip())
    return odors

def save_csv(item_list, file_name):
    csv_file = open(file_name, 'w', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['odor_type'])
    for item in item_list:
        csv_writer.writerow([item])
    csv_file.close()
    print('save {} file'.format(file_name))


url = 'http://www.thegoodscentscompany.com/allodor.html'
save_name = 'odor_list.csv'
odor_list = crawler(url)
#print(odor_list)
save_csv(odor_list, save_name)
