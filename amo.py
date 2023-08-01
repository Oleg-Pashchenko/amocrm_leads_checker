import os
import time
import dotenv
import requests
from amocrm.v2 import tokens, Lead
import bs4

dotenv.load_dotenv()
def get_token():
    mail = 'business-robots@yandex.ru'
    host = 'https://chatgpt.amocrm.ru/'
    password = "Xh1wdBlk"
    try:
        session = requests.Session()
        response = session.get(host)
        session_id = response.cookies.get('session_id')
        csrf_token = response.cookies.get('csrf_token')
        headers = {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': f'session_id={session_id}; '
                      f'csrf_token={csrf_token};'
                      f'last_login={mail}',
            'Host': host.replace('https://', '').replace('/', ''),
            'Origin': host,
            'Referer': host,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        payload = {
            'csrf_token': csrf_token,
            'password': password,
            'temporary_auth': "N",
            'username': mail}

        response = session.post(f'{host}oauth2/authorize', headers=headers, data=payload)
        access_token = response.cookies.get('access_token')
        refresh_token = response.cookies.get('refresh_token')
        headers['access_token'], headers['refresh_token'] = access_token, refresh_token
        payload = {'request[chats][session][action]': 'create'}
        headers['Host'] = 'chatgpt.amocrm.ru'
        response = session.post(f'{host}ajax/v1/chats/session', headers=headers, data=payload)
        token = response.json()['response']['chats']['session']['access_token']
    except Exception as e:
        print(e)
        time.sleep(3)
        return get_token()
    print('Amo Token:', token)
    return token, session


def create_task():
    pass


def turn_off_checker():
    pass


def get_chat_history(hash):

    token, session = get_token()
    headers = {'X-Auth-Token': token}
    url = f'https://amojo.amocrm.ru/messages/{os.getenv("ACCOUNT_CHAT_ID")}/merge?stand=v16&offset=0&' \
                  f'limit=100&chat_id[]={hash}&get_tags=true&lang=ru'
    chat_history = requests.get(url, headers=headers).json()
    return chat_history


def get_info_by_link(link):
    print(link)
    token, session = get_token()
    try:
        response = session.get(link)
        hash_id = response.text.split('data-chat-id="')[1].split('"')[0]
        soup = bs4.BeautifulSoup(response.text, features='html.parser')
        pipeline_id = soup.find('input', {'class': 'pipeline-select__pipeline-selected'}).get('value')
        stage = soup.find('div', {'class': 'pipeline-select-view__status'}).find('span').text
        elements = soup.find_all('div', {'class': 'linked-form__field-checkbox'})
        checked = False
        for element in elements:
            if element.find('div', {'class': 'linked-form__field__label'}).get('title') == 'Check':
                if 'checked="checked"' in str(element.find('div', {'class': 'linked-form__field__value'}).find('input')):
                    checked = True
                    break
        return hash_id, pipeline_id, stage, checked
    except:
        return None, None, None, None


def get_tasks(needed_pipeline):
    tokens.default_token_manager(
        client_id="1145fbe2-4fd8-48ed-a874-1f58e5f14d69",
        client_secret="RELohXjzWeD9bDePioS5476sEPgzncXS6dJt1FTRqUFA1IQDW92DqQrV66jz7dHZ",
        subdomain="chatgpt",
        redirect_url="https://ya.ru",
        storage=tokens.FileTokensStorage()
    )
    leads = Lead.objects.all()
    for lead in leads:
        deal_id, contact_id = lead.id, 0
        for contact in lead.contacts: contact_id = contact.id
        deal_id = 11308715
        hash_id, pipeline_id, stage, checked = get_info_by_link(f'https://chatgpt.amocrm.ru/leads/detail/{deal_id}')
        if hash_id is None or int(pipeline_id) != int(needed_pipeline) or not checked:
            continue
        chat_history = get_chat_history(hash_id)
