# main.py
# Main orchestrator - runs the complete pipeline

import json
import config
from scraper import scrape_following
from classifier import classify_all_accounts
from vectorizer import compute_all_metrics
from inference import generate_full_report
from visualization import create_all_visualizations


def print_separator():
    print("\n" + "="*70 + "\n")


def print_results(interest_vector, metrics, report):
    """Print formatted results to console"""
    print_separator()
    print("📊 INTEREST DISTRIBUTION")
    print_separator()
    
    sorted_interests = sorted(interest_vector.items(), key=lambda x: x[1], reverse=True)
    for category, percentage in sorted_interests:
        bar_length = int(percentage / 2)  # Scale for display
        bar = "█" * bar_length
        print(f"{category:20} {percentage:5.1f}% {bar}")
    
    print_separator()
    print("📈 DERIVED METRICS")
    print_separator()
    print(f"Diversity Index (Shannon Entropy): {metrics['diversity_index']:.3f}")
    print(f"Knowledge/Entertainment Ratio:     {metrics['knowledge_entertainment_ratio']:.2f}")
    print(f"Celebrity Ratio:                   {metrics['celebrity_ratio']:.2f}")
    print(f"Distribution Skewness:             {metrics['skewness']:.3f}")
    
    print_separator()
    print("💬 SUMMARY")
    print_separator()
    print(report['summary'])
    print()
    print("⚠️", report['confidence_note'])
    print()
    print("🛡️", report['ethical_disclaimer'])
    print_separator()


def main():
    """Main execution pipeline"""
    
    print("\n" + "="*70)
    print("  INSTAGRAM INTEREST ANALYSIS - EDUCATIONAL VERSION")
    print("="*70)
    
    # Input
    target_username = input("\n📝 Enter your Instagram username: ").strip()
    
    if not target_username:
        print("❌ Username required")
        return
    
    print(f"\n🎯 Analyzing account: @{target_username}")
    print("⚠️  This is for educational self-analysis only")
    print("⚠️  The account must be public")
    print("⚠️  No data will be stored permanently\n")
    
    input("Press ENTER to continue...")
    
    # Check credentials
    if not config.INSTAGRAM_USERNAME or not config.INSTAGRAM_PASSWORD:
        print("\n❌ Instagram credentials not configured")
        print("Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in environment variables")
        return
    
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n❌ Gemini API key not configured")
        print("Set GEMINI_API_KEY in environment variables")
        return
    
    try:
        # Step 1: Scrape
        print_separator()
        print("STEP 1: DATA COLLECTION")
        print_separator()
        
        following_accounts = scrape_following(
            config.INSTAGRAM_USERNAME,
            config.INSTAGRAM_PASSWORD,
            target_username
        )
        
        if not following_accounts:
            print("❌ No accounts found or scraping failed")
            return
        
        # Step 2: Classify
        print_separator()
        print("STEP 2: CLASSIFICATION")
        print_separator()
        
        classified_accounts = classify_all_accounts(following_accounts)
        
        # Step 3: Vectorize and compute metrics
        print_separator()
        print("STEP 3: NUMERIC ANALYSIS")
        print_separator()
        
        results = compute_all_metrics(classified_accounts)
        interest_vector = results['interest_vector']
        metrics = results['metrics']
        
        # Step 4: Generate summary
        print_separator()
        print("STEP 4: INFERENCE")
        print_separator()
        
        report = generate_full_report(interest_vector, metrics)
        
        # Step 5: Visualize
        print_separator()
        print("STEP 5: VISUALIZATION")
        print_separator()
        
        create_all_visualizations(interest_vector)
        
        # Display results
        print_results(interest_vector, metrics, report)
        
        print("✅ Analysis complete!")
        print("\n📁 Output files generated:")
        print("   - interest_bar.png")
        print("   - interest_radar.png")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
