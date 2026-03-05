"""
Utilities - Các hàm tiện ích chung
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Any
import json
import os


def load_csv(filepath: str) -> pd.DataFrame:
    """Load CSV file"""
    return pd.read_csv(filepath)


def save_csv(df: pd.DataFrame, filepath: str):
    """Save DataFrame to CSV"""
    df.to_csv(filepath, index=False)


def load_json(filepath: str) -> dict:
    """Load JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(data: dict, filepath: str):
    """Save dict to JSON"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def save_features(features: np.ndarray, filepath: str):
    """Lưu features dạng .npy"""
    np.save(filepath, features)


def load_features(filepath: str) -> np.ndarray:
    """Load features từ .npy"""
    return np.load(filepath)


def normalize(data: np.ndarray) -> np.ndarray:
    """Min-Max Normalization"""
    min_val = np.min(data, axis=0)
    max_val = np.max(data, axis=0)
    return (data - min_val) / (max_val - min_val + 1e-8)


def standardize(data: np.ndarray) -> np.ndarray:
    """Standardization (Z-score)"""
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    return (data - mean) / (std + 1e-8)


def train_val_test_split(
    X: np.ndarray,
    y: np.ndarray,
    val_size: float = 0.2,
    test_size: float = 0.2,
    random_state: int = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Chia dữ liệu thành train/val/test"""
    if random_state:
        np.random.seed(random_state)

    n = len(y)
    indices = np.random.permutation(n)

    test_idx = indices[:int(n * test_size)]
    val_idx = indices[int(n * test_size):int(n * (test_size + val_size))]
    train_idx = indices[int(n * (test_size + val_size)):]

    return (
        X[train_idx], X[val_idx], X[test_idx],
        y[train_idx], y[val_idx], y[test_idx]
    )
