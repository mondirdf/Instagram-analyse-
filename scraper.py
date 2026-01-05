# scraper.py
# Instagram scraper using Playwright - NO data persistence

from playwright.sync_api import sync_playwright
import time
import config

def scrape_following(username, password, target_username):
    """
    Scrape following list from Instagram account.
    Returns list of dicts: {username, bio, category, verified}
    """
    following_list = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Login
            print("🔐 Logging into Instagram...")
            page.goto("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
            time.sleep(5)
            
            # Navigate to target profile
            print(f"📍 Navigating to @{target_username}...")
            page.goto(f"https://www.instagram.com/{target_username}/")
            time.sleep(3)
            
            # Click following
            following_link = page.locator('a[href*="/following/"]').first
            following_link.click()
            time.sleep(3)
            
            # Scrape following list
            print("🔍 Scraping following list...")
            dialog = page.locator('div[role="dialog"]').first
            
            # Scroll to load accounts
            prev_count = 0
            stale_count = 0
            
            while len(following_list) < config.MAX_FOLLOWING_TO_SCRAPE:
                # Get all account elements
                accounts = dialog.locator('a[href^="/"][role="link"]').all()
                
                for account in accounts:
                    try:
                        account_username = account.get_attribute("href").strip("/")
                        
                        # Skip if already processed
                        if any(f["username"] == account_username for f in following_list):
                            continue
                        
                        # Navigate to profile to get bio and category
                        account_data = _get_account_details(page, account_username)
                        
                        if account_data:
                            following_list.append(account_data)
                            print(f"  ✓ {len(following_list)}: @{account_username}")
                        
                        if len(following_list) >= config.MAX_FOLLOWING_TO_SCRAPE:
                            break
                            
                    except Exception as e:
                        continue
                
                # Check if stuck
                if len(following_list) == prev_count:
                    stale_count += 1
                    if stale_count > 3:
                        break
                else:
                    stale_count = 0
                
                prev_count = len(following_list)
                
                # Scroll
                dialog.evaluate("el => el.scrollBy(0, 300)")
                time.sleep(1)
            
            print(f"\n✅ Scraped {len(following_list)} accounts")
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
        finally:
            browser.close()
    
    return following_list


def _get_account_details(page, username):
    """Get bio, category, verified status for a single account"""
    try:
        # Open in new tab to avoid losing dialog
        account_page = page.context.new_page()
        account_page.goto(f"https://www.instagram.com/{username}/", timeout=10000)
        time.sleep(2)
        
        # Extract bio
        bio = ""
        try:
            bio_element = account_page.locator('section header h1').first
            bio = bio_element.inner_text(timeout=2000)
        except:
            pass
        
        # Extract category
        category = None
        try:
            category_element = account_page.locator('div.x7a106z').first
            category = category_element.inner_text(timeout=2000)
        except:
            pass
        
        # Check verified
        verified = False
        try:
            verified_badge = account_page.locator('svg[aria-label*="Verified"]').first
            verified = verified_badge is not None
        except:
            pass
        
        account_page.close()
        
        return {
            "username": username,
            "bio": bio.strip() if bio else "",
            "category": category,
            "verified": verified
        }
        
    except Exception as e:
        return None
