# Instagram Interest Analysis - Educational Tool

Educational Python tool for analyzing Instagram following patterns using hybrid classification and LLM inference.

## ⚠️ Important Disclaimers

- **Educational Use Only**: This tool is for personal learning and self-analysis
- **Single User**: Only analyze your own account
- **No Storage**: All data processed in-memory, nothing saved permanently
- **No Diagnosis**: Provides probabilistic indicators, not personality assessments
- **Public Accounts Only**: Target account must be public
- **API Limits**: Respects Instagram and Gemini API rate limits

## 🏗️ Architecture

```
project/
├── main.py              # Main orchestrator
├── scraper.py           # Playwright-based Instagram scraper
├── classifier.py        # Gemini classification layer
├── vectorizer.py        # Numeric fusion and metrics
├── inference.py         # Gemini text generation (numbers only)
├── visualization.py     # Matplotlib charts
├── config.py            # Configuration and constants
└── requirements.txt     # Python dependencies
```

## 📋 Requirements

1. **Python 3.8+**
2. **Instagram Account** (to login)
3. **Gemini API Key** (from Google AI Studio)
4. **Target Account** must be public

## 🚀 Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

### 3. Configure Environment Variables

```bash
export INSTAGRAM_USERNAME="your_username"
export INSTAGRAM_PASSWORD="your_password"
export GEMINI_API_KEY="your_gemini_api_key"
```

Or edit `config.py` directly (not recommended for security).

## ▶️ Usage

```bash
python main.py
```

Follow the prompts:
1. Enter your Instagram username
2. Wait for scraping (may take several minutes)
3. Classification and analysis runs automatically
4. View results in terminal and generated images

## 📊 Output

### Console Output
- Interest distribution percentages
- Diversity index (Shannon entropy)
- Knowledge/Entertainment ratio
- Celebrity ratio
- AI-generated probabilistic summary

### Visual Output
- `interest_bar.png` - Bar chart of top 10 categories
- `interest_radar.png` - Radar chart of top 8 categories

## 🔬 Methodology

### Classification Pipeline
1. **Data Collection**: Scrape following list (username, bio, category, verified)
2. **Gemini Classification**: Every account classified by Gemini
   - Input: Instagram category + bio
   - Output: primary/secondary categories + confidence
3. **Numeric Fusion**: Weighted combination
   - Instagram category weight: 0.6
   - Bio weight: 0.4
4. **Interest Vector**: Aggregate weighted categories
5. **Metrics Calculation**:
   - Shannon entropy (diversity)
   - Knowledge/Entertainment ratio
   - Celebrity ratio
6. **Inference**: Gemini generates summary from numbers only

### Closed Taxonomy
33 predefined categories including Science, Technology, Business, Health, Entertainment, Art, Lifestyle, and more. See `config.py` for full list.

## 🛡️ Privacy & Ethics

- **Self-Analysis Only**: Do not use on others
- **In-Memory Processing**: No data persistence
- **No Identifiable Info**: Gemini never receives usernames in inference
- **Probabilistic Output**: Results are indicators, not diagnoses
- **Educational Purpose**: Not for commercial or decision-making use

## ⚙️ Configuration

Edit `config.py` to adjust:
- `MAX_FOLLOWING_TO_SCRAPE`: Default 100 (for speed)
- `ALLOWED_CATEGORIES`: Closed taxonomy
- Signal weights (Instagram/Bio)
- Category groupings (Knowledge/Entertainment)

## 🐛 Troubleshooting

**Scraping fails:**
- Ensure Instagram account is valid
- Target account must be public
- Instagram may have changed HTML structure
- Try running with `headless=False` to debug

**Classification errors:**
- Check Gemini API key validity
- API may have rate limits
- Fallback to "Other" category on errors

**No visualization:**
- Ensure matplotlib is installed
- Check write permissions in directory

## 📚 Dependencies

- `playwright`: Web automation for scraping
- `google-generativeai`: Gemini API client
- `matplotlib`: Visualization
- `numpy`: Numerical operations

## 📄 License

Educational use only. Not for redistribution or commercial purposes.

## 🤝 Contributing

This is a locked educational reference implementation. For learning purposes only.

## ⚖️ Legal

- Complies with Instagram Terms of Service for personal use
- Uses publicly available data only
- No circumvention of access controls
- Educational fair use of Gemini API

---

**Remember**: This tool is for understanding your own digital footprint, not for profiling others.
