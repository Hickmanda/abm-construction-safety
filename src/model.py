"""
Mesa-based model for the ABM simulation.
Based on Zhang et al. (2025, ASCE JCEM).
"""

import mesa
import random

from src.agents import Worker, Manager


class SafetyModel(mesa.Model):
    """Construction site safety model."""

    def __init__(self, num_workers=100, num_managers=3, seed=None):
        super().__init__(seed=seed)

        self.rng = random.Random(seed)
        self.num_workers = num_workers
        self.num_managers = num_managers

        self.workers = [
            Worker(worker_id=i, rng=self.rng)
            for i in range(num_workers)
        ]

        self.managers = [
            Manager(manager_id=i, rng=self.rng)
            for i in range(num_managers)
        ]

        self.safety_rate_history = []
        self.avg_SA_history = []
        self.avg_SK_history = []
        self.avg_reference_point_history = []

        self.smoothed_rate = None
        self.prev_smoothed_rate = None

        self.step_count = 0

    def step(self):
        """One day of simulation."""
        decisions = []
        for w in self.workers:
            w.update_behavior_attributes()
            result = w.decide()
            decisions.append(result['behavior'])

        safety_rate = sum(decisions) / len(decisions)

        if self.smoothed_rate is None:
            self.smoothed_rate = safety_rate
            self.prev_smoothed_rate = safety_rate
        else:
            self.prev_smoothed_rate = self.smoothed_rate
            self.smoothed_rate = 0.2 * safety_rate + 0.8 * self.smoothed_rate

        for m in self.managers:
            m.update_behaviors(self.prev_smoothed_rate, self.smoothed_rate)

        if self.managers:
            team_ET = sum(m.ET for m in self.managers) / len(self.managers)
            team_IR = sum(m.IR for m in self.managers) / len(self.managers)
            team_SI = sum(m.SI for m in self.managers) / len(self.managers)
            team_SM = sum(m.SM for m in self.managers) / len(self.managers)
            team_HEM = sum(m.HEM for m in self.managers) / len(self.managers)

            team = Manager(manager_id=-1, rng=self.rng)
            team.ET, team.IR, team.SI, team.SM, team.HEM = (
                team_ET, team_IR, team_SI, team_SM, team_HEM
            )

            for w in self.workers:
                team.apply_to_worker(w)

        self.safety_rate_history.append(safety_rate)
        self.avg_SA_history.append(
            sum(w.SA for w in self.workers) / len(self.workers)
        )
        self.avg_SK_history.append(
            sum(w.SK for w in self.workers) / len(self.workers)
        )
        self.avg_reference_point_history.append(
            sum(w.reference_point for w in self.workers) / len(self.workers)
        )

        self.step_count += 1

    def run(self, steps=100):
        for _ in range(steps):
            self.step()


if __name__ == '__main__':
    print("=" * 60)
    print("Safety Model — 100 workers x 3 managers x 100 days")
    print("=" * 60)

    model = SafetyModel(num_workers=100, num_managers=3, seed=42)
    model.run(steps=100)

    print(f"\nInitial safety rate: {model.safety_rate_history[0]:.2%}")
    print(f"Final safety rate:   {model.safety_rate_history[-1]:.2%}")