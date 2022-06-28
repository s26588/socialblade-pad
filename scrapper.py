import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome()
driver.get('https://socialblade.com/youtube/top/100')

driver.maximize_window();

time.sleep(5)

# accept privacy notice
WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.ID, 'sp_message_iframe_633228')))
driver.switch_to.frame(driver.find_element(by=By.ID, value='sp_message_iframe_633228'))
WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'button.message-component:nth-child(2)')))
privacy_notice_btn = driver.find_element(by=By.CSS_SELECTOR, value='button.message-component:nth-child(2)')
privacy_notice_btn.click()


countries = ['de', 'pl', 'ro']
links = []

# interate over countries
for country in countries:
  WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.ID, 'CountrySelectorSidebar')))
  country_select = driver.find_element(by=By.ID, value='CountrySelectorSidebar')
  country_select.click()

  time.sleep(5)

  WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="CountrySelectorSidebar"]/option[@value="{country}"]')))
  country_option = driver.find_element(by=By.XPATH, value=f'//*[@id="CountrySelectorSidebar"]/option[@value="{country}"]')
  country_option.click()

  time.sleep(5)

  WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.ID, 'sort-by-current')))
  sortby_select = driver.find_element(by=By.ID, value='sort-by-current')
  sortby_select.click()

  time.sleep(5)

  # sort by most subscribed
  WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sort-by-dropdown"]/div[@data-sort="mostsubscribed"]')))
  mostsubscribed_option = driver.find_element(by=By.XPATH, value='//*[@id="sort-by-dropdown"]/div[@data-sort="mostsubscribed"]')
  mostsubscribed_option.click()

  time.sleep(5)

  # get links
  accounts = driver.find_elements(by=By.CSS_SELECTOR, value='#sort-by ~ div a')
  accounts_links = [account.get_attribute("href") for account in accounts]
  links.extend(accounts_links)


accounts_df = pd.DataFrame({
  'name': [],
  'uploads_srt': [],
  'subs_str': [],
  'views_str': [],
  'channel_type': [],
  'earnings': [],
})

for link in links:
  try:
    time.sleep(1);

    account_dict = {}
    driver.get(link)

    # get info about user
    name_info = driver.find_element(by=By.XPATH, value='//*[@id="YouTubeUserTopInfoAvatar"]')
    account_dict['name'] = [name_info.get_attribute("alt")];

    uploads_info = driver.find_element(by=By.XPATH, value='//*[@id="YouTubeUserTopInfoBlock"]/div[2]/span[2]')
    account_dict['uploads_str'] = [uploads_info.text];

    subs_info = driver.find_element(by=By.XPATH, value='//*[@id="YouTubeUserTopInfoBlock"]/div[3]/span[2]')
    account_dict['subs_str'] = [subs_info.text];

    views_info = driver.find_element(by=By.XPATH, value='//*[@id="YouTubeUserTopInfoBlock"]/div[4]/span[2]')
    account_dict['views_str'] = [views_info.text];

    country_info = driver.find_element(by=By.XPATH, value='//*[@id="YouTubeUserTopInfoBlock"]/div[5]/span[2]')
    account_dict['country'] = [country_info.text];

    channeltype_info = driver.find_element(by=By.XPATH, value='//*[@id="YouTubeUserTopInfoBlock"]/div[6]/span[2]')
    account_dict['channel_type'] = [channeltype_info.text];

    earnings_info = driver.find_element(by=By.XPATH, value='//*[@id="socialblade-user-content"]/div[3]/div[2]/p[1]')
    account_dict['earnings'] = [earnings_info.text];

    accounts_df = pd.concat([accounts_df, pd.DataFrame(account_dict)], ignore_index=True)
    
  except:
    pass

# save to csv file
accounts_df.to_csv('accounts_dirty.csv', sep=';')

driver.quit(); 