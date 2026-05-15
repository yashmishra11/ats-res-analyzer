## ATS Resume Analyzer

Resume Optimization Platform that analyzes resume-job match scores using machine learning algorithms.

## 📁 Project Structure

```
ats-resume-analyzer/
│
├── app.py                          # Main Streamlit application (with auth)
├── config.py                       # Configuration and constants
├── nltk_setup.py                   # NLTK initialization
│
├── text_extractors.py              # PDF and text extraction utilities
├── feature_extractors.py           # Resume feature extraction (skills, education, etc.)
├── similarity_calculator.py        # Similarity scoring algorithms
├── section_analyzer.py             # Section-by-section analysis
├── recommendation_generator.py     # Improvement recommendations
├── visualization.py                # Charts and visualizations
├── ui_components.py                # Streamlit UI components and styling
│
├── auth.py                         # User & admin authentication
├── admin_dashboard.py              # Admin dashboard (stats, controls, uploads)
├── database.py                     # SQLite database (metadata + system settings)
├── s3_utils.py                     # AWS S3 PDF upload utilities
│
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not committed)
└── README.md                       # This file
```

## 🔧 Module Descriptions

### Core Modules

- **app.py**: Main application entry point. Orchestrates all components, handles authentication, and controls user interactions.

- **config.py**: Central configuration file containing all constants, skill categories, regex patterns, and score weights.

### Utility Modules

- **nltk_setup.py**: Handles NLTK initialization and downloads required packages.

- **text_extractors.py**: Functions for extracting and normalizing text from PDF files.

- **feature_extractors.py**: Extracts specific resume features like skills, technologies, education, experience, location, and projects.

### Analysis Modules

- **similarity_calculator.py**: Calculates resume-job match scores using:
  - TF-IDF similarity (40% weight)
  - Skills matching (30% weight)
  - Keyword matching (20% weight)
  - Section completeness (10% weight)

- **section_analyzer.py**: Performs detailed analysis of each resume section:
  - Skills & Technologies
  - Projects
  - Education
  - Experience Level
  - Location
  - Important Keywords

- **recommendation_generator.py**: Generates actionable recommendations and rewrite examples for improvement.

### UI Modules

- **ui_components.py**: Contains all Streamlit UI components, CSS styling, and rendering functions.

- **visualization.py**: Creates charts and graphs for visualizing analysis results.

### Auth & Admin Modules *(New in v3.0)*

- **auth.py**: Handles user and admin authentication using SHA256-hashed passwords and Streamlit session state.

- **admin_dashboard.py**: Full admin panel with upload statistics, timeline charts, recent uploads table, PDF viewer, CSV export, and the "No More Uppy" upload control toggle.

- **database.py**: SQLite database managing resume metadata (filename, S3 URL, scores, user, timestamp) and system settings (upload enable/disable toggle).

- **s3_utils.py**: Handles PDF uploads to AWS S3, generating public URLs stored in the database.

---

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ats-resume-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables — create a `.env` file:
```env
# AWS S3
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=your_bucket_name

# Admin credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
```

4. Initialize the database (auto-runs on first launch):
```bash
streamlit run app.py
```
---
## 📖 Usage

### Regular Users
1. **Login** with your credentials on the login screen
2. **Upload Resume** in PDF format
3. **Paste Job Description** from the job posting
4. **Set Relocation Preference** (Yes / No / Not specified)
5. **Click Analyze** — button sits inline below the Job Description
6. **Review Results**:
   - Current match score vs expected after improvements
   - Section-by-section impact chart
   - Detailed recommendations with bold highlighted keywords
   - Pro tips for ATS optimization

### Admin
1. Click **"🔑 Admin Login"** on the login screen
2. Access the **Admin Dashboard** to:
   - Toggle the **"No More Uppy"** switch to enable/disable S3 uploads
   - View upload statistics by hour / day / week / month / year
   - Browse recent uploads with scores and user info
   - Open or download individual PDFs from S3
   - Export all data as CSV

---

## 🎯 Features

### Analysis
- **Multi-factor Scoring**: Combines TF-IDF, skills matching, keywords, and section completeness
- **Section Detection**: Identifies missing or weak resume sections
- **Keyword Extraction**: Highlights critical missing terms from job descriptions
- **Bold Recommendations**: Missing keywords appear highlighted in green in each section card
- **Visual Analytics**: Section-by-section impact chart (current vs expected after improvements)
- **Relocation Awareness**: Factors in relocation preference for location scoring

