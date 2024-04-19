import csv
import datetime
import time
import re
import sys
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver

def scrap():
    url = 'https://rejestracjapoznan.poznan.uw.gov.pl/QueueStatus'
    ua = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={ua.chrome}')
    options.add_argument("--headless")  # Ensure GUI is off
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(url)
    html = BeautifulSoup(driver.page_source, 'html.parser')
    body = str(html.body) # converts to string

    a_string = "PASZPORTY - Składanie wniosków o paszport"
    b_string = "PASZPORTY - Odbiór paszportu"

    queue_a_start_index = body.find(a_string) + len(a_string)
    queue_b_start_index = body.find(b_string)
    max_digits = 600 # this is arbitrary, but should be enough to capture all the numbers

    queue_a = body[queue_a_start_index:queue_a_start_index + max_digits] 
    queue_b = body[queue_b_start_index:queue_b_start_index + max_digits]

    pattern = r'>\s*(\d+)\s*<'
    values_a = re.findall(pattern, queue_a)
    values_b = re.findall(pattern, queue_b)

    values_a = [int(x) for x in values_a]
    values_b = [int(x) for x in values_b]

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    values_a.insert(0, timestamp)
    values_b.insert(0, timestamp)

    driver.quit()

    return values_a, values_b


def save_to_csv(filename, data):
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def main():
    timeout = 15  # in minutes
    
    if 60 % timeout != 0:
        print("Error: timeout must be a factor of 60.")
        sys.exit(1)

    while True:
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        minutes_past = current_time.minute % timeout

        if (8 <= current_hour < 16) and (minutes_past == 0):
            new_values_a, new_values_b = scrap()

            save_to_csv('numbers_a.csv', new_values_a)
            save_to_csv('numbers_b.csv', new_values_b)

        sleep_time = 60 * timeout - (minutes_past * 60 + current_time.second)
        time.sleep(sleep_time)  # wait for the next timeout mark

if __name__ == "__main__":
    main()