from bs4 import BeautifulSoup
import requests
import csv

link = 'https://azurlane.koumakan.jp/wiki/List_of_Ships'
html_text = requests.get(link).text

# Creating instance of BeautifulSoup
soup = BeautifulSoup(html_text, 'lxml')

# Finding all the <tr> tags in the webpage and saving them in the variable ship_list
# The variable ship_list is a list containing multiple <td> tags which contain information on each ship
ship_list = soup.find_all('tr')

def create_csv(fields, rows, dirname, filename):
    with open(dirname+filename, 'w', encoding='UTF8', newline='') as csvfile: 
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields) 
        csvwriter.writerows(rows)
    print(f"Saved csv with name {filename}")

def get_basic_ship_info():
    # Creating the fields to store in the csv
    fields = ['id', 'name', 'rarity', 'type', 'faction', 'link']
    rows = []

    # extracting all the ship details from the <td> tags
    for ship in ship_list:
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
            
            columns = columns[0:5] # Removing the stats of the ships
            columns.append(ship_link)
            rows.append(columns)
    print("Ships Scraped successfully")
    get_detailed_ship_info(rows)
    # create_csv(fields, rows, 'Azur Lane Data/', 'AzurLaneShips.csv') # Use if only the basic details are needed (the ones in the field variable)