### Authentication *(New in v3.0)*
- **User Login**: Email + password required to access the app
- **Admin Login**: Separate admin credentials via `.env`
- **Session Management**: Streamlit session state with logout support
- **SHA256 Password Hashing**: Passwords never stored in plain text

### Admin Dashboard *(New in v3.0)*
- **Upload Statistics**: Total uploads, average score, storage used, active users
- **Timeline Chart**: Visual bar chart of uploads over selected time period
- **Recent Uploads Table**: Last 50 uploads with filename, score, size, date, user
- **PDF Access**: Open S3 URL or download individual PDFs directly from dashboard
- **CSV Export**: Download full upload history as spreadsheet
- **"No More Uppy" Toggle**: Instantly disable S3 uploads to control AWS costs
  - When OFF: users can still analyze resumes, but no new files are saved to S3
  - When ON: full upload and save functionality restored

### Storage *(New in v3.0)*
- **AWS S3**: PDFs stored at `resumes/{uuid}.pdf` with public URLs
- **SQLite Database**: Local metadata store (`ats_analyzer.db`) tracking all uploads and system settings

---

## 🛠️ Customization

### Adding New Users

Edit `auth.py` and add to `DEMO_USERS`:

```python
DEMO_USERS = {
    "user@example.com": hashlib.sha256("password123".encode()).hexdigest(),
    "newuser@example.com": hashlib.sha256("theirpassword".encode()).hexdigest(),
}
```

### Changing Admin Password

Update `.env`:
```env
ADMIN_PASSWORD=your_new_secure_password
```

### Adding New Skills/Technologies

Edit `config.py` and add to `SKILL_CATEGORIES` or `TECH_KEYWORDS`:

```python
SKILL_CATEGORIES = {
    'New Category': ['skill1', 'skill2', 'skill3'],
    # ...
}
```

### Adjusting Score Weights

Modify weights in `config.py`:

```python
SCORE_WEIGHTS = {
    'tfidf': 0.40,
    'skills': 0.30,
    'keywords': 0.20,
    'sections': 0.10
}
```

### Adding New Recommendation Templates

Add templates to `recommendation_generator.py` in `keyword_templates` dictionary.

---

## 𖤓 Analysis Components

### Similarity Score Calculation
- **TF-IDF Similarity** (40%): Measures overall text similarity
- **Skills Matching** (30%): Compares technical skills and technologies
- **Keywords Matching** (20%): Checks for important keywords
- **Section Completeness** (10%): Verifies all necessary sections are present

### Section Analysis
Each section is rated as:
- ✓ **Good**: Meets requirements
- ⚠️ **Needs Work**: Needs improvement
- ❌ **Missing**: Critical gap

---

## 🎨 UI Customization

All styling is contained in `ui_components.py`. The app uses a consistent dark theme throughout:
- Background: `#0E1117`
- Cards: `#1E1E1E`
- Accent / Good: `#00D4AA` (teal green)
- Warning: `#FFA500` (orange)
- Error / Missing: `#FF6B6B` (red)
- Card-based layout with left border status indicators
- Interactive section-by-section impact chart
- Bold green keyword highlighting in recommendations

---

## ⚠️ Known Limitations

- PDF text extraction may vary based on PDF structure
- Visual/image-based PDFs may have reduced accuracy
- Semantic fallbacks are used for edge cases
- User accounts are currently hardcoded in `auth.py` (no self-registration)
- SQLite database is local — does not sync across multiple Streamlit Cloud instances

---

## 🌐 Deployment (Streamlit Cloud)

Add the following to **Streamlit Cloud → Settings → Secrets**:

```toml
AWS_REGION = "us-east-1"
AWS_ACCESS_KEY_ID = "your_key"
AWS_SECRET_ACCESS_KEY = "your_secret"
AWS_S3_BUCKET = "your_bucket"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_secure_password"
```

Then update `auth.py` to read from `st.secrets` with `.env` as fallback.

---

## 📝 Version History

| Version | Changes |
|---------|---------|
| **v3.0** | Added user authentication, admin dashboard, AWS S3 storage, SQLite database, "No More Uppy" upload toggle, relocation radio button, analyze button repositioned below JD |
| **v2.1** | Improved section detection, bold keyword highlighting, fixed location extraction for educational institutions |
| **v2.0** | Added section-by-section impact chart, expected score after improvements, relocation preference |
| **v1.0** | Initial release — TF-IDF similarity, section analysis, recommendations |

---

## 🤝 Contributing

Contributions are welcome! The modular structure makes it easy to:
- Add new analysis sections
- Improve extraction algorithms
- Enhance UI components
- Add new visualizations
- Extend the admin dashboard
