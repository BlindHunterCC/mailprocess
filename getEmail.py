import json
import asyncio
from fake_useragent import UserAgent
from curl_cffi.requests import AsyncSession
from asyncio.windows_events import WindowsSelectorEventLoopPolicy

import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, colorize=True, format="<g>{time:HH:mm:ss:SSS}</g> | <c>{level}</c> | <level>{message}</level>")

class TempEmail:
    def __init__(self) -> None:
        headers = {
            "Referer": "https://temp-mail.org/",
            "Origin": "https://temp-mail.org",
            "Content-Type": "application/json",
            "User-Agent": UserAgent().chrome
        }

        self.http = AsyncSession(timeout=120,headers= headers, impersonate="chrome120")

    async def getMailAddress(self):
        try:
            res = await self.http.post("https://web2.temp-mail.org/mailbox")
            if  res.status_code == 200:
                self.http.headers.update({"authorization":"Bearer "+ res.json()['token']})
                return res.json()['mailbox']
            
        except Exception as e:
            logger.error(f"获取邮箱地址失败:{e}")

    async def getMailContent(self):
        try:
            res = await self.http.get("https://web2.temp-mail.org/messages")
            if  res.status_code == 200:
                return res.json()['messages']
            
        except Exception as e:
            logger.error(f"获取邮箱内容失败:{e}")

async def reciveMailMessage():
    te = TempEmail()
    mailaddress = await te.getMailAddress()
    await te.getMailContent()
    pass

async def taskExe():
    taskArr = []
    taskArr.append(reciveMailMessage())
    try:
        await asyncio.gather(*taskArr)
    except:
        logger.error("任务启动失败!")

if __name__ == '__main__':
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    asyncio.run(taskExe())