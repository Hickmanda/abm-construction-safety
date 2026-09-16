"""
Command-line interface for the ABM simulation.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.model import SafetyModel


def parse_args():
    parser = argparse.ArgumentParser(
        description='Agent-Based Simulation of Construction Worker Safety',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--workers', type=int, default=100)
    parser.add_argument('--managers', type=int, default=3)
    parser.add_argument('--days', type=int, default=100)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--batch', type=int, default=0)
    return parser.parse_args()


def run_single(args):
    print("=" * 60)
    print(f"Single run: {args.workers} workers x {args.managers} managers "
          f"x {args.days} days (seed={args.seed})")
    print("=" * 60)

    model = SafetyModel(
        num_workers=args.workers,
        num_managers=args.managers,
        seed=args.seed,
    )
    model.run(steps=args.days)

    print(f"\nInitial safe rate: {model.safety_rate_history[0]:.2%}")
    print(f"Final safe rate:   {model.safety_rate_history[-1]:.2%}")
    print("Target (paper):    90.4%")


def run_batch(args):
    import numpy as np

    print("=" * 60)
    print(f"Batch run: {args.batch} seeds x {args.workers} workers "
          f"x {args.days} days")
    print("=" * 60)

    final_rates = []
    for seed in range(args.batch):
        model = SafetyModel(
            num_workers=args.workers,
            num_managers=args.managers,
            seed=seed,
        )
        model.run(steps=args.days)
        rate = model.safety_rate_history[-1]
        final_rates.append(rate)
        print(f"  Seed {seed}: final safe rate = {rate:.2%}")

    arr = np.array(final_rates)
    print("\n" + "=" * 60)
    print("Batch Summary")
    print("=" * 60)
    print(f"  Mean final safe rate:   {arr.mean():.2%}")
    print(f"  Std deviation:          {arr.std():.2%}")
    print(f"  Min / Max:              {arr.min():.2%} / {arr.max():.2%}")
    print("  Paper reference:        90.4%")


def main():
    args = parse_args()
    if args.batch > 0:
        run_batch(args)
    else:
        run_single(args)


if __name__ == '__main__':
    main()