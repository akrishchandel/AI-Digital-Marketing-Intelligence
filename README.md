# AI Digital Marketing Intelligence Platform


An AI and Data Science project that analyzes digital marketing campaigns, evaluates campaign performance, generates recommendations, and predicts conversions using Machine Learning.

## 🚀 Features

- Campaign performance dashboard
- Total spend and revenue analysis
- CTR calculation
- Conversion rate analysis
- ROAS analysis
- ROI analysis
- Best and worst campaign detection
- Best platform detection
- Campaign performance rating
- Campaign-specific recommendations
- Machine Learning conversion prediction
- Interactive charts
- Campaign and platform filters
- Downloadable campaign report

## 🧠 Machine Learning

The platform uses a Machine Learning regression model to predict the expected number of conversions.

### Input Features

- Impressions
- Clicks
- Advertising Spend

### Output

- Predicted conversions

## 📊 Campaign Intelligence

Campaigns are automatically classified into four categories:

| Rating | ROAS |
|---|---:|
| Excellent | ≥ 2x |
| Good | 1x – 1.99x |
| Needs Improvement | 0.5x – 0.99x |
| Poor | < 0.5x |

The system also generates recommendations based on campaign performance.

## 🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn
- Flask
- Joblib
- HTML
- CSS
- JavaScript
- Chart.js

## 📁 Project Structure

```text
AI-Digital-Marketing-Intelligence/
│
├── app.py
│
├── data/
│   ├── campaigns.csv
│   ├── clean_campaigns.csv
│   ├── analyzed_campaigns.csv
│   └── platform_analysis.csv
│
├── model/
│   └── conversion_model.pkl
│
├── src/
│   ├── data_processing.py
│   ├── analytics.py
│   ├── campaign_analysis.py
│   └── ml_model.py
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── .gitignore
└── README.md

## 👨‍💻 Author

**Akrish Chandel**

B.Tech Computer Science Engineering (AI & Data Science)

[GitHub](https://github.com/akrishchandel)