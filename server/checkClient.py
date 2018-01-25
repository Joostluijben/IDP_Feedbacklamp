import queue
import threading
import requests
from bs4 import BeautifulSoup
import datetime
import time

def checkClient(q):
    while True:
        page = requests.get('http://192.168.1.25:8080/')
        soup = BeautifulSoup(page.text, 'html.parser')
        value = soup.find('div', class_='volumeValue').text.strip()
        now = datetime.datetime.now()
        q.put([value,now])       
        time.sleep(5)

q = queue.Queue()
t1 = threading.Thread(target=checkClient, name=checkClient, args=(q,))
t1.start()
