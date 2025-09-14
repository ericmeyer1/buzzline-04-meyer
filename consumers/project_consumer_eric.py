"""
project_consumer_eric.py

Gospel Message Analyzer Consumer for P4 Project
Analyzes streaming JSON messages for Christian content and evangelistic opportunities
Inspired by bold faith leaders like Charlie Kirk

Author: Eric Meyer
"""

#####################################
# Import Modules
#####################################

import json
import os
import sys
import time
import pathlib
from datetime import datetime
from collections import defaultdict, deque
import re

# Import Matplotlib for visualization
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for compatibility

# Import logging utility
from utils.utils_logger import logger

#####################################
# Set up Paths - read from the file the producer writes
#####################################

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FILE = DATA_FOLDER.joinpath("project_live.json")  # This matches the producer output

# Create charts directory
CHARTS_FOLDER = PROJECT_ROOT.joinpath("charts")
CHARTS_FOLDER.mkdir(exist_ok=True)

logger.info(f"Project root: {PROJECT_ROOT}")
logger.info(f"Data folder: {DATA_FOLDER}")
logger.info(f"Data file: {DATA_FILE}")
logger.info(f"Charts folder: {CHARTS_FOLDER}")

#####################################
# Gospel Analysis Configuration
#####################################

class GospelAnalyzer:
    def __init__(self, max_points=100):
        self.max_points = max_points
        
        # Gospel keywords inspired by bold Christian witness
        self.gospel_keywords = {
            'salvation': ['salvation', 'saved', 'born again', 'redeemed', 'forgiven'],
            'jesus': ['jesus', 'christ', 'lord', 'savior', 'messiah', 'god'],
            'faith': ['faith', 'believe', 'trust', 'christian', 'prayer'],
            'scripture': ['bible', 'scripture', 'word', 'psalm', 'verse', 'biblical'],
            'grace': ['grace', 'mercy', 'forgiveness', 'love', 'blessed'],
            'witness': ['testimony', 'witness', 'share', 'proclaim', 'preach'],
            'truth': ['truth', 'righteousness', 'holy', 'pure', 'righteous'],
            'eternity': ['heaven', 'eternal', 'soul', 'spirit', 'heavenly']
        }
        
        # Data structures for tracking gospel impact
        self.timestamps = deque(maxlen=max_points)
        self.gospel_scores = deque(maxlen=max_points)
        self.faith_impact = deque(maxlen=max_points)
        
        # Statistics tracking
        self.total_messages = 0
        self.gospel_messages = 0
        self.high_impact_messages = 0
        self.keyword_counts = defaultdict(int)
        self.authors_sharing_gospel = set()
        self.category_gospel_counts = defaultdict(int)
        
        # Charlie Kirk inspired metrics
        self.bold_witness_count = 0
        self.evangelistic_opportunities = 0

    def calculate_gospel_score(self, message_text):
        """Calculate how gospel-focused a message is (0-1 scale)"""
        if not message_text:
            return 0
            
        message_lower = message_text.lower()
        total_keywords = 0
        found_categories = 0
        
        for category, keywords in self.gospel_keywords.items():
            category_found = False
            for keyword in keywords:
                if keyword in message_lower:
                    total_keywords += 1
                    self.keyword_counts[keyword] += 1
                    if not category_found:
                        found_categories += 1
                        category_found = True
        
        # Score based on keyword density and category diversity
        base_score = min(total_keywords * 0.2, 1.0)
        diversity_bonus = found_categories * 0.1
        
        return min(base_score + diversity_bonus, 1.0)

    def calculate_faith_impact(self, gospel_score, sentiment):
        """Calculate overall faith impact (Charlie Kirk style boldness)"""
        return gospel_score * max(sentiment, 0.3)

    def is_evangelistic_opportunity(self, message_data):
        """Detect messages that create opportunities for gospel sharing"""
        message = message_data.get('message', '').lower()
        sentiment = float(message_data.get('sentiment', 0))
        
        opportunity_phrases = [
            'what is the point', 'feeling lost', 'need hope', 'struggling',
            'what happens when', 'life is hard', 'need help', 'depressed',
            'lonely', 'purpose', 'meaning', 'why am i here', 'amazing', 'boring'
        ]
        
        for phrase in opportunity_phrases:
            if phrase in message:
                return True
                
        return sentiment < -0.1 or sentiment > 0.8  # Very negative or very positive

