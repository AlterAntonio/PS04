from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # Иногда нада
import time

browser = wd.Firefox()
browser.get('https://ru.wikipedia.org/') # Главная страница
wait = 3 # Время задержки

# Собственно поиск
def find(asc):
    search_box = browser.find_element(By.ID, 'searchInput')
    search_box.send_keys(asc)
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(browser, 10).until(lambda browser: browser.title != title)
    time.sleep(wait)

# Если на запрос будут результаты поиска
def search_result():
    print()
    print(browser.title)
    print('1 - вывести список результатов (пока только первые 20);\n2 - новый поиск;\n3 - выход.')
    while True:
        user_choice = input('Ваш выбор: ')
        if user_choice == '1':
            result = []
            for element in browser.find_elements(By.TAG_NAME, 'div'):
                if element.get_attribute('class') == 'mw-search-result-heading': result.append(element)
            links = []
            names = []
            for element in result:
                links.append(element.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                names.append(element.find_element(By.TAG_NAME, 'a').get_attribute('title'))
            print()
            print('Вот что получилось:')
            while True:
                n = 1
                for name in names:
                    print(f'{n} - {name};')
                    n += 1
                print('q (й) - новый поиск.')
                user_choice = input('Ваш выбор: ')
                print()
                if user_choice in ['q', 'й']: return 1
                else:
                    try:
                        user_choice = int(user_choice) - 1
                        if 0 <= user_choice <= len(names):
                            browser.get(links[user_choice])
                            WebDriverWait(browser, 10).until(lambda browser: browser.title != title)
                            time.sleep(wait)
                            return 3
                        else:
                            print('Нет такого варианта!')
                            continue
                    except:
                        print('Неверный ввод! Введите номер статьи:')
                        continue
        elif user_choice == '2': return 1
        elif user_choice == '3': return 2
        else:
            print('Нет такого варианта!')
            continue

# Проход по параграфам
def paragraph():
    paragraphs = browser.find_elements(By.TAG_NAME, 'p')
    for paragraph in paragraphs:
        print()
        print(paragraph.text)
        print('Enter - следующий параграф; q (й) - назад к выбору.')
        user_choice = input()
        if user_choice in ['q', 'й']: break
        elif user_choice: print()
        else: continue

# Проход по статьям
def article():
    hatnotes = []
    for element in browser.find_elements(By.TAG_NAME, 'div'):
        if element.get_attribute('class') == 'hatnote navigation-not-searchable':
            for hatnote in element.find_elements(By.TAG_NAME, 'a'): hatnotes.append(hatnote)
    if len(hatnotes) == 0:
        print()
        print('Эта статья не имеет связанных статей. Попробуйте полистать параграфы.')
        return
    else:
        print('Связанные статьи:')
    n = 1
    for title in hatnotes:
        print(f'{n} - {title.get_attribute("title")}')
        n += 1
    while True:
        print('q/й - назад к выбору.')
        user_choice = input()
        if user_choice in ['q', 'й']: return
        else:
            try:
                user_choice = int(user_choice) - 1
                if user_choice in range(len(hatnotes)):
                    link = hatnotes[user_choice].get_attribute('href')
                    browser.get(link)
                    WebDriverWait(browser, 10).until(lambda browser: browser.title != title)
                    time.sleep(wait)
                    return 1
                else: print('Нет такого варианта!')
            except: print('Неверный ввод!')
            return

# Функция по статьям и параграфам
def explore():
    while True:
        print(browser.title)
        print('1 - посмотреть список связанных статей;\n2 - новый поиск;\n3 - выход;\nEnter - листать параграфы текущей '
              'статьи.')
        user_choice = input('Ваш выбор: ')
        if user_choice == '1': article()
        elif user_choice == '2': return '1'
        elif user_choice == '3': return '2'
        elif user_choice == '': paragraph()
        else:
            print('Нет такого варианта!')
            continue

# Цикл программы
condition = 0
while True:
    title = browser.title
    user_choice = ''
    if condition == 0:
        print('1 - новый поиск;\n2 - выход;\n3 - поменять тайминг.')
        user_choice = input('Ваш выбор: ')
        print()
    elif condition == 1:
        user_choice = '1'
        condition = 0
    elif condition == 2:
        user_choice = '2'
        condition = 0
    elif condition == 3:
        explore()
        condition = 0
    if user_choice == '1':
        find(input('Что найти на Википедии: '))
        if 'Результаты для' in browser.title:
            condition = search_result()
            if condition == 1: continue
        else:
            condition = explore()
    elif user_choice == '2':
        print('Ладно, пока...')
        break
    elif user_choice == '3':
        print('Это время ожидания для загрузки страницы в секундах. Если что-то идёт не так, то можно увеличить. А '
              'если кажется '
              'долго, то уменьшить. В целях упрощения надо вводить целое цисло.')
        while True:
            user_choice = input(f'Введите новое время ожидания (сейчас {wait} сек.): ')
            try:
                wait = int(user_choice)
                print(f'Теперь время ожидания {wait} сек.')
                break
            except: print('Введите целое число!')

    else:
        print('Нет такого варианта!')
        continue

browser.quit()