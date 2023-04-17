import streamlit as st
from numpy import random
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time

st.set_page_config(page_title="Amazon Coupon Extractor", layout="wide")

progress_text = "Operation in progress. Please wait."

st.title("Amazon Coupon Extractor")

# Generic Vars
ASIN = 'B082DK316V'
df = None

# =========================================

# Managing Session States

if "asin_lst" not in st.session_state:
    st.session_state.asin_lst = []

if "res_data" not in st.session_state:
    st.session_state.res_data = None

# =========================================

# Functions for core functionality


def conc_url(asin):
    return asin


def pram_maker(ASIN):
    return '{%s}' % (f'"asin":"{ASIN}"')


def initialize(driver):

    driver.get('https://www.amazon.com/s?k=B08RNKTFXY&ref=nb_sb_noss')

    loc = driver.find_element(By.XPATH,
                              '//*[@id="nav-global-location-popover-link"]')
    loc.click()

    try:
        loc_zip = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="GLUXZipUpdateInput"]')))
    finally:
        print("No Element")

    loc_zip.click()
    loc_zip.send_keys("10001")
    driver.find_element(By.XPATH,
                        '//*[@id="GLUXZipUpdate"]/span/input').click()
    try:
        driver.find_element(
            By.XPATH, '//*[@id="a-popover-2"]/div/div[2]/span/span').click()
        driver.find_element(
            By.XPATH, '//*[@id="a-popover-2"]/div/div[2]/span/span').click()
    except:
        print("Something Went Wrong!")
    return driver


def new_tab_url(ASIN, driver):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 'w')
    driver.get(f'https://www.amazon.com/s?k={ASIN}&ref=nb_sb_noss')


def get_coupon(page_source, ASIN):
    soup = BeautifulSoup(page_source, 'html.parser')
    span = soup.find_all('span', {'data-component-props': pram_maker(ASIN)})
    try:
        coupon_amount = span[0].find('span', {
            'class': 's-coupon-highlight-color'
        }).text.strip()
        coupon_amount = coupon_amount.split(' ', -1)
        return coupon_amount[1]
    except IndexError as e:
        print(f'{e}: Coupon Does Not Exist for ASIN: {ASIN}')
        return "Nill"


@st.cache_data
def start_extraction(asins):

    driver = webdriver.Edge()
    # Basic Setup for the Amazon.com (Change Address etc)
    initialize(driver)
    time.sleep(5)
    # List to store the ASIN base URL and coupon amount
    coupons = []
    # Open a new tab and go to the next ASIN in user ASIN file
    for asin in asins:
        new_tab_url(asin, driver)
        time.sleep(random.randint(1))
        page_source = driver.page_source
        coupon_amount = get_coupon(page_source, asin)
        coupons.append({
            "URL": f'https://www.amazon.com/s?k={asin}&ref=nb_sb_noss',
            "Coupon": coupon_amount
        })
    # Scraping Completion Prompt
    st.write(
        "Finished Scraping! You can see the coupons in the Coupons.csv file.")
    print(
        "Finished Scraping! You can see the coupons in the Coupons.csv file.")
    # Convert and Save the Scraped Data to CSV format
    res = pd.DataFrame(coupons)
    res.to_csv("Coupons.csv", index=False)
    time.sleep(6)
    # Close the Edge Browser
    driver.quit()
    return res


# =========================================

csv_file = st.file_uploader("Choose a .csv file", type='csv')

if csv_file is not None:
    df = pd.read_csv(csv_file, index_col=False)
    asin_col = df['ASIN']
    st.session_state.asin_lst = asin_col.apply(lambda x: conc_url(x)).tolist()

with st.container():
    st.markdown("----", unsafe_allow_html=True)
    col1, col2, col3 = st.columns((2, 1, 2))
    with col2:
        start_btn = st.button("Start")

    if start_btn:
        st.session_state.res_data = start_extraction(
            st.session_state.asin_lst[25:40])

    st.markdown("----", unsafe_allow_html=True)



            



with st.container():
    st.table(st.session_state.res_data)
