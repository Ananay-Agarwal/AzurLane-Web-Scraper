from bs4 import BeautifulSoup
import requests

link = 'https://azurlane.koumakan.jp/wiki/List_of_Ships'
html_text = requests.get(link).text

# Creating instance of BeautifulSoup
soup = BeautifulSoup(html_text, 'lxml')

# Finding all the <tr> tags in the webpage and saving them in the variable ship_list
ship_list = soup.find_all('tr')

# The variable ship_list is a list containing multiple <td> tags which contain information on each ship
for index, ship in enumerate(ship_list):
    ship_info = ship.find_all('td')
    if ship_info != []:
        ship_link = "https://azurlane.koumakan.jp"+ship_info[0].a['href']
        with open(f'Azur Lane Ships/{ship_info[0].text}_{ship_info[1].text}.text', 'w') as f:
            f.write(f'{ship_info[0].text}\n')
            f.write(f'Name: {ship_info[1].text}\n')
            f.write(f'Rarity: {ship_info[2].text}\n')
            f.write(f'Type: {ship_info[3].text}\n')
            f.write(f'Affiliation: {ship_info[4].text}\n')
            f.write(f'Fire Power: {ship_info[5].text}\n')
            f.write(f'Health: {ship_info[6].text}\n')
            f.write(f'Anti-Air: {ship_info[7].text}\n')
            f.write(f'Evasion: {ship_info[8].text}\n')
            f.write(f'Aviation: {ship_info[9].text}\n')
            f.write(f'Torpedo: {ship_info[10].text}\n')
            f.write(f'Link: {ship_link}\n')
        print(f"File Saved: {index}")

