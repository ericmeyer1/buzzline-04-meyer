# Buzzline Project - Gospel Message Analysis
## Project Overview
This project analyzes streaming JSON messages to detect and visualize gospel content and evangelistic opportunities. Inspired by bold Christian leaders like Charlie Kirk, it encourages believers to be intentional and outspoken in sharing their faith through digital communications.

---

## Gospel Message Analyzer Consumer
What It Does
The Gospel Message Analyzer processes real-time JSON messages to:

Detect Gospel Content: Scans for Christian keywords (salvation, Jesus, faith, scripture, grace, witness, truth, eternity)
Measure Bold Witness: Identifies high-impact gospel messages with positive sentiment
Find Evangelistic Opportunities: Detects messages expressing struggle, seeking, or spiritual questions
Track Ministry Effectiveness: Provides real-time metrics on gospel sharing success
Encourage Boldness: Biblical inspiration and challenges to share Christ more intentionally

Insight Focus
Gospel Message Analysis and Digital Evangelism Effectiveness
"Therefore go and make disciples of all nations..." - Matthew 28:19
This analysis helps believers understand their digital witness impact, identify missed opportunities for gospel conversations, and encourages more intentional Christian testimony online.

---

## Visualization Types

Line Charts: Gospel content scores and faith impact trends over time
Bar Charts: Top gospel keywords, ministry impact metrics, evangelistic effectiveness percentages
Real-time Dashboard: Live statistics with biblical inspiration and bold witness challenges

Why This is Interesting: Shows both immediate gospel opportunities and long-term evangelistic effectiveness, helping believers become more strategic and bold in their digital witness like Charlie Kirk and other outspoken Christian leaders.
Required Project Setup
Environment Setup
bash# Create and activate virtual environment
python -m venv .venv

---

## Windows
.venv\Scripts\activate

## Linux/Mac
source .venv/bin/activate

## Install required packages
pip install -r requirements.txt

---

## Running the Project

Step 1: Start the Required Producer

The project uses the provided producer without any modifications:
bash# Run the basic JSON producer (generates sample messages)
python -m producers.basic_json_producer_case
This will start generating JSON messages to the data/buzz_live.json file with the format:
json{
    "message": "I just shared a movie! It was amazing.",
    "author": "Charlie",
    "timestamp": "2025-01-29 14:35:20",
    "category": "humor",
    "sentiment": 0.87,
    "keyword_mentioned": "movie",
    "message_length": 42
}

Step 2: Run a Consumer

Option A: Original Basic Consumer (Provided Example)
To run the original basic consumer that counts messages by author:
bash# In a new terminal window (keep producer running)
python -m consumers.basic_json_consumer_case
This will display a live bar chart showing message counts by author.

Option B: New Gospel Message Analyzer Consumer
To run the new gospel-focused consumer:
bash# In a new terminal window (keep producer running)
python -m consumers.project_consumer_gospel
Then open your browser and navigate to:

Dashboard: gospel_dashboard.html (auto-refreshes every 3 seconds)
Charts: Will be saved in charts/gospel_analysis.png

Expected Output
Console Output
🔥 Starting Gospel Message Analyzer Consumer
💪 Inspired by bold faith leaders like Charlie Kirk
📖 Monitoring file: data\buzz_live.json
✝️ Open gospel_dashboard.html to see live gospel analysis
🚀 Be bold in sharing your faith!
--------------------------------------------------
📖 Message #1 - Gospel Score: 0.40, Impact: 0.35, Author: Charlie
🔥 STRONG GOSPEL MESSAGE detected from Alice!
Dashboard Features

Live Statistics: Total messages, gospel messages, bold witness count, evangelistic opportunities
Visual Charts: Real-time gospel content analysis with biblical themes
Encouragement: Scripture verses and challenges to be bold in faith
Ministry Metrics: Effectiveness percentages and trending analysis

message: Text content analyzed for gospel keywords
author: Tracks who is sharing gospel content
sentiment: Combined with gospel score for faith impact calculation
timestamp: Used for time-series analysis

Special Data Structures

Gospel Keywords Dictionary: 8 categories with related terms
Time Series Deques: Gospel scores and faith impact over time
Author Set: Tracks unique individuals sharing gospel content
Keyword Counters: Frequency analysis of Christian terms

Processing Logic

Gospel Score Calculation: Analyzes message for Christian keywords (0-1 scale)
Faith Impact Measurement: Combines gospel content with positive sentiment
Evangelistic Opportunity Detection: Identifies struggles, questions, or spiritual seeking
Bold Witness Tracking: High gospel score + positive sentiment (Charlie Kirk style)

Biblical Foundation
"How beautiful are the feet of those who bring good news!" - Romans 10:15
"For I am not ashamed of the gospel, because it is the power of God that brings salvation to everyone who believes." - Romans 1:16
This tool encourages believers to be intentional, strategic, and bold in sharing Christ through digital communications.
Troubleshooting
Common Issues

No charts appearing: Make sure you have matplotlib installed and are opening the HTML dashboard
File not found errors: Ensure the producer is running first to create the data file
Import errors: Verify all packages are installed with pip install -r requirements.txt

Platform-Specific Notes

Windows: Use python -m commands as shown
WSL/Linux: May need python3 instead of python
Chart Display: Dashboard works in any web browser; no special setup needed

Be Bold Challenge
Use this tool to challenge yourself and your community to be more like Charlie Kirk and other bold Christian leaders - unashamed, intentional, and effective in sharing the gospel in every digital conversation!

"And he said to them, 'Go into all the world and proclaim the gospel to the whole creation.'" - Mark 16:15