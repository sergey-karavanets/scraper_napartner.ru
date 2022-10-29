import requests
from bs4 import BeautifulSoup
import lxml
import json

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    # req = requests.get(url, headers)
    #
    # with open('project.html', 'w', encoding='utf-8') as file:
    #     file.write(req.text)

    with open('project.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    startups = soup.find_all(class_='main_startup_view')

    project_urls = []
    for startup in startups:
        project_url = 'https://www.napartner.ru' + startup.find('div', class_='name').find('a').get('href')
        project_urls.append(project_url)

    projects_data_list = []
    for project_url in project_urls:
        req = requests.get(project_url, headers)
        project_name = (project_url.split('/')[-1])

        with open(f'data/{project_name}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)

        with open(f'data/{project_name}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        project_data = soup.find('div', class_='startup_page')

        try:
            project_logo = 'https://www.napartner.ru' + project_data.find('div', class_='left').find('img').get('src')
        except Exception:
            project_logo = 'No project logo'

        try:
            project_name = project_data.find('div', class_='center').find('div', class_='name').find('h1').text
        except Exception:
            project_name = 'No project name'

        try:
            project_description = '\n'.join(filter(lambda x: x not in ('Твитнуть'), map(lambda x: x.strip(), project_data.find('div', class_='bottom').find('div', class_='text').get_text('|').split('|'))))
        except Exception:
            project_description = 'No project description'

        projects_data_list.append(
            {
                'Имя проекта': project_name,
                'Ссылка на проект': project_url,
                'URL логотипа проекта': project_logo,
                'Описание проекта': project_description
            }
        )

    with open('data/project_data.json', 'a', encoding='utf-8') as file:
        json.dump(projects_data_list, file, indent=4, ensure_ascii=False)

get_data('https://www.napartner.ru/')