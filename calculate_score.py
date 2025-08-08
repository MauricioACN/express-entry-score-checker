#!/usr/bin/env python3
"""
Express Entry Score Calculator
Quick calculator for individual score estimation
"""

from comprehensive_analyzer import ComprehensiveScoreAnalyzer


def calculate_my_score():
    """Interactive score calculator"""
    print("\n🍁 Express Entry Score Calculator 🍁")
    print("Answer the following questions to estimate your CRS score:")

    # Get age
    while True:
        try:
            age = int(input("\n1. What is your age? "))
            if 18 <= age <= 47:
                break
            else:
                print("Please enter an age between 18 and 47")
        except ValueError:
            print("Please enter a valid number")

    # Get education
    print("\n2. What is your highest education level?")
    education_options = {
        '1': ('secondary', 'High school'),
        '2': ('one_year_postsecondary', 'One-year post-secondary'),
        '3': ('two_year_postsecondary', 'Two-year post-secondary'),
        '4': ('bachelor_3year', 'Bachelor degree (3 years)'),
        '5': ('bachelor_4year', 'Bachelor degree (4+ years)'),
        '6': ('master_degree', 'Master degree'),
        '7': ('professional_degree', 'Professional degree (medicine, law, etc.)'),
        '8': ('doctoral_degree', 'Doctoral degree (PhD)')
    }

    for key, (_, desc) in education_options.items():
        print(f"   {key}. {desc}")

    while True:
        choice = input("Enter your choice (1-8): ").strip()
        if choice in education_options:
            education = education_options[choice][0]
            break
        print("Please enter a valid choice (1-8)")

    # Get language level
    print("\n3. What is your English/French language level (CLB)?")
    language_options = {
        '1': ('clb_4_below', 'CLB 4 or below'),
        '2': ('clb_5', 'CLB 5'),
        '3': ('clb_6', 'CLB 6'),
        '4': ('clb_7', 'CLB 7'),
        '5': ('clb_8', 'CLB 8'),
        '6': ('clb_9', 'CLB 9'),
        '7': ('clb_10_plus', 'CLB 10+')
    }

    for key, (_, desc) in language_options.items():
        print(f"   {key}. {desc}")

    while True:
        choice = input("Enter your choice (1-7): ").strip()
        if choice in language_options:
            language = language_options[choice][0]
            break
        print("Please enter a valid choice (1-7)")

    # Get work experience
    print("\n4. How many years of work experience do you have?")
    work_options = {
        '1': ('0_years', 'No work experience'),
        '2': ('1_year', '1 year'),
        '3': ('2_years', '2 years'),
        '4': ('3_years', '3 years'),
        '5': ('4_years', '4 years'),
        '6': ('5_years', '5 years'),
        '7': ('6_plus_years', '6+ years')
    }

    for key, (_, desc) in work_options.items():
        print(f"   {key}. {desc}")

    while True:
        choice = input("Enter your choice (1-7): ").strip()
        if choice in work_options:
            work_exp = work_options[choice][0]
            break
        print("Please enter a valid choice (1-7)")

    # Get foreign work experience
    while True:
        try:
            foreign_exp = int(
                input("\n5. How many years of foreign work experience do you have? "))
            if 0 <= foreign_exp <= 10:
                break
            else:
                print("Please enter a number between 0 and 10")
        except ValueError:
            print("Please enter a valid number")

    # Calculate score
    analyzer = ComprehensiveScoreAnalyzer()
    total_score = analyzer.calculate_total_score(
        age, education, language, work_exp, foreign_exp)

    # Get component breakdown
    age_points = analyzer.get_age_score(age)
    education_points = analyzer.education_scores.get(education, 0)
    language_points = analyzer.get_language_score(language)
    work_points = analyzer.work_experience_scores.get(work_exp, 0)
    transferability_points = analyzer.calculate_skill_transferability(
        education, language, work_exp, str(foreign_exp) + '_years'
    )

    # Display results
    print("\n" + "="*50)
    print("🎯 YOUR CRS SCORE BREAKDOWN")
    print("="*50)
    print(f"Age ({age} years old): {age_points} points")
    print(f"Education: {education_points} points")
    print(f"Language: {language_points} points")
    print(f"Work Experience: {work_points} points")
    print(f"Skill Transferability: {transferability_points} points")
    print("-" * 30)
    print(f"TOTAL CRS SCORE: {total_score} points")
    print("="*50)

    # Provide recommendations
    print("\n💡 RECOMMENDATIONS:")

    if total_score >= 500:
        print("✅ Excellent score! You're very competitive for Express Entry")
    elif total_score >= 470:
        print("✅ Good score! You have a good chance in Express Entry draws")
    elif total_score >= 430:
        print("⚠️  Moderate score. Consider improvements to be more competitive")
    else:
        print("❌ Low score. Significant improvements needed to be competitive")

    # Specific recommendations
    if language_points < 120:  # Not CLB 9+
        print("🔥 Priority: Improve language skills to CLB 9+ for maximum points")

    if age >= 30:
        print("⏰ Consider applying soon due to age factor")

    if education_points < 120:  # Less than bachelor's
        print("📚 Consider higher education for more points")

    if transferability_points < 50:
        print("🔄 Work on skill transferability combinations")

    print(f"\n📊 Recent draw cutoffs typically range from 470-500 points")
    print(
        f"📈 Your score puts you {'above' if total_score >= 470 else 'below'} typical cutoffs")


if __name__ == "__main__":
    calculate_my_score()
