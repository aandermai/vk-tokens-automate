import re

from selenium import webdriver
from selenium.webdriver.common.by import By

from vk.app import check_vk_app, create_vk_app
from vk.oauth import generate_pkce, get_auth_url, get_tokens, parse_authorization_url

APP_NAME = "VK Video Views"
DOMAIN_NAME = "vk.com"
REDIRECT_URI = "https://oauth.vk.com/blank.html"
TOKENS_FILE = "tokens.json"
 
driver = webdriver.Chrome()

# Авторизация в профиле ВК
driver.get("https://id.vk.com/about/business/go")
input("Авторизуйся в профиле ВК и нажми кнопку разрешения, а затем нажми здесь Enter...")

vk_app_exist = check_vk_app(driver, APP_NAME)

if vk_app_exist:
    app_id_div = driver.find_element(
        By.CSS_SELECTOR,
        "div[class^='styles_id']"
    )

    client_id = re.search(r"\d+", app_id_div.text).group()
else:
    create_vk_app(driver, APP_NAME, DOMAIN_NAME, REDIRECT_URI)

    app_id_input = driver.find_element(
        By.CSS_SELECTOR,
        'input[name="id"]'
    )

    client_id = app_id_input.get_attribute("value")

code_verifier, code_challenge = generate_pkce()
auth_url = get_auth_url(client_id, REDIRECT_URI, code_challenge)

driver.get(auth_url)
url = driver.current_url

authorization_code, device_id = parse_authorization_url(url)

get_tokens(TOKENS_FILE, client_id, authorization_code, code_verifier, device_id, REDIRECT_URI)