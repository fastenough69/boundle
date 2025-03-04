from playwright.async_api import async_playwright, BrowserContext
from selector import NewAccount
import asyncio
import re

async def new_boundle(link: str, paste: str, context: BrowserContext, user_id: int) -> bool:
    try:
        new_acc = NewAccount(user_id)
        cookie = new_acc.get_cookie()
        if cookie is not None:
            page = await context.new_page()
            await page.goto(link)
            await page.wait_for_load_state("networkidle")
            # await page.context.clear_cookies()
            # await asyncio.sleep(1)
            await page.context.add_cookies(cookie)
            # await asyncio.sleep(1)
            await page.reload(wait_until='networkidle')

            await page.wait_for_selector('.p--l--2')
            data =  await page.locator('.p--l--2').all()

            for li in data:
                if await li.inner_text() == 'Add To Bundle':
                    await li.click()
                    await page.wait_for_load_state("networkidle")
                    break
                
            
            await asyncio.sleep(2)
            await page.wait_for_selector('[placeholder="Add your comment.."]')
            await page.get_by_placeholder(text='Add your comment..').fill(paste)
            await page.wait_for_load_state("networkidle")
            await page.get_by_role('button', name=re.compile("Send", re.IGNORECASE)).click()
            await asyncio.sleep(1)

            return True
        else:
            raise 'Нет данных о cookie'
    except Exception:
        return False

async def test_playwright():

    async with async_playwright() as pw:
        chromium = pw.chromium
        browser = await chromium.launch(headless=False)
        context = await browser.new_context(proxy={"server": "http://127.0.0.1:60000"})
        
        task = asyncio.create_task(new_boundle('https://poshmark.com/listing/673f7ed6142ad4a69e7d9a88', 'Hello', context))
        task1 = asyncio.create_task(new_boundle('https://poshmark.com/listing/673f7ed6142ad4a69e7d9a88', 'Hello', context))
        res = await asyncio.gather(task, task1)
        print(*res, end='\n')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_playwright())
