#!/usr/bin/env python3
"""
Express Entry Analysis Summary
Shows a summary of all available tools and quick access
"""

import os
import sys


def print_banner():
    print("\n" + "🍁" * 30)
    print("🍁 EXPRESS ENTRY SCORE ANALYZER 🍁")
    print("🍁" + " " * 28 + "🍁")
    print("🍁    Complete CRS Analysis Suite    🍁")
    print("🍁" * 30)


def check_files():
    """Check which analysis files exist"""
    files_to_check = [
        ('comprehensive_crs_analysis.png', 'Main visualization dashboard'),
        ('age_impact_analysis.csv', 'Age scoring analysis data'),
        ('education_impact_analysis.csv', 'Education comparison data'),
        ('language_impact_analysis.csv', 'Language proficiency data'),
        ('optimal_combinations.csv', 'Best scoring combinations'),
        ('analysis_log.txt', 'Execution logs')
    ]

    print("\n📋 Generated Files Status:")
    print("-" * 40)

    for filename, description in files_to_check:
        if os.path.exists(filename):
            print(f"✅ {filename} - {description}")
        else:
            print(f"❌ {filename} - {description}")

    print()


def show_tools():
    """Show available tools"""
    tools = [
        {
            'name': '🎯 Personal Score Calculator',
            'file': 'calculate_score.py',
            'description': 'Interactive calculator for your personal CRS score',
            'command': 'python calculate_score.py'
        },
        {
            'name': '📊 Comprehensive Analysis',
            'file': 'comprehensive_analyzer.py',
            'description': 'Complete analysis of all CRS factors with visualizations',
            'command': 'python comprehensive_analyzer.py'
        },
        {
            'name': '👴 Age Impact Analysis',
            'file': 'age_analyzer.py',
            'description': 'Focused analysis of how age affects scores',
            'command': 'python age_analyzer.py'
        },
        {
            'name': '🌐 Web Scraper',
            'file': 'express_entry_scraper.py',
            'description': 'Experimental tool to scrape official calculator',
            'command': 'python express_entry_scraper.py'
        },
        {
            'name': '🚀 All-in-One Runner',
            'file': 'run_analysis.py',
            'description': 'Interactive menu to run any analysis',
            'command': 'python run_analysis.py'
        }
    ]

    print("🛠️  Available Tools:")
    print("=" * 50)

    for i, tool in enumerate(tools, 1):
        print(f"\n{i}. {tool['name']}")
        print(f"   📄 File: {tool['file']}")
        print(f"   📝 {tool['description']}")
        print(f"   ▶️  Run: {tool['command']}")

        # Check if file exists
        if os.path.exists(tool['file']):
            print(f"   ✅ Ready to use")
        else:
            print(f"   ❌ File not found")


def show_key_insights():
    """Show key insights from analysis"""
    print("\n🔍 Key Insights from Express Entry Analysis:")
    print("=" * 50)

    insights = [
        "🎂 Age Factor: Maximum 110 points until age 29, then declining",
        "🎓 Education: Doctoral (150pts) > Master's (135pts) > Bachelor's (120pts)",
        "🗣️  Language: CLB 10+ gives 136 points, focus on this first",
        "💼 Work Experience: 5+ years gives maximum 80 points",
        "🔄 Skill Transferability: Up to 100 bonus points for combinations",
        "🏆 Maximum Score: 576 points (perfect profile)",
        "📈 Competitive Range: 470-500+ points typically invited",
        "⏰ Timing Matters: Apply before major age milestones (30, 35, 40)"
    ]

    for insight in insights:
        print(f"  {insight}")


def quick_recommendations():
    """Show quick improvement recommendations"""
    print("\n💡 Quick Improvement Strategies:")
    print("=" * 50)

    recommendations = [
        "1. 🎯 Language First: Highest ROI - aim for CLB 9+ in all skills",
        "2. ⏰ Age Timing: Don't delay if you're approaching 30, 35, or 40",
        "3. 🎓 Education ROI: Master's degree worth it if under 30",
        "4. 💼 Experience Balance: Gain experience but don't delay too long",
        "5. 🌍 Foreign Experience: Can add significant transferability points",
        "6. 🔄 Combination Strategy: Optimize education + language + experience"
    ]

    for rec in recommendations:
        print(f"  {rec}")


def main():
    print_banner()

    if len(sys.argv) > 1:
        if sys.argv[1] == '--calc':
            os.system('python calculate_score.py')
            return
        elif sys.argv[1] == '--analyze':
            os.system('python comprehensive_analyzer.py')
            return
        elif sys.argv[1] == '--run':
            os.system('python run_analysis.py')
            return

    # Show current status
    check_files()

    # Show available tools
    show_tools()

    # Show insights
    show_key_insights()

    # Show recommendations
    quick_recommendations()

    print("\n🚀 Quick Start Commands:")
    print("-" * 30)
    print("📱 Personal calculator:     python summary.py --calc")
    print("📊 Full analysis:          python summary.py --analyze")
    print("🎛️  Interactive menu:       python summary.py --run")
    print("📖 This summary:           python summary.py")

    print("\n📚 More Information:")
    print("-" * 30)
    print("📄 README.md - Complete documentation")
    print("📋 requirements.txt - Dependencies list")
    print("🌐 Official tool: canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/check-score.html")

    print("\n" + "🍁" * 30)


if __name__ == "__main__":
    main()