#####################################
# Global Gospel Analyzer Instance
#####################################

gospel_analyzer = GospelAnalyzer()

#####################################
# Chart Update Function
#####################################

def update_chart():
    """Create comprehensive gospel analysis charts"""
    if len(gospel_analyzer.gospel_scores) < 2:
        return
        
    try:
        fig = plt.figure(figsize=(16, 12))
        
        # Chart 1: Gospel Score Over Time (top)
        ax1 = plt.subplot(3, 2, (1, 2))
        timestamps = list(gospel_analyzer.timestamps)
        gospel_scores = list(gospel_analyzer.gospel_scores)
        faith_impacts = list(gospel_analyzer.faith_impact)
        
        ax1.plot(timestamps, gospel_scores, 'g-', linewidth=3, marker='o', 
                markersize=5, label='Gospel Content', alpha=0.8)
        ax1.plot(timestamps, faith_impacts, 'b-', linewidth=2, marker='s', 
                markersize=4, label='Faith Impact', alpha=0.8)
        ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, 
                   label='Strong Gospel Threshold')
        
        ax1.set_title('Gospel Message Analysis Over Time (Charlie Kirk Style)', 
                     fontsize=16, fontweight='bold', color='#2c3e50')
        ax1.set_ylabel('Score (0-1)', fontsize=12)
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 1.1)
        
        # Format x-axis for better readability
        if len(timestamps) > 10:
            ax1.set_xticks(timestamps[::max(1, len(timestamps)//5)])
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        
        # Chart 2: Top Gospel Keywords (middle left)
        ax2 = plt.subplot(3, 2, 3)
        if gospel_analyzer.keyword_counts:
            top_keywords = sorted(gospel_analyzer.keyword_counts.items(), 
                                key=lambda x: x[1], reverse=True)[:8]
            if top_keywords:
                keywords, counts = zip(*top_keywords)
                colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', 
                         '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
                bars = ax2.bar(keywords, counts, color=colors[:len(keywords)])
                
                ax2.set_title('Most Mentioned Gospel Keywords', 
                             fontsize=14, fontweight='bold', color='#2c3e50')
                ax2.set_ylabel('Mentions', fontsize=12)
                plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
                
                # Add count labels on bars
                for bar, count in zip(bars, counts):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{count}', ha='center', va='bottom', fontweight='bold')
        
        # Chart 3: Impact Categories (middle right)
        ax3 = plt.subplot(3, 2, 4)
        categories = ['Total\nMessages', 'Gospel\nMessages', 'Bold\nWitness', 'Evangelistic\nOpps']
        counts = [gospel_analyzer.total_messages, gospel_analyzer.gospel_messages, 
                 gospel_analyzer.bold_witness_count, gospel_analyzer.evangelistic_opportunities]
        colors = ['#95a5a6', '#27ae60', '#f1c40f', '#e67e22']
        
        bars = ax3.bar(categories, counts, color=colors)
        ax3.set_title('Ministry Impact Metrics', fontsize=14, fontweight='bold', color='#2c3e50')
        ax3.set_ylabel('Count', fontsize=12)
        
        # Add count labels
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{count}', ha='center', va='bottom', fontweight='bold')
        
        # Chart 4: Gospel Effectiveness (bottom)
        ax4 = plt.subplot(3, 1, 3)
        if gospel_analyzer.total_messages > 0:
            gospel_rate = (gospel_analyzer.gospel_messages / gospel_analyzer.total_messages) * 100
            witness_rate = (gospel_analyzer.bold_witness_count / gospel_analyzer.total_messages) * 100
            opportunity_rate = (gospel_analyzer.evangelistic_opportunities / gospel_analyzer.total_messages) * 100
            
            metrics = ['Gospel Content %', 'Bold Witness %', 'Evangelistic Opps %']
            percentages = [gospel_rate, witness_rate, opportunity_rate]
            colors = ['#27ae60', '#f1c40f', '#e67e22']
            
            bars = ax4.bar(metrics, percentages, color=colors)
            ax4.set_title('Evangelistic Effectiveness - Be Bold Like Charlie Kirk!', 
                         fontsize=16, fontweight='bold', color='#2c3e50')
            ax4.set_ylabel('Percentage', fontsize=12)
            ax4.set_ylim(0, max(100, max(percentages) * 1.2) if percentages else 100)
            
            # Add percentage labels
            for bar, pct in zip(bars, percentages):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        chart_path = CHARTS_FOLDER / "gospel_analysis.png"
        plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        
        logger.info(f"Chart updated and saved to {chart_path}")
        
        # Update dashboard
        create_dashboard()
        
    except Exception as e:
        logger.error(f"Error updating chart: {e}")

def create_dashboard():
    """Create inspiring gospel dashboard"""
    try:
        gospel_rate = (gospel_analyzer.gospel_messages / max(gospel_analyzer.total_messages, 1)) * 100
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Gospel Message Dashboard - Be Bold in Faith!</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body {{ 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 1400px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.95); 
            padding: 30px; 
            border-radius: 15px; 
            color: #2c3e50;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }}
        h1 {{ 
            text-align: center; 
            color: #2c3e50; 
            margin-bottom: 10px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        .verse {{ 
            text-align: center; 
            font-style: italic; 
            color: #7f8c8d; 
            margin-bottom: 20px;
            font-size: 1.2em;
            font-weight: 500;
        }}
        .stats {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin: 30px 0; 
        }}
        .stat {{ 
            padding: 25px 20px; 
            border-radius: 12px; 
            text-align: center; 
            color: white; 
            font-weight: bold;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }}
        .stat:hover {{ transform: translateY(-5px); }}
        .gospel {{ background: linear-gradient(45deg, #27ae60, #2ecc71); }}
        .bold {{ background: linear-gradient(45deg, #f39c12, #e67e22); }}
        .opportunity {{ background: linear-gradient(45deg, #e74c3c, #c0392b); }}
        .authors {{ background: linear-gradient(45deg, #9b59b6, #8e44ad); }}
        .total {{ background: linear-gradient(45deg, #34495e, #2c3e50); }}
        .stat-number {{ font-size: 3em; display: block; margin-bottom: 5px; }}
        .stat-label {{ font-size: 1.1em; }}
        .chart-container {{ text-align: center; margin: 30px 0; }}
        .chart {{ 
            max-width: 100%; 
            border-radius: 15px; 
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }}
        .inspiration {{ 
            background: linear-gradient(45deg, #3498db, #2980b9); 
            color: white; 
            padding: 20px; 
            border-radius: 12px; 
            margin: 25px 0; 
            text-align: center; 
            font-size: 1.3em;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }}
        .footer {{ 
            text-align: center; 
            color: #7f8c8d; 
            margin-top: 30px;
            font-size: 1.1em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Gospel Message Analysis Dashboard</h1>
        <div class="verse">"Therefore go and make disciples of all nations..." - Matthew 28:19</div>
        
        <div class="inspiration">
            <strong>Be Bold Like Charlie Kirk!</strong> Every message is an opportunity to share the Gospel!
        </div>
        
        <div class="stats">
            <div class="stat total">
                <span class="stat-number">{gospel_analyzer.total_messages}</span>
                <span class="stat-label">Total Messages</span>
            </div>
            <div class="stat gospel">
                <span class="stat-number">{gospel_analyzer.gospel_messages}</span>
                <span class="stat-label">Gospel Messages<br>({gospel_rate:.1f}% rate)</span>
            </div>
            <div class="stat bold">
                <span class="stat-number">{gospel_analyzer.bold_witness_count}</span>
                <span class="stat-label">Bold Witness</span>
            </div>
            <div class="stat opportunity">
                <span class="stat-number">{gospel_analyzer.evangelistic_opportunities}</span>
                <span class="stat-label">Evangelistic Opportunities</span>
            </div>
            <div class="stat authors">
                <span class="stat-number">{len(gospel_analyzer.authors_sharing_gospel)}</span>
                <span class="stat-label">Gospel Sharers</span>
            </div>
        </div>
        
        <div class="chart-container">
            <img src="charts/gospel_analysis.png?v={int(time.time())}" class="chart" alt="Gospel Analysis Chart">
        </div>
        
        <div class="inspiration">
            <strong>Keep sharing boldly!</strong> "How beautiful are the feet of those who bring good news!" - Romans 10:15
        </div>
        
        <div class="footer">
            <em>Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')} | 
            Be outspoken in your faith!</em>
        </div>
    </div>
</body>
</html>"""
        
        dashboard_path = PROJECT_ROOT / "gospel_dashboard.html"
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        logger.info(f"Dashboard updated: {dashboard_path}")
        
    except Exception as e:
        logger.error(f"Error creating dashboard: {e}")

#####################################
# Process Message Function
#####################################

def process_message(message: str) -> None:
    """Process a single JSON message and update gospel analysis"""
    try:
        message_dict = json.loads(message)
        logger.info(f"Processed JSON message: {message_dict}")
        
        if isinstance(message_dict, dict):
            # Extract fields
            message_text = message_dict.get('message', '')
            author = message_dict.get('author', 'Unknown')
            sentiment = float(message_dict.get('sentiment', 0))
            category = message_dict.get('category', 'other')
            
            # Calculate gospel metrics
            gospel_score = gospel_analyzer.calculate_gospel_score(message_text)
            faith_impact = gospel_analyzer.calculate_faith_impact(gospel_score, sentiment)
            
            # Update time series data
            current_time = datetime.now()
            gospel_analyzer.timestamps.append(current_time)
            gospel_analyzer.gospel_scores.append(gospel_score)
            gospel_analyzer.faith_impact.append(faith_impact)
            
            # Update statistics
            gospel_analyzer.total_messages += 1
            
            if gospel_score > 0.3:  # Significant gospel content
                gospel_analyzer.gospel_messages += 1
                gospel_analyzer.authors_sharing_gospel.add(author)
                gospel_analyzer.category_gospel_counts[category] += 1
                
            if faith_impact > 0.7:  # Bold witness
                gospel_analyzer.bold_witness_count += 1
                gospel_analyzer.high_impact_messages += 1
                
            if gospel_analyzer.is_evangelistic_opportunity(message_dict):
                gospel_analyzer.evangelistic_opportunities += 1
            
            logger.info(f"Message #{gospel_analyzer.total_messages} - "
                       f"Gospel Score: {gospel_score:.2f}, Impact: {faith_impact:.2f}, "
                       f"Author: {author}")
            
            if gospel_score > 0.5:
                logger.info(f"STRONG GOSPEL MESSAGE detected from {author}!")
            
            # Update chart
            update_chart()
            
        else:
            logger.error(f"Expected a dictionary but got: {type(message_dict)}")
            
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON message: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

#####################################
# Main Function
#####################################

def main() -> None:
    """Main entry point for the gospel consumer"""
    logger.info("START Gospel Message Analyzer Consumer")
    logger.info("Inspired by bold faith leaders like Charlie Kirk")
    logger.info(f"Monitoring file: {DATA_FILE}")
    
    print("Gospel Message Analyzer Consumer Starting...")
    print("Be bold in sharing your faith!")
    print(f"Monitoring file: {DATA_FILE}")
    print("Open gospel_dashboard.html to see live gospel analysis")
    print("Press Ctrl+C to stop")
    print("-" * 60)
    
    # Verify the data file exists
    if not DATA_FILE.exists():
        logger.info(f"Data file {DATA_FILE} does not exist yet. Waiting for producer...")
        print(f"Waiting for data file {DATA_FILE} to be created by producer...")
    
    try:
        last_position = 0
        
        while True:
            if DATA_FILE.exists():
                try:
                    with open(DATA_FILE, "r") as file:
                        # Move to last known position
                        file.seek(last_position)
                        
                        # Read new lines
                        for line in file:
                            line = line.strip()
                            if line:
                                process_message(line)
                        
                        # Update position
                        last_position = file.tell()
                        
                except Exception as e:
                    logger.error(f"Error reading file: {e}")
            else:
                logger.debug("Data file not found, waiting...")
            
            time.sleep(1)  # Check every second
            
    except KeyboardInterrupt:
        logger.info("Gospel Consumer interrupted by user.")
        print(f"\nConsumer stopped. Gospel messages analyzed: {gospel_analyzer.gospel_messages}/{gospel_analyzer.total_messages}")
        print("Keep being bold in your faith!")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Gospel Consumer closed.")

#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()