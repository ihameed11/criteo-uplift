# Uplift Modeling on Criteo Advertising Data

[One-sentence description. What does this project do, in plain language?
e.g. "Predicting which customers respond incrementally to advertising,
so marketing budget targets the people who actually change their behavior."]

## Problem & Business Value

[2-3 sentences. Frame the business question, not the algorithm.
Why does an advertiser care? Hint: most ad spend is wasted on people who'd
convert anyway — the goal is to find the "persuadables." Write this in your
own words once you fully understand it.]

## Dataset

- **Source:** Criteo Uplift Modeling dataset (Kaggle)
- **Link:** https://www.kaggle.com/datasets/arashnic/uplift-modeling
- [Describe it briefly: ~13M rows, real randomized-control-trial ad data,
  12 anonymized features, a treatment flag, and visit/conversion labels.]

## Project Structure

​```
criteo-uplift/
├── data/         # raw dataset (not committed — download from Kaggle link above)
├── notebooks/    # EDA and modeling experiments
├── src/          # reusable, cleaned-up code
├── outputs/      # generated charts and results
├── app/          # Streamlit dashboard
├── requirements.txt
└── README.md
​```

## How to Run

​```bash
# 1. Clone the repo
git clone [your-repo-url]
cd criteo-uplift

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the dataset from the Kaggle link above into data/

# 5. Run the dashboard
streamlit run app/[your_app_name].py
​```

## Methodology

[Fill this in as you build. Brief notes on:
- how you cleaned the data
- the two-model uplift approach you used
- how you evaluated it (Qini curve)]

## Results

[Placeholder — fill in once you have findings. Your headline uplift number,
Qini result, and a screenshot of the dashboard go here. This section is what
recruiters read most, so make it concrete when you get there.]

## Tech Stack

Python · pandas · NumPy · scikit-learn · scikit-uplift · Matplotlib · Streamlit