# inference.py
# Gemini inference layer - receives ONLY numbers, generates probabilistic text

import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_summary(interest_vector, metrics):
    """
    Generate 2-3 sentence probabilistic summary from numeric data only.
    NO usernames, NO diagnosis, NO judgments.
    """
    
    # Prepare numeric input (top categories only)
    top_categories = dict(sorted(
        interest_vector.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:5])
    
    prompt = f"""You are analyzing interest distribution patterns from Instagram following data. Generate a 2-3 sentence probabilistic summary.

NUMERIC INPUT:
Interest Distribution (top categories, %):
{', '.join(f"{k}: {v:.1f}%" for k, v in top_categories.items())}

Metrics:
- Diversity Index: {metrics['diversity_index']}
- Knowledge/Entertainment Ratio: {metrics['knowledge_entertainment_ratio']}
- Celebrity Ratio: {metrics['celebrity_ratio']}

REQUIREMENTS:
1. Write 2-3 sentences maximum
2. Use probabilistic language: "suggests", "indicates", "may reflect", "appears to", "likely"
3. Describe patterns, NOT personality
4. NO diagnosis, NO judgments
5. Focus on distribution and balance
6. Do NOT mention usernames or specific accounts

EXAMPLE OUTPUT:
"The interest distribution suggests a balanced engagement across multiple domains, with notable emphasis on technology and science-related content. The moderate diversity index indicates focused but not narrow interests. The knowledge-to-entertainment ratio reflects a slight preference toward educational material."

YOUR SUMMARY:"""

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
        # Remove any quotes if present
        summary = summary.replace('"', '').replace("'", "")
        
        return summary
        
    except Exception as e:
        print(f"⚠️ Summary generation error: {e}")
        return "Unable to generate summary due to API limitations."


def generate_full_report(interest_vector, metrics):
    """
    Generate complete textual report with disclaimers.
    """
    print("✍️ Generating summary with Gemini...\n")
    
    summary = generate_summary(interest_vector, metrics)
    
    confidence_note = (
        "Note: This analysis is based on publicly visible following patterns and "
        "represents probabilistic indicators rather than definitive assessments."
    )
    
    ethical_disclaimer = (
        "Ethical Notice: This tool is for educational self-analysis only. "
        "It should not be used for profiling others, making decisions about people, "
        "or any commercial purposes. All data is processed in-memory and not stored."
    )
    
    report = {
        "summary": summary,
        "confidence_note": confidence_note,
        "ethical_disclaimer": ethical_disclaimer
    }
    
    print("✅ Summary generated\n")
    
    return report
