import json
from playwright.async_api import async_playwright, Playwright
import asyncio
import re

class Coockies:
    def __init__(self, user_id: int, coockies_user: str=None) -> None:
        self.err = True
        self.user_id = user_id
        self.coockies_user = coockies_user
       
    def write_coockies(self):
        try:
            if self.coockies_user is None:
                self.err = False
                return
            temp = {}
            for line in self.coockies_user.split(';'):
                line = line.strip()
                temp = line.split('=')
                temp[temp[0]] = temp[1]
            
            # playwright_cookies = [
            #     {
            #         "name": key,
            #         "value": value,
            #         "domain": "poshmark.com",  # Домен для poshmark.com
            #         "path": "/",
            #         "httpOnly": False,
            #         "secure": True,  # HTTPS
            #     }
            #     for key, value in temp.items()
            # ]

            with open(f'coockies-users\\{self.user_id}_coockies.json', 'w+') as file:
                json.dump(temp, file, indent=4)

        except Exception:
            self.err = False

    def read_coockies(self):
        try:
            with open(f'coockies-users\\{self.user_id}_coockies.json', 'r') as file:
                self.data_coockie: dict = json.loads(file.read())
            return self.data_coockie
        except Exception:
            return None

class NewAccount:
    __link = 'https://poshmark.com/login'

    def __init__(self, user_id: int, login: str=None, password: str=None) -> None:
        self.__login = login
        self.__paswword = password
        self.__user_id = user_id

    async def write_cookie_acc(self, port: str):
        if self.__login and self.__paswword:
            async with async_playwright() as pw:
                chromium = pw.chromium
                browser = await chromium.launch(headless=False)
                context = await browser.new_context(proxy={"server": f"http://127.0.0.1:{port}"})
                page = await context.new_page()
                await page.goto(self.__link, timeout=40000)
                await page.get_by_placeholder(text='Username or Email').fill(self.__login)
                await page.get_by_placeholder(text='Password').fill(self.__paswword)
                await asyncio.sleep(3)
                await page.get_by_role('button', name=re.compile("Login", re.IGNORECASE)).click()
                await asyncio.sleep(60)
                cookies = await context.cookies()
                await browser.close()
        
            with open(f'coockies-users\\{self.__user_id}_coockies.json', 'w+') as file:
                json.dump(cookies, file, indent=4)
        else:
            return None

    def get_cookie(self):
        try:
            with open(f'coockies-users\\{self.__user_id}_coockies.json', 'r') as file:
                result: dict = json.loads(file.read())
            return result
        except Exception:
            return None

async def main():
    new = NewAccount(1482790150, '124annalise@gmail.com', 'Vanilla124!')
    task1 = asyncio.create_task(new.write_cookie_acc(60000))
    
    await task1
    

if __name__ == '__main__':
    asyncio.run(main())
    