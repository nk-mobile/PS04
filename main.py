from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# Настройка Firefox WebDriver
firefox_options = Options()
firefox_options.headless = False  # Установите True, если хотите запустить браузер в фоновом режиме
geckodriver_path = "/snap/bin/geckodriver"
service = Service(executable_path=geckodriver_path)  # Укажите путь к geckodriver
driver = webdriver.Firefox(service=service, options=firefox_options)

# Функция для вывода параграфов статьи
def print_paragraphs():
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i + 1}:")
        print(paragraph.text)
        user_input = input("Нажмите Enter для следующего параграфа или 1 для выхода: ")
        if user_input.lower() == '1':
            break

# Функция для выбора связанной страницы
def choose_linked_page():
    links = driver.find_elements(By.XPATH, "//a[@href]")
    valid_links = [link for link in links if link.get_attribute("href").startswith("https://ru.wikipedia.org/wiki/")]
    if not valid_links:
        print("Связанные страницы не найдены.")
        return

    print("Доступные связанные страницы:")
    for i, link in enumerate(valid_links[:10]):  # Показываем только первые 10 ссылок
        print(f"{i + 1}. {link.text}")

    choice = input("Выберите номер страницы для перехода: ")
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(valid_links):
            valid_links[choice_index].click()
            time.sleep(2)  # Ждём загрузки страницы
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Пожалуйста, введите число.")

# Основная программа
try:
    # 1. Ввод первоначального запроса пользователя
    query = input("Введите запрос для поиска на Wikipedia: ")
    driver.get("https://ru.wikipedia.org/wiki/")
    search_box = driver.find_element(By.ID, "searchInput")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Ждём загрузки страницы

    while True:
        # 2. Предлагаем пользователю три варианта действий
        print("\nВыберите действие:")
        print("a) Вывести последовательно параграфы текущей статьи")
        print("b) Выбрать одну из связанных страниц и перейти на неё")
        print("c) Выйти из программы")

        action = input("Введите ваш выбор (a/b/c): ").lower()

        if action == 'a':
            print_paragraphs()
        elif action == 'b':
            choose_linked_page()
        elif action == 'c':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

finally:
    # Закрытие браузера
    driver.quit()
