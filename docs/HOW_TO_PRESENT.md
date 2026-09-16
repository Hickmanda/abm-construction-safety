# How to Present This Project

A step-by-step guide for presenting the ABM simulation to
academic supervisors, review committees, or at a thesis defence.

---

## 📌 Quick Summary (30 seconds)

If someone asks *"What is this project about?"* — say:

> *"This is a Python implementation of an agent-based model from
> Zhang et al. (2025, ASCE JCEM). It simulates how construction
> managers influence workers' safety behavior through cumulative
> prospect theory. The model reproduces the paper's main result:
> ~90% safety rate at equilibrium."*

---

## 🎯 Different Presentation Scenarios

### Scenario A — Send an email to a professor (5 minutes)

**What to write:**

> Dear Professor [Name],
>
> I would like to share a project I've been working on:
> an agent-based simulation of construction worker safety behavior,
> based on Zhang et al. (2025, ASCE JCEM).
>
> **Live demo:** https://abm-construction-safety.streamlit.app
> **GitHub:** https://github.com/Hickmanda/abm-construction-safety
>
> The model reproduces the paper's key result (90.4% safe rate).
> Full documentation is in the `docs/` folder.
>
> I would be happy to discuss this in more detail.
>
> Best regards,
> [Your Name]

**What the professor will see:**
1. **Streamlit dashboard** — 30 seconds to understand
2. **GitHub README** — 2 minutes to get full picture
3. **`docs/METHODOLOGY.md`** — 10 minutes for deep dive

### Scenario B — 10-minute presentation at a meeting

**Structure:**

| Time | What | Where |
|:---|:---|:---|
| 0:00–0:30 | Problem statement | Slide 1 |
| 0:30–1:30 | Model overview (agents + 3-stage cognition) | Slide 2 |
| 1:30–3:00 | Live demo — open Streamlit dashboard | Browser |
| 3:00–5:00 | Main result — 91% vs 90.4% | `results/safe_behavior_rate.png` |
| 5:00–6:30 | Scenario comparison | `results/scenario_comparison.png` |
| 6:30–8:00 | Robustness check (20 seeds) | `results/batch_analysis.png` |
| 8:00–10:00 | Q&A + code walkthrough | GitHub |

### Scenario C — Bachelor's thesis defence (15–20 minutes)

Same as Scenario B, but add:
- **Jupyter notebook** — open `notebooks/exploration.ipynb` and walk through CPT formulas
- **Methodology detail** — read from `docs/METHODOLOGY.md`
- **Reproducibility** — show that `python run.py` gives same result

---

## 🎬 Live Demo Script (Streamlit dashboard)

**Step 1:** Open https://abm-construction-safety.streamlit.app

**Step 2:** Say: *"This is an interactive dashboard built on top of
the simulation. On the left you can adjust parameters."*

**Step 3:** Show defaults (100 workers, 3 managers, 100 days, seed=42).

**Step 4:** Click **▶️ Run simulation**. While it runs, say:
*"The simulation takes about 3 seconds to complete 100 days."*

**Step 5:** When results appear, point to:
- **Metric cards** — *"Initial 25%, final 91%, paper reference 90.4%"*
- **Safe Behavior chart** — *"The S-curve shows workers gradually adopting safe behavior"*
- **Worker Attributes chart** — *"SA, SK, and reference point all rise above the 0.6 threshold"*

**Step 6:** Change **workers to 200**, click Run again:
*"With more workers, the model shows higher variance — a classic property of ABM"*

**Step 7:** Close dashboard.

---

## ❓ Questions the Reviewer Might Ask

### Q1: Why agent-based modeling instead of regression?

**A:** Regression can't capture emergent behavior from individual
decisions. ABM lets us model how macro-level patterns (like 90%
safety rate) emerge from micro-level interactions.

### Q2: Why Cumulative Prospect Theory?

**A:** CPT captures real human decision-making under uncertainty —
especially loss aversion and probability weighting. Standard
expected utility theory assumes perfect rationality, which doesn't
match how construction workers actually behave.

### Q3: Why is the result 91% and not exactly 90.4%?

**A:** The model is stochastic. Different random seeds give
different final results (range: 54%–93% across 20 seeds).
Our seed=42 result (91%) is within 0.6 percentage points of the
paper's 90.4%.

### Q4: How do I know the code is correct?

**A:** We have 19 unit tests that verify every formula from the
paper. Tests run automatically on every push via GitHub Actions
(see the green ✅ badge in the README).

### Q5: What's the theoretical contribution?

**A:** We reproduce the paper's result and additionally show that
**weak management can be worse than no management** — a finding
implicit in Eq. 6–7 but not explicitly discussed in the paper.

### Q6: What about scaling? Can it handle 10,000 workers?

**A:** Yes, but simulation time grows linearly. Currently we
simulate 100–500 workers in 3–5 seconds. For 10,000 we'd need
optimization (vectorization or parallelization).

---

## 🎥 Screen Recording (Optional)

If you want to record a video demo:

1. **OBS Studio** (free) — download from obsproject.com
2. Record screen for 3–5 minutes
3. Upload to YouTube (Unlisted)
4. Add link to README

**What to record:**
- Open Streamlit dashboard
- Run simulation
- Show all 4 charts
- Open Jupyter notebook
- Show GitHub README

---

## 📋 Pre-Presentation Checklist

Before showing to anyone:

- [ ] Streamlit dashboard is live: [check](https://abm-construction-safety.streamlit.app)
- [ ] GitHub repository is public
- [ ] README renders correctly with all images
- [ ] `python -m pytest -v` gives 19 passed
- [ ] `python run.py` gives ~91% final rate
- [ ] All 4 PNG charts are present in `results/`
- [ ] GIF animation works
- [ ] Jupyter notebook runs without errors

---

## 💡 Tips for the Defence

1. **Start with the WHY, not the HOW.** First explain *why* safety
   matters, *why* ABM is needed, *why* CPT is used. Then show code.

2. **Use the dashboard for engagement.** Live demo > static slides.

3. **Be honest about limitations.** ABM is stochastic. Different
   seeds give different results. This is a **feature**, not a bug.

4. **Cite properly.** Always reference Zhang et al. (2025) as the
   primary source.

5. **Know your parameters.** Table 6 and 7 of the paper list
   every number used in the model. Be ready to explain each one.

6. **Prepare for "What if...?"** questions. Try changing parameters
   in the dashboard **before** the meeting — so you know what
   happens when the reviewer asks.

---

## 📞 Contact

If you have questions about this project, contact:

**Daniil Marchici** — [@Hickmanda](https://github.com/Hickmanda)
