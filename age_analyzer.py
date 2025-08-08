#!/usr/bin/env python3
"""
Express Entry Age Analysis - Focused Scraper
Specifically analyzes how age affects CRS scores
"""

import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgeScoreAnalyzer:
    def __init__(self):
        """Initialize the analyzer"""
        self.url = "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/check-score.html"
        self.setup_driver()
        self.age_scores = []

    def setup_driver(self):
        """Set up Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 15)

    def load_page(self):
        """Load the calculator page"""
        logger.info("Loading calculator page...")
        self.driver.get(self.url)
        time.sleep(5)

        # Wait for page to load completely
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.TAG_NAME, "body")))
            logger.info("Page loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load page: {e}")
            return False

    def find_calculator_elements(self):
        """Find and analyze calculator elements"""
        logger.info("Searching for calculator elements...")

        # Print page source length for debugging
        page_source = self.driver.page_source
        logger.info(f"Page source length: {len(page_source)}")

        # Look for various calculator indicators
        selectors_to_try = [
            "form",
            "[data-wb-fieldflow]",
            ".wb-fieldflow",
            "fieldset",
            "input[type='radio']",
            "select",
            ".form-group",
            "[role='form']"
        ]

        found_elements = {}
        for selector in selectors_to_try:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    found_elements[selector] = len(elements)
                    logger.info(
                        f"Found {len(elements)} elements for selector: {selector}")
            except Exception as e:
                logger.debug(f"Error with selector {selector}: {e}")

        return found_elements

    def analyze_page_content(self):
        """Analyze the page content to understand structure"""
        logger.info("Analyzing page content...")

        # Get all text content
        body_text = self.driver.find_element(By.TAG_NAME, "body").text

        # Look for calculator-related keywords
        calculator_keywords = [
            "marital status",
            "age",
            "education",
            "language",
            "work experience",
            "calculate",
            "score",
            "points"
        ]

        found_keywords = []
        for keyword in calculator_keywords:
            if keyword.lower() in body_text.lower():
                found_keywords.append(keyword)

        logger.info(f"Found keywords: {found_keywords}")

        # Try to find calculator start button or form
        try:
            # Look for common calculator trigger elements
            triggers = self.driver.find_elements(
                By.XPATH, "//*[contains(text(), 'Calculate') or contains(text(), 'Start') or contains(text(), 'Begin')]")
            if triggers:
                logger.info(
                    f"Found {len(triggers)} potential calculator triggers")
                for trigger in triggers:
                    logger.info(f"Trigger text: {trigger.text}")

            # Try clicking the first trigger
            if triggers:
                trigger = triggers[0]
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", trigger)
                time.sleep(2)
                self.driver.execute_script("arguments[0].click();", trigger)
                time.sleep(3)
                logger.info("Clicked calculator trigger")

        except Exception as e:
            logger.error(f"Error with calculator triggers: {e}")

    def create_simple_analysis(self):
        """Create a simple analysis based on known age scoring patterns"""
        logger.info("Creating theoretical age score analysis...")

        # Known CRS age scoring pattern (approximate)
        age_data = []
        for age in range(18, 46):
            if age <= 29:
                points = 110  # Maximum points
            elif age <= 31:
                points = 105
            elif age <= 32:
                points = 100
            elif age <= 33:
                points = 95
            elif age <= 34:
                points = 90
            elif age <= 35:
                points = 85
            elif age <= 36:
                points = 80
            elif age <= 37:
                points = 75
            elif age <= 38:
                points = 70
            elif age <= 39:
                points = 65
            elif age <= 40:
                points = 60
            elif age <= 41:
                points = 55
            elif age <= 42:
                points = 50
            elif age <= 43:
                points = 45
            elif age <= 44:
                points = 35
            else:
                points = 25

            age_data.append({'age': age, 'points': points})

        return pd.DataFrame(age_data)

    def create_visualizations(self, age_df):
        """Create visualizations for age score analysis"""
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Express Entry Age Score Analysis', fontsize=16)

        # 1. Age vs Points line chart
        axes[0, 0].plot(age_df['age'], age_df['points'],
                        marker='o', linewidth=2, markersize=4)
        axes[0, 0].set_title('CRS Points by Age')
        axes[0, 0].set_xlabel('Age')
        axes[0, 0].set_ylabel('Points')
        axes[0, 0].grid(True, alpha=0.3)

        # 2. Points distribution
        axes[0, 1].hist(age_df['points'], bins=15, alpha=0.7,
                        color='skyblue', edgecolor='black')
        axes[0, 1].set_title('Distribution of Age Points')
        axes[0, 1].set_xlabel('Points')
        axes[0, 1].set_ylabel('Frequency')

        # 3. Age groups analysis
        age_df['age_group'] = pd.cut(age_df['age'],
                                     bins=[17, 25, 30, 35, 40, 46],
                                     labels=['18-25', '26-30', '31-35', '36-40', '41-45'])
        age_group_stats = age_df.groupby(
            'age_group')['points'].agg(['mean', 'min', 'max'])

        x_pos = range(len(age_group_stats))
        axes[1, 0].bar(x_pos, age_group_stats['mean'],
                       alpha=0.7, color='lightcoral')
        axes[1, 0].set_title('Average Points by Age Group')
        axes[1, 0].set_xlabel('Age Group')
        axes[1, 0].set_ylabel('Average Points')
        axes[1, 0].set_xticks(x_pos)
        axes[1, 0].set_xticklabels(age_group_stats.index, rotation=45)

        # 4. Point decline rate
        age_df['point_decline'] = age_df['points'].diff().fillna(0)
        axes[1, 1].bar(age_df['age'], -age_df['point_decline'],
                       alpha=0.7, color='orange')
        axes[1, 1].set_title('Points Lost Each Year')
        axes[1, 1].set_xlabel('Age')
        axes[1, 1].set_ylabel('Points Lost')
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('age_score_analysis.png', dpi=300, bbox_inches='tight')
        logger.info("Age analysis chart saved as 'age_score_analysis.png'")
        plt.show()

        return age_group_stats

    def generate_insights(self, age_df, age_group_stats):
        """Generate insights from the analysis"""
        insights = []

        max_points = age_df['points'].max()
        max_age = age_df[age_df['points'] == max_points]['age'].iloc[0]

        insights.append(
            f"Maximum age points ({max_points}) are awarded up to age {max_age}")

        # Find the steepest decline
        age_df['decline_rate'] = age_df['points'].diff()
        steepest_decline = age_df['decline_rate'].min()
        steepest_age = age_df[age_df['decline_rate']
                              == steepest_decline]['age'].iloc[0]

        insights.append(
            f"Steepest point decline ({abs(steepest_decline)} points) occurs at age {steepest_age}")

        # Age group insights
        best_group = age_group_stats['mean'].idxmax()
        worst_group = age_group_stats['mean'].idxmin()

        insights.append(
            f"Best age group: {best_group} (avg {age_group_stats.loc[best_group, 'mean']:.1f} points)")
        insights.append(
            f"Worst age group: {worst_group} (avg {age_group_stats.loc[worst_group, 'mean']:.1f} points)")

        return insights

    def run_analysis(self):
        """Run the complete analysis"""
        try:
            # Load page
            if not self.load_page():
                logger.error(
                    "Could not load page, continuing with theoretical analysis")

            # Try to find calculator elements
            self.find_calculator_elements()

            # Analyze page content
            self.analyze_page_content()

            # Create theoretical analysis
            age_df = self.create_simple_analysis()

            # Create visualizations
            age_group_stats = self.create_visualizations(age_df)

            # Generate insights
            insights = self.generate_insights(age_df, age_group_stats)

            # Print results
            logger.info("\n" + "="*50)
            logger.info("EXPRESS ENTRY AGE ANALYSIS RESULTS")
            logger.info("="*50)

            for insight in insights:
                logger.info(f"• {insight}")

            logger.info("\nAge Group Statistics:")
            logger.info(age_group_stats)

            # Save data
            age_df.to_csv('age_analysis_data.csv', index=False)
            logger.info("\nData saved to 'age_analysis_data.csv'")

        except Exception as e:
            logger.error(f"Error during analysis: {e}")
        finally:
            self.close()

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    analyzer = AgeScoreAnalyzer()
    analyzer.run_analysis()
