import pandas as pd
import numpy as np
from pathlib import Path

# Create directory structure
profile_dir = Path("hybrid_renewable_pypsa/data/profiles/grid_profiles")
metadata_path = Path("hybrid_renewable_pypsa/data/metadata/grid_profiles_metadata.csv")
profile_dir.mkdir(parents=True, exist_ok=True)
metadata_path.parent.mkdir(parents=True, exist_ok=True)

# Configuration parameters
START_DATE = "2024-01-01 00:00:00"
HOURS = 24
DAYS = 7
TIMES = pd.date_range(START_DATE, periods=HOURS * DAYS, freq="h", tz="UTC")
TIME_ZONE = "UTC+00"

def generate_grid_import_profile():
    """Generate grid import profile (p.u.) with demand variation"""
    daily_curve = np.array([
        0.5, 0.4, 0.3, 0.2, 0.2, 0.3, 0.6, 0.8,
        1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.6, 0.7,
        0.8, 0.9, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5
    ])
    base = 1.0  # Normalized to 1.0
    noise_level = 0.05
    profile = np.tile(daily_curve, DAYS)
    noise = np.random.normal(0, noise_level, len(profile))
    return np.clip(base * profile + noise, 0, 1)

# Generate profile
grid_import_profile = generate_grid_import_profile()

# Save grid_import_p_max_pu.csv
grid_import_df = pd.DataFrame({
    "time": TIMES.strftime("%Y-%m-%d %H:%M:%S"),
    "p_max_pu": np.round(grid_import_profile, 4)  # p.u.
})
grid_import_df.to_csv(profile_dir / "grid_import_p_max_pu.csv", index=False)

# Generate metadata file
grid_metadata = pd.DataFrame([
    {"profile_name": "grid_import_p_max_pu.csv", "description": "Grid import profile with daily demand variations.",
     "source": "Synthetic model", "time_resolution": "Hourly", "time_zone": TIME_ZONE}
])
grid_metadata.to_csv(metadata_path, index=False)

print("Successfully generated:")
print("- grid_import_p_max_pu.csv in", profile_dir)
print("- grid_profiles_metadata.csv in", metadata_path)
