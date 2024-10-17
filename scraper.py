import requests
from bs4 import BeautifulSoup
import sqlite3

def create_db():
    conn = sqlite3.connect('countries.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        capital TEXT,
        population INTEGER,
        area REAL
    )
    ''')
    conn.commit()
    conn.close()

def extract_data():
    url = 'https://scrapethissite.com/pages/simple/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    countries = soup.find_all('div', class_='col-md-4 country')
    
    data = []
    for country in countries:
        name = country.find('h3', class_='country-name').text.strip()
        capital = country.find('span', class_='country-capital').text.strip()
        population = int(country.find('span', class_='country-population').text.strip().replace(',', ''))
        area = float(country.find('span', class_='country-area').text.strip().replace(',', ''))

        data.append((name, capital, population, area))

    return data

def store_data(data):
    conn = sqlite3.connect('countries.db')
    cursor = conn.cursor()
    
    for country in data:
        cursor.execute('''
        INSERT INTO countries (name, capital, population, area)
        VALUES (?, ?, ?, ?)
        ''', country)
    
    conn.commit()
    conn.close()

def main():
    create_db()
    data = extract_data()
    store_data(data)
    print("Data stored successfully.")

if __name__ == "__main__":
    main()
