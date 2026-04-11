from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from perceptron_experiments import (
    dataset_statistics,
    make_separable_dataset,
    run_dimension_sweep,
    run_gamma_sweep,
    run_sanity_check,
    run_small_margin_sweep,
)


ROOT = Path(__file__).resolve().parent


def plot_gamma_sweep(rows: list[dict[str, float]], output_path: Path) -> None:
    x = [row["inv_margin_sq"] for row in rows]
    y = [row["avg_mistakes"] for row in rows]
    yerr = [row["std_mistakes"] for row in rows]
    bound = [row["theory_bound"] for row in rows]

    plt.figure(figsize=(7, 4.5))
    plt.errorbar(x, y, yerr=yerr, fmt="o-", capsize=4, label="Average mistakes")
    plt.plot(x, bound, "--", label=r"Theoretical bound $R^2 / \gamma^2$")
    plt.xlabel(r"$1 / \gamma^2$")
    plt.ylabel("Mistakes")
    plt.title("Perceptron Mistakes vs. $1 / \\gamma^2$")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def plot_dimension_sweep(rows: list[dict[str, float]], output_path: Path) -> None:
    x = [int(row["dimension"]) for row in rows]
    y = [row["avg_mistakes"] for row in rows]
    yerr = [row["std_mistakes"] for row in rows]

    plt.figure(figsize=(7, 4.5))
    plt.errorbar(x, y, yerr=yerr, fmt="o-", capsize=4)
    plt.xlabel("Dimension d")
    plt.ylabel("Mistakes")
    plt.title("Perceptron Mistakes vs. Dimension")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def print_table(title: str, rows: list[dict[str, float]], keys: list[str]) -> None:
    print(title)
    for row in rows:
        formatted = ", ".join(f"{key}={row[key]:.4f}" for key in keys)
        print(f"  {formatted}")
    print()


def main() -> None:
    gamma_values = [0.5, 0.35, 0.25, 0.2, 0.15, 0.1, 0.08, 0.05]
    dimension_values = [2, 5, 10, 20, 50, 100]
    small_gamma_values = [0.2, 0.1, 0.05, 0.02, 0.01]

    sanity = run_sanity_check()

    features, labels, separator = make_separable_dataset(
        n_samples=200, dimension=10, radius=1.0, margin=0.2, seed=0
    )
    stats = dataset_statistics(features, labels, separator)

    gamma_rows = run_gamma_sweep(gamma_values)
    dimension_rows = run_dimension_sweep(dimension_values)
    small_gamma_rows = run_small_margin_sweep(small_gamma_values)

    plot_gamma_sweep(gamma_rows, ROOT / "mistakes_vs_inv_gamma_sq.png")
    plot_dimension_sweep(dimension_rows, ROOT / "mistakes_vs_dimension.png")
    plot_gamma_sweep(small_gamma_rows, ROOT / "mistakes_vs_small_gamma.png")

    print("Sanity check")
    print(f"  mistakes={sanity['mistakes']:.0f}, epochs={sanity['epochs']:.0f}, accuracy={sanity['accuracy']:.3f}")
    print()

    print("Generator check")
    print(f"  max_norm={stats['max_norm']:.6f}, min_signed_margin={stats['min_signed_margin']:.6f}")
    print()

    print_table(
        "Gamma sweep",
        gamma_rows,
        ["margin", "inv_margin_sq", "avg_mistakes", "std_mistakes", "theory_bound"],
    )
    print_table(
        "Dimension sweep",
        dimension_rows,
        ["dimension", "avg_mistakes", "std_mistakes"],
    )
    print_table(
        "Small-margin sweep",
        small_gamma_rows,
        ["margin", "inv_margin_sq", "avg_mistakes", "std_mistakes", "theory_bound"],
    )


if __name__ == "__main__":
    main()
