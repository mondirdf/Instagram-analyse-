# classifier.py
# Gemini-based classification - always used, even if Instagram category exists

import google.generativeai as genai
import json
import config

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def classify_account(account):
    """
    Classify a single account using Gemini.
    Input: {username, bio, category, verified}
    Output: {primary_category, secondary_category, signals, confidence}
    """
    
    prompt = f"""You are a precise category classifier. Analyze the following Instagram account data and return ONLY valid JSON.

INPUT:
- Instagram Category: {account['category'] if account['category'] else 'null'}
- Bio: {account['bio'] if account['bio'] else 'empty'}

ALLOWED CATEGORIES (you MUST choose from this list):
{', '.join(config.ALLOWED_CATEGORIES)}

YOUR TASK:
1. Determine primary_category (most relevant)
2. Determine secondary_category (second most relevant, or null)
3. Provide signal scores (0.0 to 1.0):
   - from_instagram_category: how much the Instagram category influenced your decision
   - from_bio: how much the bio influenced your decision
4. Provide overall confidence (0.0 to 1.0)

RULES:
- Primary must be from allowed list
- Secondary must be from allowed list or null
- Signal scores must sum approximately to your confidence level
- If Instagram category is null, from_instagram_category should be 0.0

OUTPUT FORMAT (JSON only, no explanation):
{{
  "primary_category": "CategoryName",
  "secondary_category": "CategoryName or null",
  "signals": {{
    "from_instagram_category": 0.0-1.0,
    "from_bio": 0.0-1.0
  }},
  "confidence": 0.0-1.0
}}"""

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean JSON (remove markdown if present)
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        # Validate
        assert result["primary_category"] in config.ALLOWED_CATEGORIES
        if result["secondary_category"]:
            assert result["secondary_category"] in config.ALLOWED_CATEGORIES
        
        return result
        
    except Exception as e:
        print(f"  ⚠️ Classification error for @{account['username']}: {e}")
        # Fallback
        return {
            "primary_category": "Other",
            "secondary_category": None,
            "signals": {
                "from_instagram_category": 0.0,
                "from_bio": 0.0
            },
            "confidence": 0.1
        }


def classify_all_accounts(accounts):
    """Classify all accounts and return enriched data"""
    classified = []
    
    print("\n🧠 Classifying accounts with Gemini...")
    for i, account in enumerate(accounts, 1):
        print(f"  {i}/{len(accounts)}: @{account['username']}")
        
        classification = classify_account(account)
        
        # Merge with original account data
        enriched = {
            **account,
            "classification": classification
        }
        
        classified.append(enriched)
    
    print("✅ Classification complete\n")
    return classified