def get_detailed_ship_info(basic_info):
    fields = ['ship_id', 'name', 'rarity', 'type', 'faction', 'full_name', 'construction_time', 'class', 'health', 'fire_power', 'torpedo', 'aviation', 'anti_air', 'reload','evasion', 
                'speed', 'accuracy', 'luck', 'asw', 'oil_consumption', 'armour', 'gear_efficiency', 'gear_equippable', 'tech_point_collection', 'tech_point_mlb', 'tech_point_120',
                'enhacement_value', 'scrap_value']
    rows = []
    for ship in basic_info:
        print(f"Retrieving information on {ship[1]}...........", end="")
        # Skipping one page because god knows why it is made totally different from everything else
        if ship[0] == "248":
            print("Skipped")
            continue

        # Getting page information of the page
        link = ship[5]
        html_text = requests.get(link).text
        ship_page = BeautifulSoup(html_text, 'lxml')

        # Getting basic information of the ship from 1st table
        info_box = ship_page.find('div', style="display:flex; flex-direction:column; position:relative; width:100%")
        full_name = info_box.find('div', style="background:rgba(255,255,255,0.25); font-size:90%; font-weight:500; padding:3px 0 3px 30px").b.text
        info_box_table = info_box.find_all('td')
        construction_time = info_box_table[0].text.strip()
        ship_class = info_box_table[len(info_box_table)-1].text.strip()

        # Getting stats of the ship from 2nd table
        stat_table = ship_page.find('div', style="margin-top:20px")
        ship_stats = stat_table.find_all('tr')
        ship_stats.pop(0) # Removing first row which contains the headers
        ship_stats.pop() # Removing last row which has no information

        # If the ship is a submarine, remove the hunting range table
        if "Submarine" in ship[3]:
            ship_stats = ship_stats[0:1]+ship_stats[8:]
        health = []
        fire_power = []
        torpedo = []
        aviation = []
        anti_air = []
        reload = []
        evasion = []
        speed = []
        accuracy = []
        luck = []
        asw = []
        oil_consumption = []
        armour = ""
        is_retrofit = False
        if ship[0].isnumeric():
            if 3000 < int(ship[0]) < 4000:
                for level in ship_stats:
                    stats = level.find_all('td', limit = 14)
                    if stats[0].text.strip() == "Level 125 Retrofit":
                        armour = stats[8].text.strip()
                        stats.pop(8)
                    if "Retrofit" in stats[0].text.strip() or stats[0].text.strip() == "Base":
                        health.append(int(stats[1].text.strip()))
                        fire_power.append(int(stats[2].text.strip()))
                        torpedo.append(int(stats[3].text.strip()))
                        aviation.append(int(stats[4].text.strip())) 
                        anti_air.append(int(stats[5].text.strip())) 
                        reload.append(int(stats[6].text.strip()))
                        evasion.append(int(stats[7].text.strip())) 
                        speed.append(int(stats[8].text.strip()))
                        accuracy.append(int(stats[9].text.strip())) 
                        luck.append(int(stats[10].text.strip()))
                        asw.append(int(stats[11].text.strip()))
                        oil_consumption.append(int(stats[12].text.strip()))
                is_retrofit = True
        if not is_retrofit:
            for level in ship_stats:
                stats = level.find_all('td')
                
                if "Retrofit" in stats[0].text.strip():
                    if stats[0].text.strip() == "Level 125 Retrofit":
                        armour = stats[8].text.strip()
                        stats.pop(8)
                    else:
                        continue
                if stats[0].text.strip() == "Level 125" and armour == "":
                    armour = stats[8].text.strip()
                    stats.pop(8)
                # print(stats)
                health.append(int(stats[1].text.strip()))
                fire_power.append(int(stats[2].text.strip()))
                torpedo.append(int(stats[3].text.strip()))
                aviation.append(int(stats[4].text.strip())) 
                anti_air.append(int(stats[5].text.strip()))
                reload.append(int(stats[6].text.strip()))
                evasion.append(int(stats[7].text.strip())) 
                speed.append(int(stats[8].text.strip()))
                accuracy.append(int(stats[9].text.strip())) 
                luck.append(int(stats[10].text.strip()))
                asw.append(int(stats[11].text.strip()))
                oil_consumption.append(int(stats[12].text.strip()))
        
        # Get the equippable gear details
        gear_table = ship_page.find('table', class_ = "wikitable" ,style="text-align:center; width:100%")
        gear_rows = gear_table.find_all('tr')
        gear_rows = gear_rows[2:]
        gear_efficiency = []
        gear_equippable = []
        for gear in gear_rows:
            gear_cell = gear.find_all('td')
            gear_efficiency.append(gear_cell[1].text.strip())
            gear_equippable.append(gear_cell[2].text.strip())
        
        # Get the 2 tables for [fleet point info] and [enhancement value and scrap value]
        double_table = ship_page.find_all('table', class_ = "wikitable" ,style="width:100%")
        tech_point_table = double_table[0]
        value_table = double_table[1]
        tech_points = [0, 0, 0]

        tech_rows = tech_point_table.find_all('tr')
        tech_rows.pop(0)
        for index, tech_cell in enumerate(tech_rows):
            tech_val = tech_cell.find_all('td')
            if tech_val[0].text.strip() == "No stat bonuses nor tech points provided":
                break
            tech_points[index] = tech_val[1].text.strip()
            
        tech_point_collection = tech_points[0]
        tech_point_mlb = tech_points[1]
        tech_point_120 = tech_points[2]
        
        value_rows = value_table.find_all('td')

        if "Cannot" in value_rows[0].text.strip(): # Set the values to 0 for PR and META ships which cannot be retired
            enhacement_value = 0
            scrap_value = 0
        else:
            enhacement_value = value_rows[0].text.strip().split()
            enhacement_value = [int(i) for i in enhacement_value]
            scrap_value_numbers = value_rows[1].text.strip().split()
            scrap_value_numbers = [int(i) for i in scrap_value_numbers]
            scrap_items = value_rows[1].find_all('img')
            scrap_value = {}
            for index, item in enumerate(scrap_items):
                scrap_value[item.attrs['alt']] = scrap_value_numbers[index]
        
        column = []
        column.extend(ship[0:5])
        column.extend([full_name, construction_time, ship_class, health, fire_power, torpedo, aviation, anti_air, reload, evasion, speed, accuracy, luck, asw, oil_consumption, armour])
        column.extend([gear_efficiency, gear_equippable, tech_point_collection, tech_point_mlb, tech_point_120, enhacement_value, scrap_value])
        rows.append(column)
        print("Done!")
        
    create_csv(fields, rows, 'Azur Lane Data/', 'AzurLaneShips.csv')
        

get_basic_ship_info()