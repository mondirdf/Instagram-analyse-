# config.py
# Configuration file for API keys and constants

import os

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDD9maL73H-iLRwgygRzq7WLtdhfp4UqeA")

# Instagram credentials (for educational use only)
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "mondir.d.f")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "NINI11")

# Closed taxonomy - DO NOT modify
ALLOWED_CATEGORIES = [
    "Science",
    "Technology",
    "Business",
    "Finance",
    "Education",
    "Programming",
    "Engineering",
    "Health",
    "Fitness",
    "Sports",
    "Entertainment",
    "Gaming",
    "Movies",
    "Music",
    "Art",
    "Design",
    "Photography",
    "Writing",
    "Lifestyle",
    "Travel",
    "Food",
    "Fashion",
    "Motivation",
    "Self-Improvement",
    "Psychology",
    "News",
    "Politics",
    "Culture",
    "Celebrity",
    "Influencer",
    "Religion",
    "Philosophy",
    "Other"
]

# Signal weights
INSTAGRAM_CATEGORY_WEIGHT = 0.6
BIO_WEIGHT = 0.4

# Category weights for interest vector
PRIMARY_WEIGHT = 1.0
SECONDARY_WEIGHT = 0.4

# Knowledge categories
KNOWLEDGE_CATEGORIES = [
    "Science", "Technology", "Education", "Programming", "Engineering"
]

# Entertainment categories
ENTERTAINMENT_CATEGORIES = [
    "Entertainment", "Gaming", "Movies", "Music", "Celebrity", "Influencer"
]

# Scraping limits
MAX_FOLLOWING_TO_SCRAPE = 100  # Limit for educational purposes
