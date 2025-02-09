import pandas as pd
import numpy as np
from pathlib import Path

# Create directory structure
profile_dir = Path("hybrid_renewable_pypsa/data/profiles/generator_profiles")
metadata_path = Path("hybrid_renewable_pypsa/data/metadata/generator_profiles_metadata.csv")
profile_dir.mkdir(parents=True, exist_ok=True)
metadata_path.parent.mkdir(parents=True, exist_ok=True)

# Configuration parameters
START_DATE = "2024-01-01 00:00:00"
HOURS = 24
DAYS = 7
TIMES = pd.date_range(START_DATE, periods=HOURS * DAYS, freq="h", tz="UTC")
TIME_ZONE = "UTC+00"

def generate_solar_profile():
    """Generate solar generation profile (p.u.) with diurnal pattern"""
    daily_curve = np.array([
        0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.5, 0.7,
        0.9, 1.0, 0.9, 0.7, 0.5, 0.3, 0.1, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ])
    base = 1.0  # Max generation is normalized to 1.0
    noise_level = 0.05
    profile = np.tile(daily_curve, DAYS)
    noise = np.random.normal(0, noise_level, len(profile))
    return np.clip(base * profile + noise, 0, 1)

def generate_hydro_profile():
    """Generate hydro generation profile (p.u.) with consistent availability"""
    base = 1.0  # Hydro generation is typically stable
    variation = 0.05  # Minor variations over time
    profile = np.ones(HOURS * DAYS) * base
    noise = np.random.normal(0, variation, len(profile))
    return np.clip(profile + noise, 0, 1)

# Generate profiles
solar_profile = generate_solar_profile()
hydro_profile = generate_hydro_profile()

# Save solar-p_max_pu.csv
solar_df = pd.DataFrame({
    "time": TIMES.strftime("%Y-%m-%d %H:%M:%S"),
    "p_max_pu": np.round(solar_profile, 4)  # p.u.
})
solar_df.to_csv(profile_dir / "solar-p_max_pu.csv", index=False)

# Save hydro-p_max_pu.csv
hydro_df = pd.DataFrame({
    "time": TIMES.strftime("%Y-%m-%d %H:%M:%S"),
    "p_max_pu": np.round(hydro_profile, 4)  # p.u.
})
hydro_df.to_csv(profile_dir / "hydro-p_max_pu.csv", index=False)

# Generate metadata file
generator_metadata = pd.DataFrame([
    {"profile_name": "solar-p_max_pu.csv", "description": "Solar generation profile with diurnal variation.",
     "source": "Synthetic model", "time_resolution": "Hourly", "time_zone": TIME_ZONE},
    {"profile_name": "hydro-p_max_pu.csv", "description": "Hydro generation profile with stable output and minor variations.",
     "source": "Synthetic model", "time_resolution": "Hourly", "time_zone": TIME_ZONE}
])
generator_metadata.to_csv(metadata_path, index=False)

print("Successfully generated:")
print("- solar-p_max_pu.csv in", profile_dir)
print("- hydro-p_max_pu.csv in", profile_dir)
print("- generator_profiles_metadata.csv in", metadata_path)
