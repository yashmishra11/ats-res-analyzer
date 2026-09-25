"""
Visualization utilities for ATS Resume Analyzer
Creates charts and graphs for analysis results
"""

import matplotlib.pyplot as plt
from config import STATUS_SCORES, EXPECTED_SCORES_AFTER_FIX, SECTION_ORDER, SECTION_LABEL_MAP


def calculate_section_scores(sections_analysis):
    """
    Calculate current and expected scores for each section
    """

    section_scores = {
        'current': [],
        'expected': [],
        'labels': []
    }

    for section_name in SECTION_ORDER:
        section = next((s for s in sections_analysis if s['title'] == section_name), None)

        if not section:
            continue

        label = SECTION_LABEL_MAP.get(section_name, section_name)

        # 🔹 Dynamic scoring
        if section_name == "Projects":
            project_count = section.get("project_count", 0)
            tech_ratio = section.get("relevant_project_ratio", 0)

            score = round(min(95, 50 + (project_count * 10) + (tech_ratio * 30)))

        elif section_name == "Skills & Technologies":
            ratio = section.get("match_ratio", 0)
            score = round(min(95, 40 + (ratio * 55)))

        else:
            status = section['status']
            if status == "missing":
                score = 45
            elif status == "weak":
                score = 65
            else:
                score = 90

        # Expected improvement boost - ONLY for sections that need work
        status = section.get('status', 'good')
        if status == "missing":
            # Missing sections can improve significantly
            expected_score = round(min(95, score + 20))
        elif status == "weak":
            # Weak sections can improve moderately
            expected_score = round(min(95, score + 15))
        else:
            # Good sections stay the same (no improvement needed)
            expected_score = score

        section_scores['labels'].append(label)
        section_scores['current'].append(score)
        section_scores['expected'].append(expected_score)

    return section_scores



def create_section_impact_chart(sections_analysis):
    """
    Create section-by-section impact analysis chart with Cyberpunk HUD aesthetic
    
    Args:
        sections_analysis (list): List of section analysis dictionaries
        
    Returns:
        matplotlib.figure.Figure: The created figure
    """
    section_scores = calculate_section_scores(sections_analysis)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#0a0a0f')
    
    x_positions = list(range(len(section_scores['labels'])))
    
    # Current score line (Neon Cyan - #00d4ff)
    ax.plot(
        x_positions, section_scores['current'], 
        marker='D', markersize=7, linewidth=2.8, 
        color='#00d4ff', label='CURRENT TELEMETRY', alpha=0.9
    )
    
    # Expected score line (Electric Green - #00ff88)
    ax.plot(
        x_positions, section_scores['expected'], 
        marker='s', markersize=7, linewidth=2.8, 
        color='#00ff88', label='OPTIMIZED TRAJECTORY', alpha=0.95
    )
    
    # Fill area between lines (Cyber neon delta zone)
    ax.fill_between(
        x_positions, section_scores['current'], section_scores['expected'], 
        alpha=0.18, color='#00ff88'
    )
    
    # Customize technical axes
    ax.set_xticks(x_positions)
    ax.set_xticklabels(
        section_scores['labels'], rotation=0, ha='center', 
        fontsize=9, color='#00d4ff', fontweight='bold'
    )
    ax.set_ylim(35, 102)
    ax.set_ylabel('SCORE COEFFICIENT (%)', color='#6b7280', fontsize=10)
    ax.set_xlabel('RESUME SECTORS // ANALYSIS CHANNELS', color='#6b7280', fontsize=10)
    ax.tick_params(colors='#6b7280', labelsize=9)
    ax.grid(axis='y', alpha=0.25, color='#2a2a3a', linestyle='--')
    ax.grid(axis='x', alpha=0.15, color='#2a2a3a', linestyle=':')
    
    # Style HUD spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#2a2a3a')
    ax.spines['bottom'].set_color('#2a2a3a')
    
    # Cyberpunk Legend
    legend = ax.legend(
        loc='lower right', framealpha=0.85, facecolor='#12121a', 
        edgecolor='#00ff88', fontsize=9, labelcolor='#e0e0e0'
    )
    legend.get_frame().set_linewidth(1.2)
    
    # Add neon values on points
    for i, (curr, exp) in enumerate(zip(section_scores['current'], section_scores['expected'])):
        ax.text(
            i, curr - 3.5, f'{int(curr)}%', ha='center', va='top', 
            fontsize=8.5, color='#00d4ff', weight='bold'
        )
        if exp != curr:
            ax.text(
                i, exp + 2.5, f'{int(exp)}%', ha='center', va='bottom', 
                fontsize=8.5, color='#00ff88', weight='bold'
            )
    
    plt.tight_layout()
    return fig