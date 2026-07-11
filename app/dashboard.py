import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df=pd.read_csv("outputs/uplift_results.csv")

st.title("Ad Targeting Simulator")

df_sorted = df.sort_values("uplift", ascending=False)

percent = st.slider("Percentage of users to target", 0, 100, 20)

n_users = int(len(df_sorted) * percent / 100)

targeted = df_sorted.head(n_users)
st.write(f"Targeting the top {n_users} users")

treated_rate = targeted[targeted["treatment"] == 1]["conversion"].mean()
control_rate = targeted[targeted["treatment"] == 0]["conversion"].mean()


group_uplift = treated_rate - control_rate
incremental = group_uplift * n_users


st.metric("Users targeted", n_users)
st.metric("Uplift in this group", f"{group_uplift:.4f}")
st.metric("Estimated incremental conversions", f"{incremental:.0f}")