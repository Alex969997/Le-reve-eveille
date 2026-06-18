import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto("http://localhost:8503")
        await page.wait_for_timeout(3000)
        
        async def dump_and_click(pattern):
            buttons = page.locator("button")
            count = await buttons.count()
            print(f"\n--- SEARCHING FOR: {pattern} ---")
            found_btn = None
            for i in range(count):
                btn = buttons.nth(i)
                txt = await btn.inner_text()
                print(f"Button {i}: '{txt}'")
                if pattern in txt:
                    found_btn = btn
            if found_btn:
                await found_btn.click()
                await page.wait_for_timeout(2000)
                return True
            return False

        await dump_and_click("Franchir le portail")
        await dump_and_click("Plonger dans le miroir")
        await dump_and_click("Explorer le jardin")
        await dump_and_click("Suivre le papillon")
        
        # Dump at the wishing well
        print("\n=== DUMPING AT WISHING WELL ===")
        buttons = page.locator("button")
        count = await buttons.count()
        for i in range(count):
            btn = buttons.nth(i)
            txt = await btn.inner_text()
            print(f"Button {i}: '{txt}'")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
