import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("http://localhost:8504")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="/Users/alexandre/.gemini/antigravity-ide/brain/6637ecac-6492-48f1-8b62-3f9e30c2903f/simple_test.png")
        
        # Print frames to verify
        frames = page.frames
        print(f"Total frames: {len(frames)}")
        for idx, f in enumerate(frames):
            print(f"Frame {idx}: url={f.url}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
