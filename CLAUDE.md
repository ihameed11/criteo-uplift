# Criteo Uplift Modeling — MSc Data Analytics Project

## Project

Uplift modeling on the real Criteo uplift dataset. The goal is to estimate the
causal effect of treatment (e.g. exposure to advertising) on an individual's
behavior, not just predict the outcome itself.

**Stack:** Python, pandas, scikit-learn, scikit-uplift, matplotlib, Streamlit.

## Working style — READ BEFORE DOING ANYTHING

This is a learning project. The user is learning uplift modeling as we go, so
process matters as much as the output.

- **One step at a time.** Do a single stage of work (e.g. "load and inspect
  the data", "split into train/test", "fit the treatment model") and then
  STOP. Do not chain multiple stages together, even if the next step seems
  obvious or trivial.
- **Wait for explicit go-ahead** before starting the next step. Do not
  proceed on the assumption that the user will want to continue — ask.
- **Explain your reasoning as you go.** Say why a step is needed, what the
  alternatives were, and what the code/output means, not just what you did.
  Assume the user wants to understand the concepts (uplift modeling, T-learner
  mechanics, evaluation metrics like Qini/uplift curves), not just get
  working code.
- **Keep models simple and interpretable.** Default approach is a two-model
  T-learner (one model for treatment group, one for control group, uplift =
  difference in predictions). Avoid fancy/complex uplift techniques (e.g.
  class transformation tricks, causal forests, meta-learners beyond T-learner)
  unless the user explicitly asks to explore them.
- **Never run more than one stage without checking in.** If a task naturally
  splits into multiple stages, list them, propose the first one, and stop.

If in doubt about whether something counts as "one step," err on the side of
smaller steps and more check-ins.
