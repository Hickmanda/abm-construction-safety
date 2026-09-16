"""
Visualization of the ABM simulation results.
Produces Fig. 9-style plots from Zhang et al. (2025).
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os

from src.model import SafetyModel


def run_and_plot(num_workers=100, num_managers=3, steps=100, seed=42):
    """Run one simulation and save 2 plots."""
    print(f"Running simulation: {num_workers} workers x "
          f"{num_managers} managers x {steps} days...")

    model = SafetyModel(num_workers=num_workers,
                        num_managers=num_managers,
                        seed=seed)
    model.run(steps=steps)

    days = list(range(1, steps + 1))

    # --------------------------------------------------------
    # Figure 1: Safe behavior rate over time
    # --------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(days, [r * 100 for r in model.safety_rate_history],
             color='#007bff', linewidth=2.5)
    ax1.axhline(y=90.4, color='red', linestyle='--',
                label='Zhang et al. (2025): 90.4%')
    ax1.set_xlabel('Day', fontsize=13)
    ax1.set_ylabel('Safe behavior rate (%)', fontsize=13)
    ax1.set_title('Workers\' Safe Behavior over Time',
                  fontsize=15, fontweight='bold')
    ax1.grid(alpha=0.3)
    ax1.legend(fontsize=11)
    ax1.set_ylim(0, 105)

    os.makedirs('results', exist_ok=True)
    fig1.tight_layout()
    fig1.savefig('results/safe_behavior_rate.png', dpi=150)
    print("Saved: results/safe_behavior_rate.png")

    # --------------------------------------------------------
    # Figure 2: Average attributes over time
    # --------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(days, model.avg_SA_history,
             label='Situational Awareness (SA)', color='#28a745',
             linewidth=2.5)
    ax2.plot(days, model.avg_SK_history,
             label='Safety Knowledge (SK)', color='#fd7e14',
             linewidth=2.5)
    ax2.plot(days, model.avg_reference_point_history,
             label='Reference Point (A)', color='#6f42c1',
             linewidth=2.5)
    ax2.axhline(y=0.6, color='red', linestyle='--',
                alpha=0.5, label='Cognitive threshold (0.6)')
    ax2.set_xlabel('Day', fontsize=13)
    ax2.set_ylabel('Average value', fontsize=13)
    ax2.set_title('Worker Attributes over Time',
                  fontsize=15, fontweight='bold')
    ax2.grid(alpha=0.3)
    ax2.legend(fontsize=11)
    ax2.set_ylim(0, 1)

    fig2.tight_layout()
    fig2.savefig('results/worker_attributes.png', dpi=150)
    print("Saved: results/worker_attributes.png")

    # --------------------------------------------------------
    # Print summary
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Initial safe rate: {model.safety_rate_history[0]:.2%}")
    print(f"Final safe rate:   {model.safety_rate_history[-1]:.2%}")
    print("Target (paper):    90.4%")

    return model


def plot_scenarios(steps=100, seed=42):
    """
    Compare three scenarios:
    1. No managers (control) — workers never influenced
    2. Weak managers (ET/IR = 0.5)
    3. Strong managers (ET/IR = 0.9)
    """
    print("\nRunning 3 scenarios...")

    scenarios = [
        ('No managers', 'none'),
        ('Weak managers', 'weak'),
        ('Strong managers', 'strong'),
    ]

    results = {}

    for name, mode in scenarios:
        model = SafetyModel(num_workers=100, num_managers=3, seed=seed)

        if mode == 'none':
            model.managers = []
        elif mode == 'weak':
            for m in model.managers:
                m.ET = m.IR = m.SI = m.SM = m.HEM = 0.5
        elif mode == 'strong':
            for m in model.managers:
                m.ET = m.IR = m.SI = m.SM = m.HEM = 0.9

        model.run(steps=steps)
        results[name] = model.safety_rate_history
        print(f"  {name}: final safe rate = "
              f"{model.safety_rate_history[-1]:.2%}")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {
        'No managers': '#dc3545',
        'Weak managers': '#fd7e14',
        'Strong managers': '#28a745',
    }

    days = list(range(1, steps + 1))
    for name, history in results.items():
        ax.plot(days, [r * 100 for r in history],
                label=name, color=colors[name], linewidth=2.5)

    ax.axhline(y=90.4, color='black', linestyle='--', alpha=0.6,
               label='Zhang et al. (2025): 90.4%')
    ax.set_xlabel('Day', fontsize=13)
    ax.set_ylabel('Safe behavior rate (%)', fontsize=13)
    ax.set_title('Impact of Management Behavior on Worker Safety',
                 fontsize=15, fontweight='bold')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=11)
    ax.set_ylim(0, 105)

    os.makedirs('results', exist_ok=True)
    fig.tight_layout()
    fig.savefig('results/scenario_comparison.png', dpi=150)
    print("Saved: results/scenario_comparison.png")

    return results


if __name__ == '__main__':
    run_and_plot()
    plot_scenarios()