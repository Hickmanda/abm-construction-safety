"""
Creates an animated GIF showing the evolution of worker behavior
over time.

Each frame = one day. Dots represent workers:
    green = safe, red = unsafe.
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import numpy as np

from src.model import SafetyModel


def create_animation(num_workers=200, steps=80, seed=42,
                     output_path='results/simulation.gif'):
    """Create the animation."""

    print(f"Generating animation: {num_workers} workers x {steps} days...")

    # Seed positions (fixed for the whole animation)
    np.random.seed(seed)
    xs = np.random.rand(num_workers)
    ys = np.random.rand(num_workers)

    # Run the model
    model = SafetyModel(num_workers=num_workers, num_managers=3, seed=seed)

    # Frame data: for each day, record each worker's behavior
    frames = []

    for _ in range(steps):
        model.step()
        behaviors = []
        for w in model.workers:
            if w.behavior_history:
                behaviors.append(w.behavior_history[-1])
            else:
                behaviors.append(0)
        frames.append(np.array(behaviors))

    # Setup the figure
    fig, (ax_dots, ax_line) = plt.subplots(
        1, 2, figsize=(12, 5),
        gridspec_kw={'width_ratios': [1, 1.5]},
    )

    def update(frame_idx):
        ax_dots.clear()
        ax_line.clear()

        behaviors = frames[frame_idx]
        colors = ['#28a745' if b == 1 else '#dc3545' for b in behaviors]

        ax_dots.scatter(xs, ys, c=colors, s=40, alpha=0.8,
                        edgecolors='black', linewidths=0.5)
        ax_dots.set_xlim(-0.05, 1.05)
        ax_dots.set_ylim(-0.05, 1.05)
        ax_dots.set_xticks([])
        ax_dots.set_yticks([])
        ax_dots.set_title(
            f"Day {frame_idx + 1} — "
            f"Safe: {behaviors.sum()}/{len(behaviors)} "
            f"({behaviors.mean():.0%})",
            fontsize=13, fontweight='bold',
        )

        ax_dots.scatter([], [], c='#28a745', s=60, label='Safe')
        ax_dots.scatter([], [], c='#dc3545', s=60, label='Unsafe')
        ax_dots.legend(loc='lower right', fontsize=10)

        rates = [f.mean() * 100 for f in frames[:frame_idx + 1]]
        ax_line.plot(range(1, len(rates) + 1), rates,
                     color='#007bff', linewidth=2.5)
        ax_line.axhline(y=90.4, color='red', linestyle='--',
                        label='Zhang et al. (2025): 90.4%')
        ax_line.set_xlim(1, steps)
        ax_line.set_ylim(0, 105)
        ax_line.set_xlabel("Day", fontsize=12)
        ax_line.set_ylabel("Safe behavior rate (%)", fontsize=12)
        ax_line.set_title("Progress", fontsize=13, fontweight='bold')
        ax_line.grid(alpha=0.3)
        ax_line.legend(fontsize=10, loc='lower right')

        plt.tight_layout()

    anim = animation.FuncAnimation(
        fig, update, frames=steps, interval=150, repeat=True,
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    anim.save(output_path, writer='pillow', fps=6, dpi=100)
    plt.close()

    print(f"Saved: {output_path}")


if __name__ == '__main__':
    create_animation()
