import pandas as pd
from bs4 import BeautifulSoup as BS
from functools import reduce

import time 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import random

def render_page(url):
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-gpu')
        driver=webdriver.Firefox(options=firefox_options)
        driver.get(url)
        time.sleep(3)
        r = driver.page_source
        driver.quit()
        return r

def hourly_scraper(page,dates):
        output = pd.DataFrame()
        for d in dates:
                url = str(str(page) + str(d))
                r = render_page(url)
                soup = BS(r, "html.parser",)
                container = soup.find('lib-city-history-observation')
                check = container.find('tbody')

                data = []
                data_hour = []
                for i in check.find_all('span', class_='ng-star-inserted'):
                        trial = i.get_text()
                        data_hour.append(trial)

        for i in check.find_all('span', class_='wu-value wu-value-to'):
                trial = i.get_text()
                data.append(trial)

        numbers = pd.DataFrame([data[i:i+7] for i in range(0, len(data), 7)],columns=["Temperature","Dew Point","Humidity","Wind Speed","Wind Gust","Pressure","Precipitation"])
        hour = pd.DataFrame(data_hour[0::17],columns=["Time"])
        wind = pd.DataFrame(data_hour[7::17],columns=["Wind"])
        condition = pd.DataFrame(data_hour[16::17],columns=["Condition"])

        dfs = [hour,numbers,wind,condition]

        df_final = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), dfs)
        df_final['Date'] = str(d)

        output = output.append(df_final)
        print(str(str(d) + ' finished!'))
        return output


page = "https://www.wunderground.com/history/daily/us/ga/atlanta/KATL/date/"
dates = ["2018-1-1"]

hourly = hourly_scraper(page,dates)
hourly.to_csv('weather_data_sample.csv')
hourly.to_csv('/home/devesh/Desktop/pywscb/weather_data_sample.csv')
                                          


