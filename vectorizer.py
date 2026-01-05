# vectorizer.py
# Pure numeric fusion and metric calculation - NO AI

import math
from collections import defaultdict
import config

def fuse_signals(classification):
    """
    Apply numeric fusion logic:
    - Instagram weight = 0.6
    - Bio weight = 0.4
    Returns final signal strength
    """
    signals = classification["signals"]
    
    instagram_signal = signals.get("from_instagram_category", 0.0)
    bio_signal = signals.get("from_bio", 0.0)
    
    final_signal = (
        instagram_signal * config.INSTAGRAM_CATEGORY_WEIGHT +
        bio_signal * config.BIO_WEIGHT
    )
    
    return final_signal


def build_interest_vector(classified_accounts):
    """
    Build interest vector with weighted categories.
    Returns: dict of {category: weight_sum}
    """
    interest_vector = defaultdict(float)
    
    for account in classified_accounts:
        classification = account["classification"]
        final_signal = fuse_signals(classification)
        
        # Add primary category
        primary = classification["primary_category"]
        interest_vector[primary] += config.PRIMARY_WEIGHT * final_signal
        
        # Add secondary category if exists
        secondary = classification.get("secondary_category")
        if secondary and secondary != "null":
            interest_vector[secondary] += config.SECONDARY_WEIGHT * final_signal
    
    # Normalize to percentages
    total = sum(interest_vector.values())
    if total > 0:
        interest_vector = {k: (v / total) * 100 for k, v in interest_vector.items()}
    
    return dict(interest_vector)


def calculate_shannon_entropy(interest_vector):
    """
    Calculate Shannon entropy (diversity index).
    H = -Σ(p * log2(p))
    """
    if not interest_vector:
        return 0.0
    
    entropy = 0.0
    for percentage in interest_vector.values():
        if percentage > 0:
            p = percentage / 100.0  # Convert to probability
            entropy -= p * math.log2(p)
    
    return round(entropy, 3)


def calculate_knowledge_entertainment_ratio(interest_vector):
    """
    Calculate ratio: Knowledge / Entertainment
    Knowledge = Science + Technology + Education + Programming + Engineering
    Entertainment = Entertainment + Gaming + Movies + Music + Celebrity + Influencer
    """
    knowledge_sum = sum(
        interest_vector.get(cat, 0) 
        for cat in config.KNOWLEDGE_CATEGORIES
    )
    
    entertainment_sum = sum(
        interest_vector.get(cat, 0) 
        for cat in config.ENTERTAINMENT_CATEGORIES
    )
    
    if entertainment_sum == 0:
        return float('inf') if knowledge_sum > 0 else 0.0
    
    return round(knowledge_sum / entertainment_sum, 2)


def calculate_celebrity_ratio(classified_accounts):
    """
    Calculate celebrity ratio: verified_accounts / total_accounts
    """
    if not classified_accounts:
        return 0.0
    
    verified_count = sum(1 for acc in classified_accounts if acc.get("verified", False))
    total = len(classified_accounts)
    
    return round(verified_count / total, 2)


def calculate_skewness(interest_vector):
    """
    Optional: Calculate distribution skewness
    """
    if not interest_vector:
        return 0.0
    
    values = list(interest_vector.values())
    n = len(values)
    
    if n < 3:
        return 0.0
    
    mean = sum(values) / n
    std = math.sqrt(sum((x - mean) ** 2 for x in values) / n)
    
    if std == 0:
        return 0.0
    
    skew = sum(((x - mean) / std) ** 3 for x in values) / n
    
    return round(skew, 3)


def compute_all_metrics(classified_accounts):
    """
    Compute complete metrics package.
    Returns: {interest_vector, metrics}
    """
    print("📊 Building interest vector and computing metrics...")
    
    interest_vector = build_interest_vector(classified_accounts)
    
    metrics = {
        "diversity_index": calculate_shannon_entropy(interest_vector),
        "knowledge_entertainment_ratio": calculate_knowledge_entertainment_ratio(interest_vector),
        "celebrity_ratio": calculate_celebrity_ratio(classified_accounts),
        "skewness": calculate_skewness(interest_vector)
    }
    
    print("✅ Metrics computed\n")
    
    return {
        "interest_vector": interest_vector,
        "metrics": metrics
    }
