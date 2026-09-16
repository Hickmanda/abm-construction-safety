"""
Batch experiments with confidence band visualization.

Usage:
    python -m src.batch --seeds 20
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.model import SafetyModel


def run_batch(num_seeds=20, num_workers=100, num_managers=3, steps=100):
    """Run the simulation for multiple seeds."""
    print(f"Running {num_seeds} seeds "
          f"({num_workers} workers x {steps} days)...")

    all_histories = np.zeros((num_seeds, steps))

    for seed in range(num_seeds):
        model = SafetyModel(
            num_workers=num_workers,
            num_managers=num_managers,
            seed=seed,
        )
        model.run(steps=steps)
        all_histories[seed] = model.safety_rate_history
        print(f"  Seed {seed:2d}: final = "
              f"{model.safety_rate_history[-1]:.2%}")

    return all_histories


def plot_confidence_band(histories, output_path='results/batch_analysis.png'):
    """Plot the mean trajectory with a ± 1 std band."""
    num_seeds, steps = histories.shape
    days = np.arange(1, steps + 1)

    mean = histories.mean(axis=0) * 100
    std = histories.std(axis=0) * 100

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(days, mean, color='#007bff', linewidth=2.5,
            label=f'Mean over {num_seeds} seeds')
    ax.fill_between(days, mean - std, mean + std,
                    color='#007bff', alpha=0.20, label='+/- 1 std')
    ax.axhline(y=90.4, color='red', linestyle='--',
               label='Zhang et al. (2025): 90.4%')

    final_mean = mean[-1]
    ax.axhline(y=final_mean, color='green', linestyle=':',
               alpha=0.7, label=f'Final mean: {final_mean:.1f}%')

    ax.set_xlabel('Day', fontsize=13)
    ax.set_ylabel('Safe behavior rate (%)', fontsize=13)
    ax.set_title(f'Batch Analysis: Mean +/- Std over {num_seeds} Seeds',
                 fontsize=15, fontweight='bold')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=11, loc='lower right')
    ax.set_ylim(0, 105)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"\nSaved: {output_path}")

    return mean, std


def plot_final_distribution(histories,
                            output_path='results/final_rates_hist.png'):
    """Histogram of the final safe rates."""
    final_rates = histories[:, -1] * 100

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(final_rates, bins=10, color='#28a745',
            edgecolor='black', alpha=0.8)
    ax.axvline(x=90.4, color='red', linestyle='--',
               label='Zhang et al. (2025): 90.4%')
    ax.axvline(x=final_rates.mean(), color='black', linestyle='-',
               alpha=0.7, label=f'Mean: {final_rates.mean():.1f}%')

    ax.set_xlabel('Final safe rate (%)', fontsize=13)
    ax.set_ylabel('Number of seeds', fontsize=13)
    ax.set_title('Distribution of Final Safe Rates',
                 fontsize=15, fontweight='bold')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=11)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Batch experiments with confidence bands'
    )
    parser.add_argument('--seeds', type=int, default=20)
    parser.add_argument('--workers', type=int, default=100)
    parser.add_argument('--managers', type=int, default=3)
    parser.add_argument('--days', type=int, default=100)
    args = parser.parse_args()

    histories = run_batch(
        num_seeds=args.seeds,
        num_workers=args.workers,
        num_managers=args.managers,
        steps=args.days,
    )

    plot_confidence_band(histories)
    plot_final_distribution(histories)

    print("\n" + "=" * 60)
    print("Batch Summary")
    print("=" * 60)
    final_rates = histories[:, -1] * 100
    print(f"  Seeds:            {args.seeds}")
    print(f"  Mean final rate:  {final_rates.mean():.2f}%")
    print(f"  Std:              {final_rates.std():.2f}%")
    print(f"  Min / Max:        {final_rates.min():.2f}% / {final_rates.max():.2f}%")
    print("  Paper reference:  90.4%")


if __name__ == '__main__':
    main()