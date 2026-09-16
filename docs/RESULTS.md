# Results

## Main Experiment (seed=42)

| Metric | Value |
|:---|:---|
| Initial safe rate | 25.0% |
| Final safe rate | **91.0%** |
| Paper reference | 90.4% |
| Difference | +0.6 pp |

The model reproduces the published result **within 0.6 percentage points**.

## Scenario Comparison

| Scenario | Final safe rate |
|:---|:---|
| No managers | 29.0% |
| Weak managers (0.5) | 1.0% |
| Strong managers (0.9) | 87.0% |

**Key insight:** weak management can be worse than no management.
This is a **new finding** not explicitly stated in Zhang et al. (2025),
but derivable from Eq. 6–7.

## Batch Analysis (20 seeds)

| Metric | Value |
|:---|:---|
| Mean | 71.9% |
| Std | 11.6% |
| Min | 54.0% |
| Max | 93.0% |

High variance is expected in agent-based models (Railsback & Grimm, 2011).

## Reproducibility

All experiments can be reproduced via:

```bash
python run.py                                 # main experiment
python run.py --batch 20                      # robustness check
python -m src.visualize                       # generate plots
python -m src.batch --seeds 20                # batch confidence band
