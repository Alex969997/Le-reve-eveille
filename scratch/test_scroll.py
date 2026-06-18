import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: [{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))
        
        brain_dir = "/Users/alexandre/.gemini/antigravity-ide/brain/6637ecac-6492-48f1-8b62-3f9e30c2903f"
        os.makedirs(brain_dir, exist_ok=True)
        
        print("Navigating to http://localhost:8503...")
        await page.goto("http://localhost:8503")
        await page.wait_for_timeout(2000)
        
        async def click_button_by_text(pattern):
            print(f"Looking for button matching: {pattern}")
            buttons = page.locator("button")
            count = await buttons.count()
            for i in range(count):
                btn = buttons.nth(i)
                text = await btn.inner_text()
                if pattern in text:
                    print(f"Found and clicking button: {text}")
                    await btn.click()
                    await page.wait_for_timeout(2000)
                    return True
            print(f"ERROR: Button matching '{pattern}' not found!")
            return False

        # Go to final boss and pick up Parchemin Lunaire
        await click_button_by_text("S'approcher de la clé")
        await click_button_by_text("Lui confier un secret")
        await click_button_by_text("Franchir le portail")
        await click_button_by_text("Examiner la porte à la serrure")
        await click_button_by_text("Insérer la Clé des Murmures")
        await click_button_by_text("Consulter le parchemin lunaire")
        await click_button_by_text("Rejoindre le couloir de la Tour")
        await click_button_by_text("Affronter l'Horloger du Temps")
        
        # Verify scroll is in inventory
        inventory_items = page.locator("aside strong, aside b, aside span")
        items_count = await inventory_items.count()
        items = []
        for i in range(items_count):
            items.append(await inventory_items.nth(i).inner_text())
        print(f"Inventory items: {items}")
        
        # Check if Parchemin Lunaire button is visible
        print("Using Parchemin Lunaire...")
        await page.screenshot(path=f"{brain_dir}/v_scroll_before.png")
        await click_button_by_text("Parchemin Lunaire")
        
        # Verify scroll is no longer in inventory and button is gone
        await page.screenshot(path=f"{brain_dir}/v_scroll_after.png")
        
        inventory_items = page.locator("aside strong, aside b, aside span")
        items_count = await inventory_items.count()
        items_after = []
        for i in range(items_count):
            items_after.append(await inventory_items.nth(i).inner_text())
        print(f"Inventory items after: {items_after}")
        
        # Check if Parchemin Lunaire button is no longer present
        buttons = page.locator("button")
        count = await buttons.count()
        button_texts = [await buttons.nth(i).inner_text() for i in range(count)]
        print(f"Available buttons after use: {button_texts}")
        
        assert "Parchemin Lunaire" not in "".join(button_texts), "Error: Scroll button still available!"
        print("Success: Parchemin Lunaire is consumed correctly!")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
