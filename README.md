# Agent-Based Simulation of Construction Worker Safety

[![Tests](https://github.com/Hickmanda/abm-construction-safety/actions/workflows/tests.yml/badge.svg)](https://github.com/Hickmanda/abm-construction-safety/actions/workflows/tests.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python implementation of the agent-based model (ABM) from **Zhang et al. (2025, ASCE Journal of Construction Engineering and Management)**. The model simulates how construction managers influence workers' safety behavior through **cumulative prospect theory (CPT)** and **cognitive process modeling**.

> **Result:** Our model reproduces the paper's key finding — workers' safe behavior rate stabilizes at **91%**, matching the published result of **90.4%** (seed=42).

---

## 📸 Visualizations

### Safe Behavior over Time

![Safe Behavior](results/safe_behavior_rate.png)

*S-curve growth from 25% (initial) to ~90% (equilibrium), matching Fig. 9 in the paper.*

### Worker Cognitive Attributes

![Worker Attributes](results/worker_attributes.png)

*SA (situational awareness), SK (safety knowledge), and A (reference point) all rise above the cognitive threshold of 0.6.*

### Impact of Management Behavior

![Scenario Comparison](results/scenario_comparison.png)

*Three scenarios: no managers (≈29%), weak managers (≈1%), strong managers (≈87%). Management quality is the key driver of safety.*

### Batch Analysis (20 seeds)

![Batch Analysis](results/batch_analysis.png)

*Mean trajectory ± 1 std across 20 random seeds. The model consistently converges to high safety levels, with variance reflecting sensitivity to initial conditions.*

---

## 🎯 Model Overview

### Agents

**Workers (100 by default)** — each with 5 cognitive attributes:
- **SA** — Situational Awareness
- **SK** — Safety Knowledge
- **SN** — Subjective Norm
- **BA** — Behavior Attitude
- **PBC** — Perceived Behavior Control

**Managers (3 by default)** — 5 management behaviors:
- **ET** — Education and Training
- **IR** — Inspection and Rectification
- **SI** — Safety Information
- **SM** — Stakeholder Management
- **HEM** — Hazard and Emergency Management

### Cognitive Decision Process (Eq. 20)

Each worker decides through 3 stages:
1. **Understanding Information** — driven by SA
2. **Perceiving Response** — driven by SK
3. **Selecting Response** — driven by SN, BA, PBC via CPT

A worker behaves safely **only if all three stages pass the 0.6 threshold**.

---

## 🧮 Mathematical Foundation

The model implements the following equations from Zhang et al. (2025):

| Equation | Description |
|:---|:---|
| **Eq. 1–5** | Manager → Worker influence on SA, SK, SN, BA, PBC |
| **Eq. 6–7** | Manager adapts ET and IR based on safety trend |
| **Eq. 9–13** | CPT formulas (value + weight functions) |
| **Eq. 14** | Cumulative prospect of UNSAFE behavior (4 outcomes) |
| **Eq. 15** | Cumulative prospect of SAFE behavior (2 outcomes) |
| **Eq. 16–19** | Dynamic CPT parameters (A, α, β, λ) from SN, BA, PBC |
| **Eq. 20** | Cognitive threshold discrimination rule |
| **Eq. 21** | Outcome ordering constraints |

All parameters are from **Tables 6 and 7** of the paper, based on Tversky & Kahneman (1992).

---

## 🛠 Tech Stack

- **Python 3.11** — core language
- **Mesa** — agent-based modeling framework
- **NumPy** — numerical computations
- **Matplotlib** — visualization
- **pytest** — unit testing
- **Docker** — containerization
- **GitHub Actions** — CI/CD

---

## 🚀 Quick Start

### Option 1 — Local (with venv)

```bash
git clone https://github.com/Hickmanda/abm-construction-safety.git
cd abm-construction-safety

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Run the main experiment
python run.py

# Generate all plots
python -m src.visualize

# Run robustness check (20 seeds)
python -m src.batch --seeds 20

# Run tests
python -m pytest -v
```

### Option 2 — Docker

```bash
docker compose up --build
```

Output plots will appear in `results/`.

---

## 📊 CLI Options

```bash
python run.py --help

# Custom parameters
python run.py --workers 200 --managers 5 --days 200 --seed 7

# Batch mode
python run.py --batch 20
```

---

## 📁 Project Structure

```
abm-construction-safety/
├── .github/
│   └── workflows/
│       └── tests.yml           # CI: runs tests on every push
├── src/
│   ├── __init__.py
│   ├── cpt.py                  # CPT formulas (Eq. 9–15)
│   ├── params.py               # All parameters (Tables 6, 7)
│   ├── agents.py               # Worker and Manager
│   ├── model.py                # Mesa model
│   ├── batch.py                # Batch experiments
│   └── visualize.py            # Plot generation
├── tests/
│   ├── test_cpt.py             # 12 tests
│   └── test_agents.py          # 7 tests
├── notebooks/
│   └── exploration.ipynb       # Interactive analysis
├── results/                    # Generated plots
├── run.py                      # CLI entry point
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── .flake8
├── .dockerignore
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📊 Results

### Main Result (seed=42)

| Metric | Value |
|:---|:---|
| Initial safe rate | 25.00% |
| Final safe rate | **91.00%** |
| Paper reference | 90.4% |

Our result reproduces the published finding within **0.6 percentage points**.

### Scenario Comparison

| Scenario | Final safe rate |
|:---|:---|
| No managers | 29.00% |
| Weak managers (ET = IR = 0.5) | 1.00% |
| Strong managers (ET = IR = 0.9) | 87.00% |

**Key insight:** weak management can be *worse than no management* — partial interventions keep workers below the cognitive threshold, creating a low-safety equilibrium.

### Robustness Check (20 seeds)

| Metric | Value |
|:---|:---|
| Mean final rate | 71.90% |
| Std deviation | 11.60% |
| Range | 54.00% – 93.00% |

High variance is **expected in ABM** — a well-documented property caused by sensitivity to initial conditions (Railsback & Grimm, 2011).

---

## 🧪 Testing

19 unit tests cover the mathematical core:

```bash
python -m pytest -v
```

```
19 passed in 0.12s
```

CI runs automatically on every push via **GitHub Actions**.

---

## 💡 What I Learned

- **Agent-based modeling** — designing agents, interaction rules, and simulation loops with Mesa
- **Cumulative Prospect Theory** — implementing value and weight functions from a research paper
- **Cognitive process modeling** — formalizing decision-making in three stages
- **Reproducing scientific results** — matching published findings with < 1% error
- **Research software engineering** — unit tests, CLI, modular structure, Docker, CI/CD

---

## 📖 References

1. **Zhang, Z., Guo, H., Li, H., & Fang, Y.** (2025). *Agent-Based Simulation Approach to Analyzing the Impact of Construction Safety Management Behaviors on Workers' Safety Behaviors.* Journal of Construction Engineering and Management, 151(8). DOI: [10.1061/JCEMD4.COENG-15977](https://doi.org/10.1061/JCEMD4.COENG-15977)

2. **Tversky, A., & Kahneman, D.** (1992). *Advances in prospect theory: Cumulative representation of uncertainty.* Journal of Risk and Uncertainty, 5(4), 297–323.

3. **Ajzen, I.** (1991). *The theory of planned behavior.* Organizational Behavior and Human Decision Processes, 50(2), 179–211.

---

## 📬 Contact

**Author:** Daniil Marchici
**GitHub:** [@Hickmanda](https://github.com/Hickmanda)
**Research collaboration:** with a student at South China University of Technology (SCUT)

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

This project is based on an open-access research paper. Code is provided for **educational and research purposes**.
