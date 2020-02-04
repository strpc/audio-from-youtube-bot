# -*- coding: utf-8 -*-
'''
Getting a random proxy using the ProxyBroker module.
https://github.com/constverum/ProxyBroker/
'''

import asyncio
from proxybroker import Broker

from random import choice


async def show(proxies):
    proxy_list = []
    while True:
        proxy = await proxies.get()
        if proxy is None:
            break
        proxy_list.append(str(proxy.schemes[-1]).lower() +
                          '://' + str(proxy.host) + ':' + str(proxy.port))
    return proxy_list


def get_proxy():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=15),
        show(proxies))
    loop = asyncio.get_event_loop()
    proxy = loop.run_until_complete(tasks)
    return choice(proxy[-1])


if __name__ == '__main__':
    pass