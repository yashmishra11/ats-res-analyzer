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
    Create section-by-section impact analysis chart with Bauhaus constructivist aesthetic
    
    Args:
        sections_analysis (list): List of section analysis dictionaries
        
    Returns:
        matplotlib.figure.Figure: The created figure
    """
    section_scores = calculate_section_scores(sections_analysis)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#F0F0F0')
    ax.set_facecolor('#FFFFFF')
    
    x_positions = list(range(len(section_scores['labels'])))
    
    # Current score line (Bauhaus Red - #D02020)
    ax.plot(
        x_positions, section_scores['current'], 
        marker='s', markersize=8, linewidth=3.2, 
        color='#D02020', markeredgecolor='#121212', markeredgewidth=2,
        label='CURRENT AUDIT', alpha=1.0
    )
    
    # Expected score line (Bauhaus Blue - #1040C0)
    ax.plot(
        x_positions, section_scores['expected'], 
        marker='o', markersize=9, linewidth=3.2, 
        color='#1040C0', markeredgecolor='#121212', markeredgewidth=2,
        label='OPTIMIZED TRAJECTORY', alpha=1.0
    )
    
    # Fill area between lines (Bauhaus Yellow delta zone)
    ax.fill_between(
        x_positions, section_scores['current'], section_scores['expected'], 
        alpha=0.35, color='#F0C020'
    )
    
    # Customize technical axes
    ax.set_xticks(x_positions)
    ax.set_xticklabels(
        section_scores['labels'], rotation=0, ha='center', 
        fontsize=9.5, color='#121212', fontweight='heavy'
    )
    ax.set_ylim(35, 104)
    ax.set_ylabel('SCORE INDEX (%)', color='#121212', fontsize=11, fontweight='heavy')
    ax.set_xlabel('RESUME CRITERIA CHANNELS', color='#121212', fontsize=11, fontweight='heavy')
    ax.tick_params(colors='#121212', labelsize=9.5, width=2)
    ax.grid(axis='y', alpha=0.18, color='#121212', linestyle='--')
    ax.grid(axis='x', alpha=0.10, color='#121212', linestyle=':')
    
    # Style Bauhaus Spines (Thick stark black framing)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#121212')
    ax.spines['left'].set_linewidth(3)
    ax.spines['bottom'].set_color('#121212')
    ax.spines['bottom'].set_linewidth(3)
    
    # Bauhaus Legend
    legend = ax.legend(
        loc='lower right', framealpha=1.0, facecolor='#FFFFFF', 
        edgecolor='#121212', fontsize=9.5, labelcolor='#121212'
    )
    legend.get_frame().set_linewidth(2.5)
    
    # Add values on points
    for i, (curr, exp) in enumerate(zip(section_scores['current'], section_scores['expected'])):
        ax.text(
            i, curr - 4.0, f'{int(curr)}%', ha='center', va='top', 
            fontsize=9, color='#D02020', weight='heavy'
        )
        if exp != curr:
            ax.text(
                i, exp + 2.5, f'{int(exp)}%', ha='center', va='bottom', 
                fontsize=9, color='#1040C0', weight='heavy'
            )
    
    plt.tight_layout()
    return fig