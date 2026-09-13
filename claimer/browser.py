import asyncio
from playwright.async_api import async_playwright, Page

async def claim_game(cookies: list[dict], namespace: str, offer_id: str, slug: str) -> tuple[list[dict], str]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        await context.add_cookies(cookies)
        page = await context.new_page()
        
        purchase_url = f"https://store.epicgames.com/purchase?highlightColor=0078f2&lang=en-US&offers=1-{namespace}-{offer_id}--&showNavigation=true"
        
        try:
            await page.goto(purchase_url, wait_until="domcontentloaded", timeout=60000)

            # Already owned?
            if await page.locator("text=You already own this").count() > 0:
                updated_cookies = await context.cookies()
                return updated_cookies, "already_owned"

            # Wait for the purchase UI to render: Place Order button or captcha
            place_order_btn = page.locator('button[data-testid="place-order-btn"]')
            try:
                await place_order_btn.first.wait_for(timeout=30000)
            except Exception:
                pass

            if await place_order_btn.count() > 0:
                await place_order_btn.first.click(timeout=10000)
            else:
                place_order_btn = page.locator('button:has-text("Place Order")')
                if await place_order_btn.count() > 0:
                    await place_order_btn.first.click(timeout=10000)
                else:
                    if await page.locator(".h-captcha").count() > 0 or await page.locator("iframe[src*='hcaptcha']").count() > 0:
                        updated_cookies = await context.cookies()
                        return updated_cookies, "needs_captcha"
                    updated_cookies = await context.cookies()
                    return updated_cookies, "failed"

            # Wait for either receipt or hcaptcha
            for _ in range(30):
                await asyncio.sleep(1)

                if await page.locator(".h-captcha").count() > 0 or await page.locator("iframe[src*='hcaptcha']").count() > 0:
                    updated_cookies = await context.cookies()
                    return updated_cookies, "needs_captcha"

                if "receipt" in page.url or await page.locator('[data-testid="receipt"]').count() > 0:
                    updated_cookies = await context.cookies()
                    return updated_cookies, "success"

            # Timeout
            updated_cookies = await context.cookies()
            return updated_cookies, "failed"
            
        except Exception as e:
            print(f"Exception during purchase flow: {e}")
            updated_cookies = await context.cookies()
            return updated_cookies, "failed"
        finally:
            await browser.close()
