import pandas as pd
import numpy as np
from pathlib import Path

# Create directory structure
Path("data/load_profiles").mkdir(parents=True, exist_ok=True)

# Common parameters
START_DATE = "2024-01-01"
HOURS = 24
DAYS = 1  # One week of data
TIMES = pd.date_range(START_DATE, periods=HOURS*DAYS, freq="h")
POWER_FACTOR = 0.9  # For calculating reactive power from active power

def add_daily_pattern(base_load, daily_curve, noise_level=0.1):
    """Add daily pattern with noise"""
    daily = base_load * daily_curve
    noise = np.random.normal(0, noise_level * base_load, len(daily))
    return np.clip(daily + noise, 0, None)

def residential_load_profile():
    """Generate residential load profile with morning/evening peaks"""
    base = 200  # Base load in kW
    daily_curve = np.array([
        0.6, 0.5, 0.4, 0.4,  # Midnight-4AM
        0.5, 0.6, 1.0, 1.2,  # 4AM-8AM (morning peak)
        0.8, 0.7, 0.6, 0.6,  # 8AM-12PM
        0.7, 0.8, 0.9, 1.0,  # 12PM-4PM
        1.4, 1.6, 1.8, 2.0,  # 4PM-8PM (evening peak)
        1.6, 1.4, 1.2, 1.0   # 8PM-Midnight
    ])
    p_set = add_daily_pattern(base, daily_curve, 0.15)
    q_set = p_set * np.tan(np.arccos(POWER_FACTOR))
    p_set_week = np.tile(p_set, DAYS)
    q_set_week = np.tile(q_set, DAYS)
    return p_set_week, q_set_week

def commercial_load_profile():
    """Generate commercial load profile with daytime peak"""
    base = 300  # Base load in kW
    daily_curve = np.array([
        0.3, 0.3, 0.3, 0.3,  # Midnight-4AM
        0.4, 0.5, 0.8, 1.0,  # 4AM-8AM
        1.2, 1.4, 1.5, 1.6,  # 8AM-12PM
        1.6, 1.7, 1.7, 1.6,  # 12PM-4PM (peak)
        1.4, 1.2, 0.8, 0.6,  # 4PM-8PM
        0.4, 0.3, 0.3, 0.3   # 8PM-Midnight
    ])
    p_set = add_daily_pattern(base, daily_curve, 0.1)
    q_set = p_set * np.tan(np.arccos(POWER_FACTOR))
    p_set_week = np.tile(p_set, DAYS)
    q_set_week = np.tile(q_set, DAYS)
    return p_set_week, q_set_week

def industrial_load_profile():
    """Generate industrial load profile with shift patterns"""
    base = 400  # Base load in kW
    daily_curve = np.array([
        0.8, 0.8, 0.8, 0.8,  # Midnight-4AM
        1.0, 1.0, 1.0, 1.0,  # 4AM-8AM
        1.2, 1.2, 1.2, 1.2,  # 8AM-12PM
        1.2, 1.2, 1.2, 1.2,  # 12PM-4PM
        1.0, 1.0, 0.8, 0.8,  # 4PM-8PM
        0.8, 0.8, 0.8, 0.8   # 8PM-Midnight
    ])
    p_set = add_daily_pattern(base, daily_curve, 0.05)
    q_set = p_set * np.tan(np.arccos(0.85))  # Industrial power factor
    return p_set, q_set

# Generate and save profiles
profiles = {
    # Residential
    "residential_1": residential_load_profile(),
    "residential_2": residential_load_profile(),
    "residential_3": residential_load_profile(),
    "residential_4": residential_load_profile(),
    
    # Commercial
    "commercial_1": commercial_load_profile(),
    "commercial_2": commercial_load_profile(),
    "commercial_3": commercial_load_profile(),
    
    # Industrial
    "industrial_1": industrial_load_profile(),
    "industrial_2": industrial_load_profile(),
    "industrial_3": industrial_load_profile()
}

for profile_id, (p_set, q_set) in profiles.items():
    if len(TIMES) == len(p_set) == len(q_set):
        df = pd.DataFrame({
            "time": TIMES,
            "p_set": np.round(p_set, 1),
            "q_set": np.round(q_set, 1)
        })
    else:
        raise ValueError(f"Length mismatch: TIMES({len(TIMES)}), p_set({len(p_set)}), q_set({len(q_set)})")
    df.to_csv(f"data/load_profiles/{profile_id}.csv", index=False)

print("Generated load profiles:")
print("\n".join(f"- data/load_profiles/{id}.csv" for id in profiles.keys()))