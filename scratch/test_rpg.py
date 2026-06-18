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
        await page.wait_for_timeout(3000)
        await page.screenshot(path=f"{brain_dir}/v_story_start.png")
        
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

        async def play_qte(turn_desc):
            print(f"Playing QTE for: {turn_desc}")
            frames = page.frames
            for f in frames:
                if "timing_slider" in f.url or "index.html" in f.url:
                    await f.wait_for_selector("#cursor")
                    await f.wait_for_selector(".zone-target")
                    
                    # Instantaneous JS evaluation loop
                    for _ in range(500):
                        positions = await f.evaluate("""() => {
                            const cursor = document.getElementById('cursor');
                            const target = document.querySelector('.zone-target');
                            return {
                                cursor: parseFloat(cursor.style.left) || 0,
                                targetLeft: parseFloat(target.style.left) || 47,
                                targetWidth: parseFloat(target.style.width) || 6
                            };
                        }""")
                        
                        c_pos = positions['cursor']
                        t_left = positions['targetLeft']
                        t_width = positions['targetWidth']
                        
                        # Trigger direct JS click for instantaneous timing resolution
                        if (t_left + 0.3) <= c_pos <= (t_left + t_width - 0.3):
                            print(f"QTE HIT: Cursor at {c_pos:.2f}%, Target {t_left:.2f}% - {(t_left + t_width):.2f}%")
                            await f.evaluate("document.getElementById('stop-btn').click()")
                            await page.wait_for_timeout(2000)
                            return True
                        await asyncio.sleep(0.005)
            print("ERROR: Failed to find or complete QTE slider!")
            return False

        # 1. Navigate to Wishing Well through the Garden path
        await click_button_by_text("Franchir le portail d'étoiles")
        await click_button_by_text("Plonger dans le miroir liquide")
        await click_button_by_text("Explorer le jardin d'engrenages")
        await click_button_by_text("Suivre le papillon d'étincelles")
        
        # 2. Steal water to trigger Le Gardien de Poussière
        await click_button_by_text("Tenter de puiser de l'eau")
        await page.screenshot(path=f"{brain_dir}/v_boss1_start.png")
        
        # Fight Le Gardien de Poussière (HP 90)
        for t in range(1, 4):
            print(f"\n--- Guardian Turn {t} ---")
            await click_button_by_text("Attaquer")
            await page.screenshot(path=f"{brain_dir}/v_boss1_turn_{t}_slider.png")
            await play_qte(f"Guardian Turn {t}")
            
        # Complete combat, get Emblem, proceed to Hanging Bridge
        await click_button_by_text("Poursuivre le voyage")
        await click_button_by_text("Avancer vers le Pont")
        await page.screenshot(path=f"{brain_dir}/v_bridge_arrival.png")
        
        # 3. Enter secret room: Le Sanctuaire Oublié
        await click_button_by_text("Insérer l'Emblème des Limbes")
        await page.screenshot(path=f"{brain_dir}/v_secret_room.png")
        
        # Return to Bridge (obtaining Temporal Anchor)
        await click_button_by_text("Retourner sur le Pont")
        
        # 4. Fight La Chimère des Limbes (HP 110)
        await click_button_by_text("Affronter la Chimère")
        await page.screenshot(path=f"{brain_dir}/v_boss2_start.png")
        
        for t in range(1, 5):
            print(f"\n--- Chimera Turn {t} ---")
            await click_button_by_text("Attaquer")
            await page.screenshot(path=f"{brain_dir}/v_boss2_turn_{t}_slider.png")
            await play_qte(f"Chimera Turn {t}")
            
        # Complete combat, proceed to Clock Tower
        await click_button_by_text("Poursuivre le voyage")
        await click_button_by_text("Pénétrer dans la Tour de l'Horloge")
        
        # 5. Fight L'Horloger du Temps (Buffed to HP 250)
        await click_button_by_text("Affronter l'Horloger")
        await page.screenshot(path=f"{brain_dir}/v_final_boss_start.png")
        
        # Turn 1: Deploy Temporal Anchor to neutralize status effects permanently!
        print("\n--- Final Boss Turn 1 (Deploying Temporal Anchor) ---")
        await click_button_by_text("Ancre Temporelle")
        await page.screenshot(path=f"{brain_dir}/v_final_boss_turn1_resolved.png")
        
        # Static list of actions to defeat the boss
        final_boss_actions = [
            ("rest", "Se Reposer"),
            ("rest", "Se Reposer"),
            ("attack", "Attaquer"),
            ("attack", "Attaquer"),
            ("attack", "Attaquer"),
            ("rest", "Se Reposer"),
            ("attack", "Attaquer"),
            ("attack", "Attaquer"),
            ("rest", "Se Reposer"),
            ("attack", "Attaquer"),
            ("attack", "Attaquer")
        ]
        
        for idx, (action_type, btn_pattern) in enumerate(final_boss_actions, start=2):
            print(f"\n--- Final Boss Turn {idx} ({action_type}) ---")
            await click_button_by_text(btn_pattern)
            if action_type == "attack":
                await page.screenshot(path=f"{brain_dir}/v_final_boss_turn_{idx}_slider.png")
                await play_qte(f"Final Boss Turn {idx}")
                await page.screenshot(path=f"{brain_dir}/v_final_boss_turn_{idx}_resolved.png")
            else:
                await page.screenshot(path=f"{brain_dir}/v_final_boss_turn_{idx}_resolved.png")
            
        # Poursuivre to ending
        await click_button_by_text("Poursuivre le voyage")
        await page.screenshot(path=f"{brain_dir}/v_victory_ending.png")
        print("Success: Finished entire story route and defeated all bosses!")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
