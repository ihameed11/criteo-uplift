# Ad Targeting Simulator
#
# Ranks the held-out test set by predicted uplift (T-learner) and shows the
# payoff of only targeting the top X% of users, versus targeting at random.
# Data source: outputs/uplift_results.csv, written by notebooks/uplift_analysis.ipynb.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

MODEL_COLOR = "#2a78d6"
RANDOM_COLOR = "#e34948"

st.set_page_config(page_title="Ad Targeting Simulator", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("outputs/uplift_results.csv")
    return df.sort_values("uplift", ascending=False).reset_index(drop=True)


@st.cache_data
def build_curve(df_sorted, overall_uplift, n_points=100):
    """Cumulative incremental conversions at each % of users targeted."""
    total = len(df_sorted)
    percentages = np.linspace(0, 100, n_points + 1)
    model_incremental = []
    for p in percentages:
        n = int(total * p / 100)
        if n == 0:
            model_incremental.append(0.0)
            continue
        group = df_sorted.head(n)
        t_rate = group.loc[group["treatment"] == 1, "conversion"].mean()
        c_rate = group.loc[group["treatment"] == 0, "conversion"].mean()
        if pd.isna(t_rate) or pd.isna(c_rate):
            model_incremental.append(0.0)
        else:
            model_incremental.append((t_rate - c_rate) * n)
    random_incremental = [overall_uplift * (total * p / 100) for p in percentages]
    return percentages, model_incremental, random_incremental


df_sorted = load_data()
total_users = len(df_sorted)

overall_treated_rate = df_sorted.loc[df_sorted["treatment"] == 1, "conversion"].mean()
overall_control_rate = df_sorted.loc[df_sorted["treatment"] == 0, "conversion"].mean()
overall_uplift = overall_treated_rate - overall_control_rate

st.title("Ad Targeting Simulator")
st.caption(
    "Ranks the test set by predicted uplift and shows the payoff of only "
    "targeting the top X% of users, versus targeting at random."
)

with st.sidebar:
    st.header("Targeting budget")
    percent = st.slider("% of users to target", 0, 100, 20)
    st.metric("Test set size", f"{total_users:,}")
    st.metric("Overall uplift (whole test set)", f"{overall_uplift:.4%}")

n_users = int(total_users * percent / 100)

if n_users == 0:
    st.info("Move the slider above 0% to see targeting results.")
else:
    targeted = df_sorted.head(n_users)
    treated_rate = targeted.loc[targeted["treatment"] == 1, "conversion"].mean()
    control_rate = targeted.loc[targeted["treatment"] == 0, "conversion"].mean()
    group_uplift = (
        0.0 if pd.isna(treated_rate) or pd.isna(control_rate)
        else treated_rate - control_rate
    )
    incremental = group_uplift * n_users
    random_incremental_here = overall_uplift * n_users

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Users targeted", f"{n_users:,}")
    col2.metric("Uplift in this group", f"{group_uplift:.4%}")
    col3.metric("Est. incremental conversions", f"{incremental:.0f}")
    col4.metric("vs. random targeting", f"{incremental - random_incremental_here:+.0f}")

    percentages, model_curve, random_curve = build_curve(df_sorted, overall_uplift)

    chart_col, bar_col = st.columns([2, 1])

    with chart_col:
        fig, ax = plt.subplots()
        ax.plot(percentages, model_curve, color=MODEL_COLOR, linewidth=2,
                label="Model (ranked by uplift)")
        ax.plot(percentages, random_curve, color=RANDOM_COLOR, linewidth=2,
                linestyle="--", label="Random targeting")
        ax.axvline(percent, color="gray", linestyle=":", linewidth=1)
        ax.scatter([percent], [incremental], color=MODEL_COLOR, s=60, zorder=5,
                   edgecolor="white")
        ax.set_xlabel("% of users targeted")
        ax.set_ylabel("Cumulative incremental conversions")
        ax.set_title("Incremental conversions vs. % targeted")
        ax.legend()
        st.pyplot(fig)

    with bar_col:
        fig2, ax2 = plt.subplots()
        ax2.bar(["Model", "Random"], [incremental, random_incremental_here],
                color=[MODEL_COLOR, RANDOM_COLOR])
        ax2.set_ylabel("Incremental conversions")
        ax2.set_title(f"At {percent}% targeted")
        st.pyplot(fig2)
