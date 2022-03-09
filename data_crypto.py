"""Модуль получения информации с binance"""
import json
import asyncio
from fake_useragent import UserAgent
import httpx


async def data_crypto(crypto_name: str ):
    global bids_list; global asks_list
    bids_list = []
    asks_list = [] 
    
    
    async def get_headers():
        """Функция, возвращающая headers для request-запроса"""
        ua = UserAgent()
        headers = {
        "User-Agent": ua.chrome,
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        return headers 

    
    async def get_url(crypto_name: str):
        """Функция автоматического определения нужного URL по каждой отдельно взятой монете"""
        if crypto_name != "RUB":
            urls = f"https://www.binance.com/api/v1/depth?symbol={crypto_name}USDT&limit=100000"
        else: 
            urls = f"https://www.binance.com/api/v1/depth?symbol=USDTRUB&limit=100000"
        return urls


    async def get_request(url, headers):
        """Посылаем запросы"""
        async with httpx.AsyncClient() as client:
            r = await client.get(url=url, headers=headers)
            return r


    async def get_txt_files(r):
        """Создаем txt файл с полученным json данными"""
        with open("index.txt", "w") as file:
            file.write(r.text)
        file_op = open("index.txt")
        data = file_op.read()
        data = json.loads(data)
        return data


    async def get_bids(data,crpt):
        """Биды"""
        bids = data["bids"]
        list_bids_volume = []
        list_bids_price = []
        for bid in bids:
            list_bids_price.append(float(bid[0]))
            list_bids_volume.append(float(bid[1]))
        result_dict_bids = dict(zip(list_bids_price,list_bids_volume))
        result_dict_bids = sorted(sorted(result_dict_bids.items(), key=lambda x: x[0]), key = lambda x:x[1], reverse=True)
        count = 0
        """Инициализация списка бидов"""
        for res in result_dict_bids:
            count += 1
            bids_list.append(res)
            if count == number_of_orders:
                break
        bids_list.append("Покупки") 
        return bids_list

    
    async def get_asks(data,crpt):
        """Аски"""
        asks = data["asks"]
        list_asks_volume = []
        list_asks_price = []
        for ask in asks:
            list_asks_price.append(float(ask[0]))
            list_asks_volume.append(float(ask[1]))
        result_dict_asks = dict(zip(list_asks_price,list_asks_volume))
        result_dict_asks = sorted(sorted(result_dict_asks.items(), key=lambda x: x[0]), key = lambda x:x[1], reverse=True)
        count = 0
        """Инициализация списка асков"""
        for res in result_dict_asks:
            count += 1
            asks_list.append(res)
            if count == number_of_orders:
                break
        asks_list.append("Продажи")
        return asks_list


    async def gather_data(crpt):
        global number_of_orders; global asks; global bids
        number_of_orders = 5
        headers = await get_headers()
        url = await get_url(crpt)
        r = await get_request(url,headers)
        data = await get_txt_files(r)
        bids = await get_bids(data,crpt)
        asks = await get_asks(data,crpt)
        return asks, bids
    
    
    async def main(crypto_name):
        """Создаем очередь задач"""
        queue = asyncio.Queue()
        crypto_list = [crypto_name]
        tasks = []
        for crpt in crypto_list:
            task = asyncio.create_task(gather_data(crpt))
            tasks.append(task)
        await queue.join()
        await asyncio.gather(*tasks, return_exceptions=True)
      
    
    await main(crypto_name=crypto_name)
    return list([bids] + [asks])
    
    
    
