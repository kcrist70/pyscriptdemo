import asyncio
import re
import aiohttp
import aiomysql
from pyquery import PyQuery

start_url = 'http://www.jobbole.com/'


stopping = False
waiting_urls = []
seen_urls = set()
sem = asyncio.Semaphore(1)

async def fetch(url,session):
    async with sem:
        await asyncio.sleep(1)
        try:
            headers = {"Cookie":"Hm_lvt_42a9b1b1d382d464c04bb82b4916af4d=1581668505; security_session_verify=712d12d780df1ff2c077fafa3137644b; security_session_mid_verify=243f0bdca763b3c9a02fa0a603a7e756; Hm_lpvt_42a9b1b1d382d464c04bb82b4916af4d=1581676108",
}
            async with session.get(url,headers=headers) as resp:
                print('url status: {}'.format(resp.status))
                if resp.status in [200,201]:
                    data = await resp.text()
                    print(data)
                    return data
        except Exception as e:
            print(e)


async def init_urls(url,session):
    html = await fetch(url, session)
    seen_urls.add(url)
    extract_urls(html)


async def article_handler(url,session, pool):
    html = await fetch(url,session)
    seen_urls.add(url)
    extract_urls(html)
    pq = PyQuery(html)
    title = pq('title').text()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            insert_sql = 'insert into article_test(title) values("{}")'.format(title)
            await cur.execute(insert_sql)


def extract_urls(html):
    urls = []
    pq = PyQuery(html)
    for link in pq.items("a"):
        url = link.attr("href")
        if url and url.startswith('http') and url not in seen_urls:
            urls.append(url)
            waiting_urls.append(url)

async def consumer(pool):
    async with aiohttp.ClientSession() as session:
        while not stopping:
            if len(waiting_urls) == 0:
                await asyncio.sleep(0.5)
                continue
            url = waiting_urls.pop()
            print('start get url: {}'.format(url))
            if re.match('http://.*?jobbole.com/\d+/',url):
                if url not in seen_urls:
                    asyncio.ensure_future(article_handler(url,session,pool))
                    await asyncio.sleep(30)
            # else:
            #     if url not in seen_urls:
            #         asyncio.ensure_future(init_urls(url, session))


async def main(loop):
    # 等待mysql连接建立好
    pool = await aiomysql.create_pool(host='localhost',port=3306,user='root',
                                      password='',db='aiomysql_test',loop=loop,
                                      charset='utf8',autocommit=True)
    async with aiohttp.ClientSession() as session:
        html = await fetch(start_url, session)
        seen_urls.add(start_url)
        extract_urls(html)
    asyncio.ensure_future(consumer(pool))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main(loop))
    loop.run_forever()
