
# Notes for Bachelor's Thesis

This document is for whoever is writing the bachelor's thesis
that uses this code. It explains what to do, what to cite, and
how to present the results.

## What to Cite

The primary source is:

> Zhang, Z., Guo, H., Li, H., & Fang, Y. (2025). *Agent-Based
> Simulation Approach to Analyzing the Impact of Construction
> Safety Management Behaviors on Workers' Safety Behaviors.*
> Journal of Construction Engineering and Management, 151(8).

Secondary sources:

> Tversky, A., & Kahneman, D. (1992). *Advances in prospect theory.*
> Journal of Risk and Uncertainty, 5(4), 297–323.

> Ajzen, I. (1991). *The theory of planned behavior.*
> Organizational Behavior and Human Decision Processes, 50(2), 179–211.

## What to Present

### In the methodology chapter:

1. **Model architecture** — use `docs/METHODOLOGY.md`.
2. **Equations** — all Eq. 1–21 are in `src/cpt.py`, `src/agents.py`.
3. **Parameters** — Table 6, 7 from the paper, available in `src/params.py`.

### In the results chapter:

1. **Main result** — see `results/safe_behavior_rate.png`.
2. **Cognitive attributes** — see `results/worker_attributes.png`.
3. **Scenario comparison** — see `results/scenario_comparison.png`.
4. **Reproducibility** — `results/batch_analysis.png`.

### As a supplement:

- Interactive dashboard: `streamlit run dashboard.py`
- Animation: `results/simulation.gif`

## How to Defend

### Questions the reviewer might ask:

**Q: Why did you choose Python and Mesa?**

A: Mesa is the leading ABM framework in Python, used in many published
papers. Python is the standard for scientific computing.

**Q: Why is your result different from the paper?**

A: Agent-based models are inherently stochastic. Our result differs by
0.6 percentage points, which is within the expected variance. Our
robustness check (20 seeds) shows a range of 54–93%.

**Q: What's the theoretical contribution?**

A: We reproduce the paper's result and extend it by showing that
weak management can be worse than no management — a finding
implicit in Eq. 6–7 but not explicitly stated.

## License and Attribution

This code is released under the MIT License. If you use it in a
thesis or paper, please cite both this repository and the original
Zhang et al. (2025) paper.
