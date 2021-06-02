from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import urllib.robotparser

headers = {'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'}
base_url = 'https://pokemondb.net/pokedex'
robot_url = 'https://pokemondb.net/robots.txt'
pokemon = input("Which Pokémon would you like information about? Enter its name here: ")
data = []


"""
Access the Robots.txt file to determine if we have permission to scrape the site.
"""
def get_rp(robot_url):
    r = requests.get(robot_url, headers=headers)
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(r.text.split('\n'))

"""
Uses RobotFileParser to access index page to determine if we have permission to scrape the page.
If we do, we return a BeautifulSoup object with the parsed html.
"""
def get_page(url):
    r = requests.get(url, headers=headers)
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(r.text)
    if (rp.can_fetch('*', r.text)):
        html = requests.get(url)
        bs = BeautifulSoup(html.text, "html.parser")
        return bs
    else:
        return None

"""
Function to parse HTML of requested page and append attributes to a list.
"""
def get_attributes(name):
    n = get_page(base_url + "/" + name)
    name = n.select_one("h1").text
    data_table = n.find("table", class_="vitals-table")
    nat_dex_num = data_table('td')[0].text
    poke_type = data_table.find_all("a", class_=re.compile('type-icon'))
    species = data_table('td')[2].text
    height = data_table('td')[3].text
    weight = data_table('td')[4].text
    abilities = data_table('td')[5].text
    print("\nBASIC DATA\n")
    print("Pokémon Name: " + name)
    print("National Pokédex Number: " + nat_dex_num)
    if len(poke_type) > 1:
        print("Primary Type: " + poke_type[0].get_text())
        print("Secondary Type: " + poke_type[1].get_text())
    else:
        print("Type: " + poke_type[0].get_text())
    print("Species: " + species)
    print("Height: " + height)
    print("Weight: " + weight)
    print("Abilities: " + abilities)

get_attributes(pokemon)