import requests
from pyquery import PyQuery as pq
from dataclasses import dataclass
import time
import lxml


@dataclass
class TaskRequest:
    account_id: str
    state: str


@dataclass
class Task:
    username: str
    connect_form_id: str
    account_id_action: str


class Dizu:
    def __init__(self):
        cookies_str = '_ga=GA1.3.1038365009.1617191872; _fbp=fb.2.1618516156105.432591116; _gid=GA1.3.1110728582.1623285531; crsftoken=74a201014e54466871f069ce8302278d:cf416731fb331c30b6f0e2818603c923; _gat_gtag_UA_160075623_1=1; __cf_bm=14f6b012d5d251b934a54ba3da43f2385e1b9d21-1623360209-1800-ASPkGezHIq2xFxtu0+py9fprylC9OxcfUO7ERhXfmvtAY3zoLZz7EDqD6xtk3aZYPSXprwnhRIgnDFSI13s8yrQqUdrtJPliueEAbUkfv/Mvis3nOxFvCPYnSk7X3+C+gA=='
        self.cookies = {}

        for cookie in cookies_str.split(';'):
            index = cookie.index('=')
            key = cookie[0:index]
            value = cookie[index+1:]
            self.cookies[key] = value

        self.headers = {
            'Accept': '* / *',
            'Host': 'dizu.com.br',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }

    def get_task(self, task_request):
        payload = {
            'conta_id': task_request.account_id,
            'twitter_id': 'Twitter',
            'tiktok_id': 'TikTok',
            'tarefa10': 0,
            'curtida05': 0,
            'acoesmg': 0,
            'estado': task_request.state,
        }
        url = f'https://dizu.com.br/painel/listar_pedido/'

        d = None
        while not d:
            r = requests.get(url, params=payload, cookies=self.cookies, headers=self.headers)
            try:
                d = pq(r.text)
                break
            except lxml.etree.ParserError as err:
                print(err)
                print(r.text) 
                time.sleep(5)

        href = d('a#conectar_step_4').attr('href')

        if '/p' in href:
            raise ValueError(f'Invalid Task: {href}')

        username = href.split('/')[-1]
        connect_form_id = d('#conectar_form_id').attr('value')
        account_id_action = d('#conta_id_acao').attr('value')

        task_response = Task(
            username=username,
            connect_form_id=connect_form_id,
            account_id_action=account_id_action
        )
        print(task_response)

        return task_response

    def submit_task(self, task):
        payload = {
            'tarefa_token': None,
            'tarefa_id': task.connect_form_id,
            'conta_id': task.account_id_action,
            'realizado': 1,
        }
        url = f'https://dizu.com.br/painel/confirmar_pedido/'

        r = requests.post(url, data=payload, cookies=self.cookies, headers=self.headers)
        print(r.text)
