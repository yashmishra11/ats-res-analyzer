"""
Configuration constants for ATS Resume Analyzer
"""

# Application constants
APP_TITLE = "ATS Resume Analyzer"
APP_ICON = "𖤓"
APP_VERSION = "1.0.1"
APP_DESCRIPTION = "Resume analysis tool that helps you optimize your resume for ATS systems"

# Cyberpunk / Glitch Design Token System
BACKGROUND_COLOR = "#0a0a0f"     # Deep void black with slight blue undertone
FOREGROUND_COLOR = "#e0e0e0"     # Primary text, soft high-tech white
CARD_COLOR = "#12121a"           # Deep purple-black container
MUTED_COLOR = "#1c1c2e"          # UI chrome/elevated backgrounds
MUTED_FOREGROUND = "#6b7280"     # Secondary text
ACCENT_COLOR = "#00ff88"         # PRIMARY NEON - Electric green (Matrix)
ACCENT_SECONDARY = "#ff00ff"     # SECONDARY NEON - Hot magenta/pink
ACCENT_TERTIARY = "#00d4ff"      # TERTIARY NEON - Cyan/electric blue
BORDER_COLOR = "#2a2a3a"         # Technical HUD border
INPUT_COLOR = "#12121a"          # Terminal input background
RING_COLOR = "#00ff88"           # Focus ring
DESTRUCTIVE_COLOR = "#ff3366"    # Critical/error red-pink

# Legacy aliases mapped to Cyberpunk palette
PRIMARY_COLOR = ACCENT_COLOR
SECONDARY_COLOR = CARD_COLOR
SUCCESS_COLOR = ACCENT_COLOR
WARNING_COLOR = "#ffa500"
ERROR_COLOR = DESTRUCTIVE_COLOR

# Score thresholds for status badges
SCORE_EXCELLENT_THRESHOLD = 80
SCORE_GOOD_THRESHOLD = 60
SCORE_FAIR_THRESHOLD = 40

# Important keywords that should appear in resume
IMPORTANT_KEYWORDS = [
    'agile', 'scrum', 'team', 'project', 'collaboration', 'communication',
    'leadership', 'problem-solving', 'analytical', 'performance', 'optimization',
    'deployment', 'testing', 'debugging', 'documentation', 'workflow',
    'api', 'database', 'frontend', 'backend', 'fullstack', 'development',
    'design', 'architecture', 'scalable', 'efficient', 'responsive',
    'ci/cd', 'devops', 'cloud', 'security', 'authentication', 'authorization'
]

# Education keywords
EDUCATION_KEYWORDS = [
    'bachelor', 'master', 'phd', 'degree', 'diploma', 'certification',
    'computer science', 'engineering', 'information technology', 'software',
    'b.tech', 'm.tech', 'b.e', 'm.e', 'bsc', 'msc', 'bca', 'mca'
]

# Job type keywords for role detection
JOB_TYPE_KEYWORDS = {
    'frontend': [
        'frontend', 'front-end', 'ui', 'ux', 'react', 'angular', 'vue',
        'html', 'css', 'javascript', 'typescript', 'responsive', 'web design'
    ],
    'backend': [
        'backend', 'back-end', 'server', 'api', 'database', 'sql', 'nosql',
        'node', 'django', 'flask', 'spring', 'microservices', 'rest', 'graphql'
    ],
    'fullstack': [
        'fullstack', 'full-stack', 'full stack', 'mern', 'mean', 'lamp'
    ],
    'devops': [
        'devops', 'sre', 'infrastructure', 'ci/cd', 'docker', 'kubernetes',
        'aws', 'azure', 'gcp', 'jenkins', 'terraform', 'ansible'
    ],
    'data': [
        'data scientist', 'data engineer', 'data analyst', 'machine learning',
        'ml', 'ai', 'deep learning', 'nlp', 'computer vision', 'analytics'
    ]
}

# Skill categories for organizing skills
SKILL_CATEGORIES = {
    'Programming Languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby',
        'php', 'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab'
    ],
    'Frontend': [
        'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt', 'gatsby',
        'html', 'css', 'webpack', 'babel', 'vite'
    ],
    'Backend & Frameworks': [
        'node.js', 'express', 'django', 'flask', 'fastapi', 'spring',
        'laravel', 'rails', 'rest', 'graphql', 'grpc'
    ],
    'Databases & Storage': [
        'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis',
        'elasticsearch', 'cassandra', 'prisma', 'sequelize'
    ],
    'Cloud & DevOps': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
        'git', 'github', 'gitlab', 'ci/cd', 'terraform', 'ansible'
    ],
    'Data Science & AI': [
        'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
        'keras', 'machine learning', 'deep learning', 'nlp'
    ]
}

# Score weights for similarity calculation
SCORE_WEIGHTS = {
    'tfidf': 0.30,       # Text similarity
    'skills': 0.40,      # Skills match
    'keywords': 0.20,    # Important keywords
    'sections': 0.10     # Section completeness
}

# Improvement potential settings
IMPROVEMENT_POTENTIAL = {
    'section_missing': 8.0,           # Points gained by adding missing section
    'section_weak': 4.0,              # Points gained by improving weak section
    'max_section_improvement': 25.0,  # Maximum total improvement from sections
    'max_overall_score': 98.0         # Maximum achievable score
}

# Status score mappings for visualization
STATUS_SCORES = {
    'missing': 45,
    'weak': 65,
    'good': 90,
    'present': 90  # Alias for 'good'
}

# Expected scores after improvements
EXPECTED_SCORES_AFTER_FIX = {
    'missing': 75,
    'weak': 85,
    'good': 95
}

# Section display order
SECTION_ORDER = [
    'Skills & Technologies',
    'Education',
    'Experience Level',
    'Location',
    'Important Keywords',
    'Projects'
]

# Section label mapping for display
SECTION_LABEL_MAP = {
    'Skills & Technologies': 'Skills &\nTechnologies',
    'Education': 'Education',
    'Experience Level': 'Experience\nLevel',
    'Location': 'Location',
    'Important Keywords': 'Important\nKeywords',
    'Projects': 'Projects'
}