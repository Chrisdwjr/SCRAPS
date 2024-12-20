import os
import re
import csv
import requests
from bs4 import BeautifulSoup
import time

# This program will scrape a website

def center_text(text): 
    # This function will center the text in the terminal
    try:
        terminal_size = os.get_terminal_size().columns
        padding = (terminal_size - len(text)) // 2
        print(' ' * padding + text)
    except OSError:
        print(text)
    

def display_data(data):
    # This function will display the scraped data. When the user selects this option, the program will display the data that was scraped from the website.
    if data:
        print('\nData found:')
        for key, values in data.items():
            print(f"{key}:")
            for value in values:
                print(f'  {value}')


    else:
        print('No data found.')



def web_scrape():
    # This function will scrape the website and return the data. When the user selects this option, the program will prompt the user to enter a URL. The program will then scrape the website and return the data.
    url = input('Enter the URL: ')
    headers = {'User-Agent': 'Mozilla/5.0'}
    if not re.match(r'http[s]?://', url):
        print("Invalid URL. Please enter a valid URL.")
        return None
    

    try:
        response = requests.get(url, headers=headers, timeout=10) 
        response.raise_for_status()
        print(f'{response.status_code}')
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"\nData Successfully Scraped! from {url}\n")
        time.sleep(2) 
        return soup.prettify()
    except requests.exceptions.RequestException as i: 
        print(f"Error Found!: {i}")
        return None
    
def regex(data): 
    # this function will search for sensitive data in the scraped data
    patterns = {
        "SSN": re.compile(r"\d{3}-\d{2}-\d{4}"), 
        "Phone Number": re.compile(r"\d{3}-\d{3}-\d{4}"),
        "Email": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
        "Credit Card": re.compile(r"\d{4}-\d{4}-\d{4}-\d{4}"),
        "Birthdate": re.compile(r"\d{2}/\d{2}/\d{4}"),
    }
    found = {}
    for key, pattern in patterns.items():
        matches = set(pattern.findall(data))
        if matches:
            found[key] = list(matches)

    if not found:
        print("No sensitive data found.")
        return {}

    return found
    



def export_to_csv(data):
    # This function will export the scraped data to a CSV file.
    if data:
        with open('scraped_data.csv', 'w', newline='') as csvfile: 
            writer = csv.writer(csvfile)
            for key, values in data.items():
                writer.writerow([key] + values)
        print("Data successfully saved to scraped_data.csv") 
    else:
        print("No data to export.")


def main_menu():
    # This function will display the main menu and handle user input.
    found_data = None

    center_text("Scraps: Sensitive Content Retrieval and Analysis for Python Security")
    center_text("Chris D Wise Jr")
    center_text("S01095843@acad.tri-c.edu")
    center_text("Cuyahoga Community College")

    while True:
        
        if not found_data:
            print('1. Scrape website')
            print('2. Exit')
        else:
            print('1. Display scraped data')
            print('2. Export data to a CSV file')
            print('3. Exit')

        choice = input('Enter your choice: ')

        if choice == '1' and not found_data:
            data = web_scrape()
            if data:
                found_data = regex(data)
        elif choice == '1' and found_data:
            display_data(found_data)
        elif choice == '2' and found_data:
            export_to_csv(found_data)
        elif choice == '2' and not found_data or choice == '3' and found_data:
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Please try again.')

if __name__ == '__main__':
    main_menu()

    
    
    
