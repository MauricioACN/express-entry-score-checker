# 🍁 Express Entry Score Checker

A comprehensive Python web scraping and analysis tool for analyzing Canada's Express Entry Comprehensive Ranking System (CRS) scores. This tool helps you understand how different factors affect your immigration score and optimize your profile for maximum points.

## 🎯 Features

- **Comprehensive Score Analysis**: Analyzes all CRS factors including age, education, language, and work experience
- **Interactive Visualizations**: Creates detailed charts showing score variations across different parameters
- **Web Scraping Capability**: Extracts real-time data from the official Express Entry calculator
- **Optimization Recommendations**: Provides actionable insights to improve your CRS score
- **Multiple Analysis Types**: Age-focused analysis, education impact, language proficiency effects, and more

## 📊 What You'll Get

### Generated Files:
- `comprehensive_crs_analysis.png` - Main visualization dashboard
- `age_impact_analysis.csv` - Detailed age scoring data
- `education_impact_analysis.csv` - Education level comparisons
- `language_impact_analysis.csv` - Language proficiency analysis
- `optimal_combinations.csv` - Highest scoring profile combinations

### Key Insights:
- How age affects your score (and when you start losing points)
- Which education levels provide the best ROI
- Language proficiency targets for maximum points
- Optimal combinations of factors for highest scores
- Skill transferability bonus calculations

## 🚀 Quick Start

### 1. Setup
```bash
# Clone or download the repository
cd express-entry-score-checker

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Analysis
```bash
# Quick comprehensive analysis
python run_analysis.py --quick

# Interactive menu
python run_analysis.py
```

### 3. Individual Scripts
```bash
# Comprehensive analysis (recommended)
python comprehensive_analyzer.py

# Age-focused analysis
python age_analyzer.py

# Web scraper (experimental)
python express_entry_scraper.py
```

## 📈 Analysis Types

### 1. Comprehensive Analysis (`comprehensive_analyzer.py`)
- **What it does**: Analyzes all CRS factors using official scoring rules
- **Output**: 9-panel visualization showing age impact, education comparison, language effects, optimal combinations, and more
- **Best for**: Getting a complete picture of CRS scoring

### 2. Age Impact Analysis (`age_analyzer.py`)
- **What it does**: Focuses specifically on how age affects scores
- **Output**: Age decline charts and group comparisons
- **Best for**: Understanding the age factor and planning timing

### 3. Web Scraper (`express_entry_scraper.py`)
- **What it does**: Attempts to scrape the official calculator for real-time data
- **Output**: Raw scraped data and analysis
- **Best for**: Getting current scoring data (experimental)

## 📋 Key Findings

Based on official CRS criteria:

### Age Factor
- **Maximum points**: 110 (ages 18-29)
- **Score decline**: Starts at age 30
- **Critical ages**: Major drops at 30, 35, 40, 44

### Education Impact
- **Doctoral degree**: 150 points
- **Master's degree**: 135 points
- **Bachelor's (4-year)**: 120 points
- **Bachelor's (3-year)**: 112 points

### Language Proficiency
- **CLB 10+**: 136 points (all skills)
- **CLB 9**: 124 points
- **CLB 8**: 92 points
- **CLB 7**: 64 points

### Work Experience
- **5+ years**: 80 points (maximum)
- **3 years**: 64 points
- **1 year**: 40 points

## 🎯 Optimization Tips

1. **Language First**: Language improvement gives the highest return on investment
2. **Age Timing**: Apply before major age thresholds (30, 35, 40)
3. **Education ROI**: Consider master's degree if under 30
4. **Skill Transferability**: Combine high education + language + experience for bonus points
5. **Foreign Experience**: Can add significant transferability points

## 🔧 Technical Requirements

- Python 3.8+
- Chrome browser (for web scraping)
- Required packages (see requirements.txt):
  - selenium
  - pandas
  - matplotlib
  - seaborn
  - beautifulsoup4
  - webdriver-manager

## 📱 Usage Examples

### Get Optimal Profile for Your Age
```python
from comprehensive_analyzer import ComprehensiveScoreAnalyzer

analyzer = ComprehensiveScoreAnalyzer()
score = analyzer.calculate_total_score(
    age=28,
    education='master_degree',
    language='clb_9',
    work_exp='3_years',
    foreign_exp=2
)
print(f"Your estimated CRS score: {score}")
```

### Analyze Age Impact
```python
from age_analyzer import AgeScoreAnalyzer

analyzer = AgeScoreAnalyzer()
analyzer.run_analysis()  # Generates age analysis charts
```

## 📊 Sample Visualizations

The tool generates comprehensive charts including:
- Age vs Score curves for different profiles
- Education level comparisons
- Language proficiency impact
- Score component breakdowns
- Optimal combination rankings
- Heatmaps for factor combinations

## ⚠️ Important Notes

- **Accuracy**: Based on official CRS criteria as of 2025
- **No Job Offers**: Reflects the removal of job offer points (March 2025)
- **Estimates**: Scores are estimates for planning purposes
- **Official Source**: Always verify with official IRCC tools
- **Updates**: CRS criteria may change; check official sources

## 🤝 Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting improvements
- Adding new analysis features
- Updating scoring criteria

## 📞 Support

If you encounter issues:
1. Check the `analysis_log.txt` file for error details
2. Ensure all dependencies are installed
3. Verify Chrome browser is available for web scraping
4. Check official IRCC website for scoring updates

## 📚 Resources

- [Official Express Entry Tool](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/check-score.html)
- [CRS Criteria Documentation](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/check-score/crs-criteria.html)
- [Express Entry Rounds](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/rounds-invitations.html)

---

**Disclaimer**: This tool is for educational and planning purposes. Always use official IRCC tools for accurate scoring and immigration advice.