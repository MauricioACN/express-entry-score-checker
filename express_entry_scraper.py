#!/usr/bin/env python3
"""
Express Entry Score Checker - Web Scraper
Analyzes how different answers affect the CRS (Comprehensive Ranking System) score
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
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ExpressEntryScoreScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with Chrome driver"""
        self.url = "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/check-score.html"
        self.driver = None
        self.headless = headless
        self.setup_driver()
        self.results = []

    def setup_driver(self):
        """Set up Chrome driver with appropriate options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def load_calculator(self):
        """Load the Express Entry calculator page"""
        logger.info("Loading Express Entry calculator...")
        self.driver.get(self.url)
        time.sleep(3)

        # Wait for the calculator to load
        try:
            # Look for the first question or the calculator container
            self.wait.until(EC.presence_of_element_located(
                (By.TAG_NAME, "form")))
            logger.info("Calculator loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load calculator: {e}")
            return False

    def analyze_form_structure(self):
        """Analyze the form structure to understand questions and options"""
        logger.info("Analyzing form structure...")

        # Get all form elements
        questions = []

        try:
            # Look for fieldsets or question containers
            fieldsets = self.driver.find_elements(By.TAG_NAME, "fieldset")
            if not fieldsets:
                # Try to find other question containers
                fieldsets = self.driver.find_elements(
                    By.CSS_SELECTOR, "[data-question], .question, .form-group")

            for i, fieldset in enumerate(fieldsets):
                question_data = {
                    'index': i,
                    'text': '',
                    'type': '',
                    'options': [],
                    'element': fieldset
                }

                # Get question text
                legend = fieldset.find_elements(By.TAG_NAME, "legend")
                if legend:
                    question_data['text'] = legend[0].text.strip()
                else:
                    # Try to find question text in labels or headings
                    labels = fieldset.find_elements(By.TAG_NAME, "label")
                    if labels:
                        question_data['text'] = labels[0].text.strip()

                # Identify question type and get options
                radio_buttons = fieldset.find_elements(
                    By.CSS_SELECTOR, "input[type='radio']")
                select_elements = fieldset.find_elements(By.TAG_NAME, "select")
                checkboxes = fieldset.find_elements(
                    By.CSS_SELECTOR, "input[type='checkbox']")

                if radio_buttons:
                    question_data['type'] = 'radio'
                    for radio in radio_buttons:
                        label = self.get_label_for_input(radio)
                        question_data['options'].append({
                            'value': radio.get_attribute('value'),
                            'text': label,
                            'element': radio
                        })
                elif select_elements:
                    question_data['type'] = 'select'
                    select = select_elements[0]
                    options = select.find_elements(By.TAG_NAME, "option")
                    for option in options:
                        if option.get_attribute('value'):  # Skip empty options
                            question_data['options'].append({
                                'value': option.get_attribute('value'),
                                'text': option.text.strip(),
                                'element': option
                            })
                elif checkboxes:
                    question_data['type'] = 'checkbox'
                    for checkbox in checkboxes:
                        label = self.get_label_for_input(checkbox)
                        question_data['options'].append({
                            'value': checkbox.get_attribute('value'),
                            'text': label,
                            'element': checkbox
                        })

                if question_data['text'] and question_data['options']:
                    questions.append(question_data)

            logger.info(f"Found {len(questions)} questions")
            return questions

        except Exception as e:
            logger.error(f"Error analyzing form structure: {e}")
            return []

    def get_label_for_input(self, input_element):
        """Get the label text for an input element"""
        try:
            # Try to find label by 'for' attribute
            input_id = input_element.get_attribute('id')
            if input_id:
                label = self.driver.find_element(
                    By.CSS_SELECTOR, f"label[for='{input_id}']")
                return label.text.strip()
        except:
            pass

        try:
            # Try to find parent label
            parent = input_element.find_element(By.XPATH, "..")
            if parent.tag_name.lower() == 'label':
                return parent.text.strip()
        except:
            pass

        try:
            # Try to find sibling label
            sibling = input_element.find_element(
                By.XPATH, "./following-sibling::label")
            return sibling.text.strip()
        except:
            pass

        return input_element.get_attribute('value') or 'Unknown'

    def get_current_score(self):
        """Extract the current score from the page"""
        try:
            # Look for score elements - these may have different selectors
            score_selectors = [
                "[data-score]",
                ".score",
                ".total-score",
                ".crs-score",
                "#score",
                ".result",
                ".points"
            ]

            for selector in score_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    # Try to extract numeric score
                    import re
                    score_match = re.search(r'(\d+)', text)
                    if score_match:
                        return int(score_match.group(1))

            # If no score found, return 0
            return 0

        except Exception as e:
            logger.error(f"Error getting score: {e}")
            return 0

    def test_combinations(self, questions, max_combinations=100):
        """Test different combinations of answers to see score variations"""
        logger.info(
            f"Testing combinations of answers (max: {max_combinations})...")

        if not questions:
            logger.warning("No questions found to test")
            return

        # Focus on questions that are likely to affect scoring significantly
        # We'll test the first few questions with multiple combinations
        import itertools

        tested_combinations = 0

        # Test systematic combinations of the first few questions
        # Limit to first 3 questions to avoid too many combinations
        for i, question in enumerate(questions[:3]):
            if tested_combinations >= max_combinations:
                break

            logger.info(f"Testing question {i+1}: {question['text'][:50]}...")

            for option in question['options']:
                if tested_combinations >= max_combinations:
                    break

                try:
                    # Reset form or reload page for clean state
                    self.load_calculator()
                    time.sleep(2)

                    # Re-analyze form structure for fresh elements
                    current_questions = self.analyze_form_structure()
                    if not current_questions or i >= len(current_questions):
                        continue

                    current_question = current_questions[i]

                    # Select the option
                    self.select_option(current_question, option['value'])
                    time.sleep(1)

                    # Get score after this selection
                    score = self.get_current_score()

                    # Record result
                    result = {
                        'question_index': i,
                        'question_text': question['text'],
                        'option_value': option['value'],
                        'option_text': option['text'],
                        'score': score,
                        'timestamp': datetime.now().isoformat()
                    }

                    self.results.append(result)
                    logger.info(
                        f"Combination {tested_combinations + 1}: {option['text'][:30]} -> Score: {score}")
                    tested_combinations += 1

                except Exception as e:
                    logger.error(f"Error testing combination: {e}")
                    continue

        logger.info(f"Completed testing {tested_combinations} combinations")

    def select_option(self, question, option_value):
        """Select an option for a given question"""
        try:
            if question['type'] == 'radio':
                # Find and click radio button
                radio = self.driver.find_element(
                    By.CSS_SELECTOR, f"input[type='radio'][value='{option_value}']")
                self.driver.execute_script("arguments[0].click();", radio)
            elif question['type'] == 'select':
                # Find and select from dropdown
                select_element = question['element'].find_element(
                    By.TAG_NAME, "select")
                select = Select(select_element)
                select.select_by_value(option_value)
            elif question['type'] == 'checkbox':
                # Find and check checkbox
                checkbox = self.driver.find_element(
                    By.CSS_SELECTOR, f"input[type='checkbox'][value='{option_value}']")
                if not checkbox.is_selected():
                    self.driver.execute_script(
                        "arguments[0].click();", checkbox)
        except Exception as e:
            logger.error(f"Error selecting option {option_value}: {e}")

    def save_results(self, filename="express_entry_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        logger.info(f"Results saved to {filename}")

    def create_visualizations(self):
        """Create charts showing score variations"""
        if not self.results:
            logger.warning("No results to visualize")
            return

        df = pd.DataFrame(self.results)

        # Create plots
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Express Entry Score Analysis', fontsize=16)

        # 1. Score distribution
        axes[0, 0].hist(df['score'], bins=20, alpha=0.7,
                        color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Score Distribution')
        axes[0, 0].set_xlabel('Score')
        axes[0, 0].set_ylabel('Frequency')

        # 2. Score by question
        if len(df['question_index'].unique()) > 1:
            df.boxplot(column='score', by='question_index', ax=axes[0, 1])
            axes[0, 1].set_title('Score by Question')
            axes[0, 1].set_xlabel('Question Index')
            axes[0, 1].set_ylabel('Score')

        # 3. Top scoring options
        top_scores = df.nlargest(10, 'score')
        if len(top_scores) > 0:
            axes[1, 0].barh(range(len(top_scores)), top_scores['score'])
            axes[1, 0].set_yticks(range(len(top_scores)))
            axes[1, 0].set_yticklabels(
                [f"{row['option_text'][:20]}..." for _, row in top_scores.iterrows()])
            axes[1, 0].set_title('Top 10 Scoring Options')
            axes[1, 0].set_xlabel('Score')

        # 4. Score trends
        df_sorted = df.sort_values('timestamp')
        axes[1, 1].plot(range(len(df_sorted)),
                        df_sorted['score'], marker='o', alpha=0.7)
        axes[1, 1].set_title('Score Trends Over Test Sequence')
        axes[1, 1].set_xlabel('Test Number')
        axes[1, 1].set_ylabel('Score')

        plt.tight_layout()
        plt.savefig('express_entry_analysis.png', dpi=300, bbox_inches='tight')
        logger.info("Visualization saved as 'express_entry_analysis.png'")
        plt.show()

    def run_analysis(self):
        """Run the complete analysis"""
        try:
            # Load the calculator
            if not self.load_calculator():
                return

            # Analyze form structure
            questions = self.analyze_form_structure()
            if not questions:
                logger.error("Could not analyze form structure")
                return

            # Print found questions
            logger.info("Found questions:")
            for i, q in enumerate(questions):
                logger.info(
                    f"{i+1}. {q['text'][:100]}... ({len(q['options'])} options)")

            # Test combinations
            self.test_combinations(questions)

            # Save results
            self.save_results()

            # Create visualizations
            self.create_visualizations()

            # Print summary
            if self.results:
                df = pd.DataFrame(self.results)
                logger.info(f"\nAnalysis Summary:")
                logger.info(f"Total tests: {len(self.results)}")
                logger.info(
                    f"Score range: {df['score'].min()} - {df['score'].max()}")
                logger.info(f"Average score: {df['score'].mean():.1f}")

        except Exception as e:
            logger.error(f"Error during analysis: {e}")
        finally:
            self.close()

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    # Run the analysis
    scraper = ExpressEntryScoreScraper(
        headless=False)  # Set to False to see browser
    scraper.run_analysis()
