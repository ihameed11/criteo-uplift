# Ad Targeting Simulator
#
# Lets a user pick a targeting budget (top X% of users, ranked by predicted
# uplift) and see the estimated payoff: how much better does the model's
# ranking do than not targeting at all, for the group it selects?
#
# Data source: outputs/uplift_results.csv, written by notebooks/01_EDA.ipynb.
# It holds the held-out test set with each user's ground-truth treatment/
# conversion outcome plus the T-learner's predicted uplift score.
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("outputs/uplift_results.csv")

st.title("Ad Targeting Simulator")

# Rank users best-to-worst by predicted uplift, so "top X%" means "the X%
# the model thinks are most worth targeting".
df_sorted = df.sort_values("uplift", ascending=False)

percent = st.slider("Percentage of users to target", 0, 100, 20)

n_users = int(len(df_sorted) * percent / 100)

targeted = df_sorted.head(n_users)
st.write(f"Targeting the top {n_users} users")

# Realized conversion rates within the targeted group, split by what
# actually happened to each user (they were randomly treated or held out as
# control regardless of our targeting choice). Comparing the two gives an
# empirical estimate of the uplift actually achieved among the users we
# picked — the same idea behind the Qini curve in the notebook.
treated_rate = targeted[targeted["treatment"] == 1]["conversion"].mean()
control_rate = targeted[targeted["treatment"] == 0]["conversion"].mean()


group_uplift = treated_rate - control_rate
incremental = group_uplift * n_users


st.metric("Users targeted", n_users)
st.metric("Uplift in this group", f"{group_uplift:.4f}")
st.metric("Estimated incremental conversions", f"{incremental:.0f}")