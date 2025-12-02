from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import requests
import time



def scrape_data():

    url = 'https://fbref.com/en/comps/9/2025-2026/schedule/2025-2026-Premier-League-Scores-and-Fixtures'

    # Selenium setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    print("Obtaining the data...")
    time.sleep(5)

    html_content = driver.page_source
    driver.quit()
    print("Loading the data...")

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', id='sched_2025-2026_9_1')

    if not table:
        print("Could not find the specified table.")
        return None

    df = pd.read_html(StringIO(str(table)))[0]

    # Clean DataFrame
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]

    df = df.dropna(subset=['Wk'])
    df = df[df['Wk'] != 'Wk']
    df = df.drop(['Match Report', 'Notes'], axis=1, errors='ignore')
    return df