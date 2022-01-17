import shutil
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Cookie': 'browserid=2355938487786925966; timezoneOffset=7200,0; strInventoryLastContext=753_0; steamCurrencyId=3; steamMachineAuth76561198093402962=B4EA0C3201CEC853D81A240930CCA8A4D09B44A3; steamRememberLogin=76561198093402962||ff1157126b796d4ff34406f9d77fae4b; gameslist_sort=achievements; _ga=GA1.2.515132221.1642205320; _gid=GA1.2.1415070889.1642205320; steamLoginSecure=76561198093402962||F04BA573C40F6FB644EFC1C7AD3D4CA45338E2CB; sessionid=90d9716ff0fd4621ef5ebae4; webTradeEligibility={"allowed":1,"allowed_at_time":0,"steamguard_required_days":15,"new_device_cooldown_days":7,"time_checked":1642404360}; steamCountry=EE|8668a41612a602518f6126e21196a552;'
})

hubs_to_monitor = [
    'https://steamcommunity.com/app/1126320/screenshots/?p=1&browsefilter=mostrecent',
    'https://steamcommunity.com/app/1607130/screenshots/?p=1&browsefilter=mostrecent'
]

hub_screenshots_url_template = 'https://steamcommunity.com/app/1607130/screenshots/?p=1&browsefilter=mostrecent'

response = requests.get(hubs_to_monitor[1])

soup = BeautifulSoup(response.content, 'html.parser')
i = 1
for card in soup.find_all('div', {'class': 'apphub_Card'}):
    file_id = card.attrs['data-publishedfileid']
    image_url = card.find('img', {'class': 'apphub_CardContentPreviewImage'}).attrs['src']
    image_response = requests.get(image_url, stream=True)
    if image_response.status_code == 200:
        with open(f'media/{i}.jpeg', 'wb') as f:
            shutil.copyfileobj(image_response.raw, f)
        print(f'Image retrieved')
    else:
        print('Failed to get image')
    i += 1


# with open('to_report.txt', 'r') as f:
#     lines = f.readlines()
#
# for line in lines:
#     id_to_report = int(urlparse(line).query.split('id=')[1])
#     print(id_to_report)
#     response = session.post('https://steamcommunity.com/sharedfiles/reportitem', {
#         'id': id_to_report,
#         'description': 'Inappropriate/pron https://help.steampowered.com/en/faqs/view/6862-8119-C23E-EA7B',
#         'sessionid': '90d9716ff0fd4621ef5ebae4'
#     })
#
#     print(response.json())
