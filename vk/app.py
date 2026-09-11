from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def create_vk_app(driver, app_name, domain_name, redirect_uri):
    # Клик по кнопке создания приложения
    add_app_button = driver.find_element(
        By.XPATH,
        "//span[normalize-space()='Добавить приложение']/ancestor::button"
    )
    add_app_button.click()

    # Задаём название приложения
    app_name_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Моё приложение"]')
        )
    )
 
    app_name_input.send_keys(app_name)

    # Выбор типа приложения
    web_switch = driver.find_element(
        By.CSS_SELECTOR,
        'input[role="switch"][value="web"]'
    )
    if web_switch.get_attribute("aria-checked") == "false":
        web_switch.find_element(By.XPATH, "./..").click()

    # Нажатие кнопки "Далее"
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[normalize-space()='Далее']]")
        )
    )
    continue_button.click()

    # Вставка базового домена приложения
    domain_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="mysite.com"]')
        )
    )
    domain_input.send_keys(domain_name)

    # Вставка Redirect URL прилоежния
    redirect_url_input = driver.find_element(
        By.CSS_SELECTOR,
        'input[placeholder="https://mysite.com"]'
    )
    redirect_url_input.send_keys(redirect_uri)

    # Нажатие кнопки "Создать приложение"
    create_app_button = driver.find_element(
        By.XPATH,
        "//button[.//span[normalize-space()='Создать приложение']]"
    )
    create_app_button.click()

    input("Введите код от ВК и нажмите Enter...")

    settings_later_button = driver.find_element(
        By.XPATH,
        "//button[.//span[normalize-space()='Настроить позже']]"
    )
    settings_later_button.click()

    close_button = driver.find_element(
        By.XPATH,
        "//button[.//span[normalize-space()='Закрыть']]"
    )
    close_button.click()
    