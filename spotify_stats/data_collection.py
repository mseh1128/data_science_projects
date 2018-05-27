import requests
import csv
import os
from bs4 import BeautifulSoup as soup


def save_weekly_csv(url, weekly_range):
    decoded_content = url.content.decode('utf-8')
    file_reader = csv.reader(decoded_content.splitlines(), delimiter=',')
    with open(f'{dir_name}/{weekly_range}', 'w', encoding='utf-8') as weekly_data:
        csv_writer = csv.writer(weekly_data)
        csv_writer.writerows(file_reader)


spotify_weekly_charts = requests.get('https://spotifycharts.com/regional/global/weekly/').text
weekly_charts = soup(spotify_weekly_charts, 'lxml')
date_ranges = weekly_charts.find('div', class_='chart-filters-list').find_all('ul')[2]
dir_name = 'weekly_data'
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
for weekly_date in date_ranges.find_all('li'):
    date_range = weekly_date['data-value']
    weekly_url = f'https://spotifycharts.com/regional/global/weekly/{date_range}/download'
    save_weekly_csv(requests.get(weekly_url), date_range)
