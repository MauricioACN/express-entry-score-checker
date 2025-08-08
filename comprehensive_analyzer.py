#!/usr/bin/env python3
"""
Express Entry Comprehensive Score Analysis
Analyzes multiple factors affecting CRS scores based on official scoring criteria
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComprehensiveScoreAnalyzer:
    def __init__(self):
        """Initialize the comprehensive analyzer"""
        self.results = []
        self.setup_scoring_rules()

    def setup_scoring_rules(self):
        """Define the CRS scoring rules based on official criteria"""

        # Age scoring (without spouse)
        self.age_scores = {
            range(18, 30): 110,
            range(30, 32): 105,
            range(32, 33): 100,
            range(33, 34): 95,
            range(34, 35): 90,
            range(35, 36): 85,
            range(36, 37): 80,
            range(37, 38): 75,
            range(38, 39): 70,
            range(39, 40): 65,
            range(40, 41): 60,
            range(41, 42): 55,
            range(42, 43): 50,
            range(43, 44): 45,
            range(44, 45): 35,
            range(45, 47): 25,
        }

        # Education scoring
        self.education_scores = {
            'no_education': 0,
            'secondary': 30,
            'one_year_postsecondary': 90,
            'two_year_postsecondary': 98,
            'bachelor_3year': 112,
            'two_or_more_certificates': 119,
            'bachelor_4year': 120,
            'master_degree': 135,
            'professional_degree': 135,
            'doctoral_degree': 150
        }

        # Language scoring (first official language)
        self.language_scores = {
            'clb_10_plus': {'speaking': 34, 'listening': 34, 'reading': 34, 'writing': 34},
            'clb_9': {'speaking': 31, 'listening': 31, 'reading': 31, 'writing': 31},
            'clb_8': {'speaking': 23, 'listening': 23, 'reading': 23, 'writing': 23},
            'clb_7': {'speaking': 16, 'listening': 16, 'reading': 16, 'writing': 16},
            'clb_6': {'speaking': 8, 'listening': 8, 'reading': 8, 'writing': 8},
            'clb_5': {'speaking': 6, 'listening': 6, 'reading': 6, 'writing': 6},
            'clb_4_below': {'speaking': 0, 'listening': 0, 'reading': 0, 'writing': 0}
        }

        # Work experience scoring
        self.work_experience_scores = {
            '0_years': 0,
            '1_year': 40,
            '2_years': 53,
            '3_years': 64,
            '4_years': 72,
            '5_years': 80,
            '6_plus_years': 80
        }

        # Skill transferability factors (combinations of education, language, and work experience)
        self.skill_transferability = {
            'education_language': {
                ('bachelor_plus', 'clb_7_plus'): 13,
                ('bachelor_plus', 'clb_9_plus'): 25,
                ('master_plus', 'clb_7_plus'): 25,
                ('master_plus', 'clb_9_plus'): 50
            },
            'education_experience': {
                ('bachelor_plus', '1_year_plus'): 13,
                ('bachelor_plus', '3_year_plus'): 25,
                ('master_plus', '1_year_plus'): 25,
                ('master_plus', '3_year_plus'): 50
            },
            'foreign_experience': {
                ('1_year', 'clb_7_plus'): 13,
                ('2_year_plus', 'clb_7_plus'): 25,
                ('1_year', 'clb_9_plus'): 25,
                ('2_year_plus', 'clb_9_plus'): 50
            }
        }

    def get_age_score(self, age):
        """Get CRS score for a given age"""
        for age_range, score in self.age_scores.items():
            if age in age_range:
                return score
        return 0

    def get_language_score(self, level):
        """Get total language score for a given CLB level"""
        if level in self.language_scores:
            lang_scores = self.language_scores[level]
            return sum(lang_scores.values())
        return 0

    def calculate_skill_transferability(self, education, language, work_exp, foreign_exp):
        """Calculate skill transferability points"""
        total_points = 0

        # Education + Language
        edu_level = 'bachelor_plus' if education in [
            'bachelor_3year', 'bachelor_4year', 'master_degree', 'professional_degree', 'doctoral_degree'] else 'other'
        edu_level = 'master_plus' if education in [
            'master_degree', 'professional_degree', 'doctoral_degree'] else edu_level

        lang_level = 'clb_9_plus' if language in [
            'clb_9', 'clb_10_plus'] else 'clb_7_plus' if language in ['clb_7', 'clb_8'] else 'other'

        key = (edu_level, lang_level)
        if key in self.skill_transferability['education_language']:
            total_points += self.skill_transferability['education_language'][key]

        # Education + Work Experience
        exp_level = '3_year_plus' if work_exp in [
            '3_years', '4_years', '5_years', '6_plus_years'] else '1_year_plus' if work_exp != '0_years' else 'none'

        key = (edu_level, exp_level)
        if key in self.skill_transferability['education_experience']:
            total_points += self.skill_transferability['education_experience'][key]

        # Foreign Experience + Language
        foreign_level = '2_year_plus' if foreign_exp in [
            '2_years', '3_years', '4_years', '5_years', '6_plus_years'] else '1_year' if foreign_exp == '1_year' else 'none'

        key = (foreign_level, lang_level)
        if key in self.skill_transferability['foreign_experience']:
            total_points += self.skill_transferability['foreign_experience'][key]

        # Maximum 100 points for skill transferability
        return min(total_points, 100)

    def calculate_total_score(self, age, education, language, work_exp, foreign_exp=0):
        """Calculate total CRS score for given parameters"""
        score = 0

        # Core factors
        score += self.get_age_score(age)
        score += self.education_scores.get(education, 0)
        score += self.get_language_score(language)
        score += self.work_experience_scores.get(work_exp, 0)

        # Skill transferability
        score += self.calculate_skill_transferability(
            education, language, work_exp, str(foreign_exp) + '_years')

        return score

    def analyze_age_impact(self):
        """Analyze how age affects scores across different profiles"""
        logger.info("Analyzing age impact...")

        # Test different age scenarios with various profiles
        profiles = [
            {
                'name': 'High Education + High Language',
                'education': 'master_degree',
                'language': 'clb_10_plus',
                'work_exp': '3_years',
                'foreign_exp': 2
            },
            {
                'name': 'Bachelor + Good Language',
                'education': 'bachelor_4year',
                'language': 'clb_8',
                'work_exp': '2_years',
                'foreign_exp': 1
            },
            {
                'name': 'Average Profile',
                'education': 'bachelor_3year',
                'language': 'clb_7',
                'work_exp': '1_year',
                'foreign_exp': 0
            }
        ]

        age_analysis = []

        for age in range(18, 46):
            for profile in profiles:
                score = self.calculate_total_score(
                    age=age,
                    education=profile['education'],
                    language=profile['language'],
                    work_exp=profile['work_exp'],
                    foreign_exp=profile['foreign_exp']
                )

                age_analysis.append({
                    'age': age,
                    'profile': profile['name'],
                    'score': score,
                    'education': profile['education'],
                    'language': profile['language'],
                    'work_exp': profile['work_exp']
                })

        return pd.DataFrame(age_analysis)

    def analyze_education_impact(self):
        """Analyze how education affects scores"""
        logger.info("Analyzing education impact...")

        education_analysis = []

        # Fixed parameters for comparison
        fixed_params = {
            'age': 28,  # Optimal age
            'language': 'clb_8',
            'work_exp': '2_years',
            'foreign_exp': 1
        }

        for education in self.education_scores.keys():
            score = self.calculate_total_score(
                education=education,
                **fixed_params
            )

            education_analysis.append({
                'education': education,
                'education_points': self.education_scores[education],
                'total_score': score,
                'education_label': education.replace('_', ' ').title()
            })

        return pd.DataFrame(education_analysis)

    def analyze_language_impact(self):
        """Analyze how language proficiency affects scores"""
        logger.info("Analyzing language impact...")

        language_analysis = []

        # Fixed parameters for comparison
        fixed_params = {
            'age': 28,
            'education': 'bachelor_4year',
            'work_exp': '2_years',
            'foreign_exp': 1
        }

        for language in self.language_scores.keys():
            score = self.calculate_total_score(
                language=language,
                **fixed_params
            )

            language_analysis.append({
                'language': language,
                'language_points': self.get_language_score(language),
                'total_score': score,
                'language_label': language.replace('_', ' ').upper()
            })

        return pd.DataFrame(language_analysis)

    def find_optimal_combinations(self):
        """Find the highest scoring combinations"""
        logger.info("Finding optimal combinations...")

        # Test combinations for people aged 25-35 (prime age range)
        combinations = []

        age_range = range(25, 36)
        education_options = ['bachelor_4year',
                             'master_degree', 'doctoral_degree']
        language_options = ['clb_8', 'clb_9', 'clb_10_plus']
        work_options = ['2_years', '3_years', '4_years', '5_years']

        for age, education, language, work_exp in itertools.product(
            age_range, education_options, language_options, work_options
        ):
            score = self.calculate_total_score(
                age, education, language, work_exp, 2)

            combinations.append({
                'age': age,
                'education': education,
                'language': language,
                'work_exp': work_exp,
                'total_score': score
            })

        df = pd.DataFrame(combinations)
        return df.nlargest(20, 'total_score')

    def create_comprehensive_visualizations(self, age_df, education_df, language_df, optimal_df):
        """Create comprehensive visualizations"""
        logger.info("Creating visualizations...")

        plt.style.use('default')
        fig = plt.figure(figsize=(20, 15))

        # 1. Age impact by profile
        plt.subplot(3, 3, 1)
        for profile in age_df['profile'].unique():
            profile_data = age_df[age_df['profile'] == profile]
            plt.plot(profile_data['age'], profile_data['score'],
                     marker='o', label=profile, linewidth=2)
        plt.title('Score by Age Across Different Profiles')
        plt.xlabel('Age')
        plt.ylabel('CRS Score')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # 2. Education impact
        plt.subplot(3, 3, 2)
        education_sorted = education_df.sort_values('total_score')
        plt.barh(range(len(education_sorted)),
                 education_sorted['total_score'], color='skyblue')
        plt.yticks(range(len(education_sorted)),
                   education_sorted['education_label'])
        plt.title('Total Score by Education Level')
        plt.xlabel('CRS Score')

        # 3. Language impact
        plt.subplot(3, 3, 3)
        language_sorted = language_df.sort_values('total_score')
        plt.bar(range(len(language_sorted)),
                language_sorted['total_score'], color='lightcoral')
        plt.xticks(range(len(language_sorted)),
                   language_sorted['language_label'], rotation=45)
        plt.title('Total Score by Language Level')
        plt.ylabel('CRS Score')

        # 4. Score distribution by age groups
        plt.subplot(3, 3, 4)
        age_df['age_group'] = pd.cut(age_df['age'], bins=[17, 25, 30, 35, 40, 46],
                                     labels=['18-25', '26-30', '31-35', '36-40', '41-45'])
        age_df.boxplot(column='score', by='age_group', ax=plt.gca())
        plt.title('Score Distribution by Age Group')
        plt.suptitle('')  # Remove automatic title

        # 5. Top 10 combinations
        plt.subplot(3, 3, 5)
        top_10 = optimal_df.head(10)
        plt.barh(range(len(top_10)), top_10['total_score'], color='gold')
        labels = [
            f"Age {row['age']}, {row['education'][:8]}" for _, row in top_10.iterrows()]
        plt.yticks(range(len(top_10)), labels)
        plt.title('Top 10 Score Combinations')
        plt.xlabel('CRS Score')

        # 6. Education vs Language heatmap
        plt.subplot(3, 3, 6)
        pivot_data = []
        for edu in ['bachelor_3year', 'bachelor_4year', 'master_degree', 'doctoral_degree']:
            for lang in ['clb_7', 'clb_8', 'clb_9', 'clb_10_plus']:
                score = self.calculate_total_score(28, edu, lang, '3_years', 2)
                pivot_data.append(
                    {'education': edu, 'language': lang, 'score': score})

        pivot_df = pd.DataFrame(pivot_data)
        heatmap_data = pivot_df.pivot(
            index='education', columns='language', values='score')
        sns.heatmap(heatmap_data, annot=True, fmt='d',
                    cmap='YlOrRd', ax=plt.gca())
        plt.title('Score Heatmap: Education vs Language')

        # 7. Work experience impact
        plt.subplot(3, 3, 7)
        work_scores = []
        for work_exp in self.work_experience_scores.keys():
            score = self.calculate_total_score(
                28, 'bachelor_4year', 'clb_8', work_exp, 1)
            work_scores.append({'work_exp': work_exp, 'score': score})

        work_df = pd.DataFrame(work_scores)
        plt.plot(work_df['work_exp'], work_df['score'],
                 marker='o', linewidth=2, markersize=8)
        plt.title('Score by Work Experience')
        plt.xlabel('Work Experience')
        plt.ylabel('CRS Score')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)

        # 8. Score component breakdown for optimal profile
        plt.subplot(3, 3, 8)
        optimal_profile = optimal_df.iloc[0]
        components = {
            'Age': self.get_age_score(optimal_profile['age']),
            'Education': self.education_scores[optimal_profile['education']],
            'Language': self.get_language_score(optimal_profile['language']),
            'Work Exp': self.work_experience_scores[optimal_profile['work_exp']],
            'Transferability': self.calculate_skill_transferability(
                optimal_profile['education'], optimal_profile['language'],
                optimal_profile['work_exp'], '2_years'
            )
        }

        plt.pie(components.values(), labels=components.keys(),
                autopct='%1.1f%%', startangle=90)
        plt.title(f'Score Breakdown (Total: {optimal_profile["total_score"]})')

        # 9. Age decline rate
        plt.subplot(3, 3, 9)
        high_profile = age_df[age_df['profile']
                              == 'High Education + High Language']
        high_profile = high_profile.sort_values('age')
        decline_rate = high_profile['score'].diff().fillna(0)
        plt.bar(high_profile['age'], -decline_rate, alpha=0.7, color='orange')
        plt.title('Points Lost per Year (High Profile)')
        plt.xlabel('Age')
        plt.ylabel('Points Lost')
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('comprehensive_crs_analysis.png',
                    dpi=300, bbox_inches='tight')
        logger.info(
            "Comprehensive analysis saved as 'comprehensive_crs_analysis.png'")
        plt.show()

    def generate_recommendations(self, age_df, education_df, language_df, optimal_df):
        """Generate actionable recommendations"""
        recommendations = []

        # Age recommendations
        best_age_range = age_df[age_df['score'] ==
                                age_df['score'].max()]['age'].iloc[0]
        recommendations.append(
            f"Optimal age range: Up to {best_age_range} years old for maximum points")

        # Education recommendations
        best_education = education_df.loc[education_df['total_score'].idxmax(
        ), 'education']
        recommendations.append(
            f"Best education level: {best_education.replace('_', ' ').title()}")

        # Language recommendations
        best_language = language_df.loc[language_df['total_score'].idxmax(
        ), 'language']
        recommendations.append(
            f"Target language level: {best_language.replace('_', ' ').upper()}")

        # Score improvement recommendations
        recommendations.extend([
            "Focus on language improvement first - it has the highest impact per point",
            "Consider pursuing higher education if under 30 years old",
            "Gain work experience, but don't delay application too long due to age factor",
            "Consider foreign work experience to boost skill transferability points"
        ])

        return recommendations

    def run_comprehensive_analysis(self):
        """Run the complete comprehensive analysis"""
        try:
            logger.info("Starting comprehensive CRS analysis...")

            # Run all analyses
            age_df = self.analyze_age_impact()
            education_df = self.analyze_education_impact()
            language_df = self.analyze_language_impact()
            optimal_df = self.find_optimal_combinations()

            # Create visualizations
            self.create_comprehensive_visualizations(
                age_df, education_df, language_df, optimal_df)

            # Generate recommendations
            recommendations = self.generate_recommendations(
                age_df, education_df, language_df, optimal_df)

            # Save results
            age_df.to_csv('age_impact_analysis.csv', index=False)
            education_df.to_csv('education_impact_analysis.csv', index=False)
            language_df.to_csv('language_impact_analysis.csv', index=False)
            optimal_df.to_csv('optimal_combinations.csv', index=False)

            # Print summary
            logger.info("\n" + "="*60)
            logger.info("EXPRESS ENTRY COMPREHENSIVE ANALYSIS RESULTS")
            logger.info("="*60)

            logger.info(f"\nTop 5 scoring combinations:")
            for i, (_, row) in enumerate(optimal_df.head(5).iterrows(), 1):
                logger.info(f"{i}. Age {row['age']}, {row['education']}, {row['language']}, "
                            f"{row['work_exp']} work exp → {row['total_score']} points")

            logger.info(f"\nKey Insights:")
            for rec in recommendations:
                logger.info(f"• {rec}")

            logger.info(f"\nScore Ranges:")
            logger.info(
                f"Maximum possible score: {optimal_df['total_score'].max()}")
            logger.info(
                f"Average score (good profile): {age_df[age_df['profile'] == 'High Education + High Language']['score'].mean():.1f}")
            logger.info(
                f"Minimum competitive score: ~470-480 (typical cutoff)")

            logger.info(f"\nFiles saved:")
            logger.info("• comprehensive_crs_analysis.png")
            logger.info("• age_impact_analysis.csv")
            logger.info("• education_impact_analysis.csv")
            logger.info("• language_impact_analysis.csv")
            logger.info("• optimal_combinations.csv")

        except Exception as e:
            logger.error(f"Error during comprehensive analysis: {e}")


if __name__ == "__main__":
    analyzer = ComprehensiveScoreAnalyzer()
    analyzer.run_comprehensive_analysis()
