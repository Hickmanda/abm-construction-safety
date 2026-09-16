# Methodology

This document explains the mathematical foundations of the ABM model
and each component in detail. It is intended for readers of the
bachelor's thesis who want to understand *why* the code is structured
the way it is.

## Overview

The model implements Zhang et al. (2025, ASCE JCEM), which uses
**agent-based modeling (ABM)** combined with **cumulative prospect
theory (CPT)** to simulate how construction managers influence
workers' safety behavior.

## Three-Layer Structure


### Layer 1: Managers

Managers have 5 behavior types: ET, IR, SI, SM, HEM.

Each is initialized as `N(0.85, 0.1)` from Table 5 in the paper.

### Layer 2: Worker Attributes

Workers have 5 cognitive attributes: SA, SK, SN, BA, PBC.

Initialized as `N(0.6, 0.1)` from p.11 of the paper.

Updated by managers through Eq. 1–5, with a memory coefficient `m = 28`.

### Layer 3: Cognitive Process

Workers decide in 3 stages (Eq. 20):

1. **Understanding Information** — needs SA ≥ 0.6
2. **Perceiving Response** — needs SK ≥ 0.6
3. **Selecting Response** — needs SB ≥ 0.6

Where `SB` comes from CPT (Eq. 14–15).

## CPT Implementation

The value function (Eq. 10) and weight functions (Eq. 12–13)
are implemented in `src/cpt.py`. All parameters from Table 7.

## Dynamic CPT Parameters (Eq. 16–19)

The reference point A, sensitivity α/β, and risk aversion λ are not
fixed — they evolve with SN, BA, PBC:

- A depends on SN (Eq. 16)
- α, β depend on BA (Eq. 17–18)
- λ depends on BA and PBC (Eq. 19)

This is what makes the model *dynamic*.

## Why Weak Managers are Worse than None

When ET and IR are weak (0.5 < 0.6), workers stay *just below*
the cognitive threshold. Managers then start relaxing their behaviors
(thinking all is well), which pushes workers even further down. Result:
a low-safety equilibrium.

This is a key finding of our reproduction (see `RESULTS.md`).

## Validation

We reproduce the paper's main result: ~90.4% safe rate.

See `docs/RESULTS.md` for details.
