# Uplift Modeling on Criteo Advertising Data

Estimating the *causal* effect of showing someone an ad — not just predicting
who converts, but predicting who converts *because* they were shown the ad —
using the real Criteo uplift dataset and a two-model (T-learner) approach.

## Problem & Business Value

Most advertising is shown to people who would have bought anyway — reaching
them doesn't change anything, it just spends budget on a foregone conclusion.
The people worth reaching are the "persuadables": those who convert only *if*
they see the ad. A plain conversion-prediction model can't tell these two
groups apart, because it never compares what happens with and without the ad
for the same kind of person. Uplift modeling does, by explicitly modeling the
difference between the treated and untreated outcome. That difference is what
this project estimates, so that a limited ad budget can be pointed at the
users where it actually changes behavior, instead of everyone.

## Dataset

- **Source:** Criteo Uplift Modeling dataset (Kaggle)
- **Link:** https://www.kaggle.com/datasets/arashnic/uplift-modeling
- ~14 million rows from a real randomized controlled trial: each row is one
  user, randomly assigned to either see an ad (`treatment = 1`) or not
  (`treatment = 0`). 12 anonymized numeric features (`f0`–`f11`), plus three
  outcome columns: `visit`, `conversion` (the main outcome used here), and
  `exposure` (whether the user was actually shown an ad — see the Results
  section, this turns out to matter).

## Project Structure

```
criteo-uplift/
├── data/         # raw dataset (not committed — download from Kaggle link above)
├── notebooks/    # EDA, sampling, two-model training, Qini evaluation
├── src/          # currently empty — notebook code hasn't been refactored out yet
├── outputs/      # charts (.png) and the uplift_results.csv used by the dashboard
├── app/          # Streamlit targeting dashboard
├── requirements.txt
└── README.md
```

## How to Run

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd criteo-uplift

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies (includes Jupyter, so this alone is enough to
#    open and run the notebook, plus pandas/scikit-learn/scikit-uplift/
#    Streamlit for the modeling and the dashboard)
pip install -r requirements.txt

# 4. Download the dataset from the Kaggle link above and place it at:
#    data/criteo-uplift-v2.1.csv

# 5. Run the notebook end-to-end (this generates outputs/*.png and
#    outputs/uplift_results.csv — the dashboard in step 6 depends on this file)
jupyter notebook notebooks/01_EDA.ipynb

# 6. Run the dashboard
streamlit run app/dashboard.py
```

## Methodology

1. **EDA** on the full ~14M-row dataset: checked for missing values and
   duplicates, and confirmed the treatment/control split looks properly
   randomized (feature averages and distributions are nearly identical
   between the two groups).
2. **Sampling:** the full dataset is too slow to iterate on, so modeling uses
   a 7% sample, taken separately within each (treatment, conversion) group so
   the 85/15 treatment split and the rare conversion rate are preserved.
3. **Train/test split:** 80/20, stratified the same way, so the held-out
   test set doesn't end up with too few converters in either arm.
4. **Two-model (T-learner) uplift model:** two separate logistic regressions
   on the 12 anonymized features — one fit only on treated users, one fit
   only on control users. Each user's uplift score is
   `P(convert | treated) − P(convert | control)`, estimated by scoring every
   test user through both models.
5. **Evaluation:** Qini AUC and the Qini curve (via `scikit-uplift`), plus a
   decile breakdown (bucket users by predicted uplift, check the realized
   treated-vs-control conversion gap in each bucket).

## Results

- **Naive average effect:** control users convert 0.194% of the time, treated
  users 0.309% — about a 60% relative increase from being shown an ad.
- **Compliance matters:** only 3.6% of the "treated" group was actually
  exposed to an ad (control: 0%, so no contamination). Since most of the
  "treated" group never actually saw an ad, the true effect for people who
  are actually exposed is larger than the naive number above suggests.
- **Model performance:** Qini AUC = **0.187** — the model's uplift ranking
  meaningfully beats random targeting. The gain isn't spread evenly: the
  decile analysis shows the middle of the ranking is noisy (conversions are
  rare, so mid-sized groups give unstable estimates), but the top decile has
  a realized uplift several times larger than any other group — the model is
  genuinely good at finding the small slice of users worth targeting.
- **Dashboard:** `app/dashboard.py` turns this into an interactive targeting
  simulator — pick a % of users to target and see the estimated incremental
  conversions versus targeting the same number of users at random.

## Tech Stack

Python · pandas · NumPy · scikit-learn · scikit-uplift · Matplotlib ·
Streamlit · Jupyter
