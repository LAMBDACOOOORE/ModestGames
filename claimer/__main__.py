import asyncio
from claimer.cookies import load_cookies, validate_cookies, save_cookies, sync_github_secret
from claimer.promotions import get_free_games
from claimer.state import is_claimed, mark_claimed
from claimer.email import send_login_prompt, send_message
from claimer.browser import claim_game

async def main():
    cookies = load_cookies()
    
    if not await validate_cookies(cookies):
        print("Cookies are missing or invalid.")
        send_login_prompt(games=[])
        return

    print("Cookies validated successfully.")
    
    try:
        games = get_free_games()
    except Exception as e:
        print(f"Failed to fetch free games: {e}")
        send_message(f"⚠️ <b>Error fetching free games</b>\n<pre>{e}</pre>")
        return
        
    if not games:
        print("No current free games found.")
        return
        
    print(f"Found {len(games)} free games.")
    
    unclaimed_games = [g for g in games if not is_claimed(g["offer_id"])]
    
    if not unclaimed_games:
        print("All current free games have already been claimed.")
        return
        
    print(f"Attempting to claim {len(unclaimed_games)} games: {', '.join(g['title'] for g in unclaimed_games)}")
    
    needs_sync = False
    
    for i, game in enumerate(unclaimed_games):
        if i > 0:
            await asyncio.sleep(2)  # Delay between claims
            
        title = game["title"]
        print(f"Claiming: {title}...")
        
        updated_cookies, status = await claim_game(cookies, game["namespace"], game["offer_id"], game["slug"])
        
        # Always update our working cookies with latest state
        if updated_cookies:
            cookies = updated_cookies
            needs_sync = True
            
        if status == "success":
            print(f"✅ Successfully claimed {title}!")
            mark_claimed(game["offer_id"], title)
            send_message(f"🎉 <b>Successfully claimed:</b> {title}")
        elif status == "already_owned":
            print(f"ℹ️ Already owned {title}.")
            mark_claimed(game["offer_id"], title)
        elif status == "needs_captcha":
            print("❌ Captcha required or login expired during checkout.")
            # Send prompt for remaining games
            remaining = [g["title"] for g in unclaimed_games[i:]]
            send_login_prompt(remaining)
            break
        else:
            print(f"❌ Failed to claim {title}.")
            send_message(f"⚠️ <b>Failed to claim:</b> {title}\nCheck the GitHub Actions logs.")

    if needs_sync:
        print("Saving updated cookies...")
        save_cookies(cookies)
        sync_github_secret(cookies)

if __name__ == "__main__":
    asyncio.run(main())
