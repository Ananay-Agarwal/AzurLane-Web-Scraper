from bs4 import BeautifulSoup
import requests
import csv

link = 'https://azurlane.koumakan.jp/wiki/List_of_Ships'
html_text = requests.get(link).text

# Creating instance of BeautifulSoup
soup = BeautifulSoup(html_text, 'lxml')

# Finding all the <tr> tags in the webpage and saving them in the variable ship_list
ship_list = soup.find_all('tr')

def create_csv(fields, rows, dirname, filename):
    with open(dirname+filename, 'w', encoding='UTF8', newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
         
        csvwriter.writerow(fields) 
        csvwriter.writerows(rows)
    print(f"Saved csv with name {filename}")

def get_basic_ship_info():
    # The variable ship_list is a list containing multiple <td> tags which contain information on each ship
    fields = ['ID', 'Name', 'Rarity', 'Type', 'Affiliation', 'Fire Power', 'Health', 'Anti-Air', 'Evasion', 'Aviation', 'Torpedo', 'Link']
    rows = []
    for index, ship in enumerate(ship_list):
        ship_info = ship.find_all('td')
        if ship_info != []: # Condition to remove any unwanted <tr> that are not about the ships
            ship_link = "https://azurlane.koumakan.jp"+ship_info[0].a['href']
            columns = []
            for value in ship_info:
                columns.append(value.text)
            
            # If a Retrofitted Ship changes their type, remove the previous type from the database
            if ship_info[0].text.isnumeric():
                if 3000 < int(ship_info[0].text) < 4000 and len(columns) == 12:
                    columns.pop(3)
            
            columns.append(ship_link)
            rows.append(columns)
    print("Ships Scraped successfully")
    create_csv(fields, rows, 'Azur Lane Data/', 'AzurLaneShips.csv')
    
    

get_basic_ship_info()

# with open(f'Azur Lane Ships/{ship_info[0].text}_{ship_info[1].text}.text', 'w') as f:
            #     f.write(f'ID: {ship_info[0].text}\n')
            #     f.write(f'Name: {ship_info[1].text}\n')
            #     f.write(f'Rarity: {ship_info[2].text}\n')
            #     f.write(f'Type: {ship_info[3].text}\n')
            #     f.write(f'Affiliation: {ship_info[4].text}\n')
            #     f.write(f'Fire Power: {ship_info[5].text}\n')
            #     f.write(f'Health: {ship_info[6].text}\n')
            #     f.write(f'Anti-Air: {ship_info[7].text}\n')
            #     f.write(f'Evasion: {ship_info[8].text}\n')
            #     f.write(f'Aviation: {ship_info[9].text}\n')
            #     f.write(f'Torpedo: {ship_info[10].text}\n')
            #     f.write(f'Link: {ship_link}\n')
            # print(f"File Saved: {index}")