from __future__ import annotations

from dataclasses import dataclass

import numpy as np


Array = np.ndarray


@dataclass
class PerceptronResult:
    weights: Array
    mistakes: int
    epochs: int


def _normalize(vector: Array) -> Array:
    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("Cannot normalize the zero vector.")
    return vector / norm


def _random_unit_vector(rng: np.random.Generator, dimension: int) -> Array:
    return _normalize(rng.normal(size=dimension))


def _random_unit_orthogonal(
    rng: np.random.Generator, direction: Array, dimension: int
) -> Array:
    candidate = rng.normal(size=dimension)
    candidate = candidate - np.dot(candidate, direction) * direction
    return _normalize(candidate)


def make_separable_dataset(
    n_samples: int,
    dimension: int,
    radius: float,
    margin: float,
    seed: int = 0,
) -> tuple[Array, Array, Array]:
    if dimension < 2:
        raise ValueError("dimension must be at least 2 for this generator.")
    if not 0 < margin < radius:
        raise ValueError("Expected 0 < margin < radius.")

    rng = np.random.default_rng(seed)
    separator = _random_unit_vector(rng, dimension)
    orth_scale = np.sqrt(radius**2 - margin**2)

    labels = rng.choice(np.array([-1.0, 1.0]), size=n_samples)
    features = np.empty((n_samples, dimension), dtype=float)

    for i, label in enumerate(labels):
        orth_dir = _random_unit_orthogonal(rng, separator, dimension)
        features[i] = label * margin * separator + orth_scale * orth_dir

    return features, labels, separator


def dataset_statistics(features: Array, labels: Array, separator: Array) -> dict[str, float]:
    norms = np.linalg.norm(features, axis=1)
    signed_margins = labels * (features @ separator)
    return {
        "max_norm": float(np.max(norms)),
        "min_signed_margin": float(np.min(signed_margins)),
    }


def perceptron_train(
    features: Array,
    labels: Array,
    max_epochs: int = 10_000,
) -> PerceptronResult:
    n_samples, dimension = features.shape
    weights = np.zeros(dimension, dtype=float)
    mistakes = 0

    for epoch in range(1, max_epochs + 1):
        updates_this_epoch = 0
        for i in range(n_samples):
            if labels[i] * np.dot(weights, features[i]) <= 0:
                weights = weights + labels[i] * features[i]
                mistakes += 1
                updates_this_epoch += 1
        if updates_this_epoch == 0:
            return PerceptronResult(weights=weights, mistakes=mistakes, epochs=epoch)

    raise RuntimeError("Perceptron did not converge within max_epochs.")


def run_gamma_sweep(
    margins: list[float],
    n_samples: int = 200,
    dimension: int = 10,
    radius: float = 1.0,
    seeds: list[int] | None = None,
) -> list[dict[str, float]]:
    seeds = seeds or [0, 1, 2, 3, 4]
    rows: list[dict[str, float]] = []

    for margin in margins:
        mistake_counts = []
        bounds = []
        for seed in seeds:
            features, labels, separator = make_separable_dataset(
                n_samples=n_samples,
                dimension=dimension,
                radius=radius,
                margin=margin,
                seed=seed,
            )
            stats = dataset_statistics(features, labels, separator)
            result = perceptron_train(features, labels)
            mistake_counts.append(result.mistakes)
            bounds.append((stats["max_norm"] ** 2) / (stats["min_signed_margin"] ** 2))

        rows.append(
            {
                "margin": margin,
                "inv_margin_sq": 1.0 / (margin**2),
                "avg_mistakes": float(np.mean(mistake_counts)),
                "std_mistakes": float(np.std(mistake_counts)),
                "theory_bound": float(np.mean(bounds)),
            }
        )

    return rows


def run_dimension_sweep(
    dimensions: list[int],
    n_samples: int = 200,
    radius: float = 1.0,
    margin: float = 0.2,
    seeds: list[int] | None = None,
) -> list[dict[str, float]]:
    seeds = seeds or [0, 1, 2, 3, 4]
    rows: list[dict[str, float]] = []

    for dimension in dimensions:
        mistake_counts = []
        for seed in seeds:
            features, labels, _ = make_separable_dataset(
                n_samples=n_samples,
                dimension=dimension,
                radius=radius,
                margin=margin,
                seed=seed,
            )
            result = perceptron_train(features, labels)
            mistake_counts.append(result.mistakes)

        rows.append(
            {
                "dimension": float(dimension),
                "avg_mistakes": float(np.mean(mistake_counts)),
                "std_mistakes": float(np.std(mistake_counts)),
            }
        )

    return rows


def run_small_margin_sweep(
    margins: list[float],
    n_samples: int = 200,
    dimension: int = 10,
    radius: float = 1.0,
    seeds: list[int] | None = None,
) -> list[dict[str, float]]:
    return run_gamma_sweep(
        margins=margins,
        n_samples=n_samples,
        dimension=dimension,
        radius=radius,
        seeds=seeds,
    )


def run_sanity_check() -> dict[str, float]:
    features = np.array(
        [
            [2.0, 1.0],
            [1.0, 2.0],
            [-2.0, -1.0],
            [-1.0, -2.0],
        ]
    )
    labels = np.array([1.0, 1.0, -1.0, -1.0])
    result = perceptron_train(features, labels)
    predictions = np.sign(features @ result.weights)
    accuracy = np.mean(predictions == labels)
    return {
        "mistakes": float(result.mistakes),
        "epochs": float(result.epochs),
        "accuracy": float(accuracy),
    }
