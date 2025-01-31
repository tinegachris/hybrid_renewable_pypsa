import pandas as pd
import numpy as np
from pathlib import Path

# Create directory structure
Path("data/load_profiles").mkdir(parents=True, exist_ok=True)

# Configuration parameters
START_DATE = "2024-01-01 00:00:00"
HOURS = 24
DAYS = 7
TIMES = pd.date_range(START_DATE, periods=HOURS*DAYS, freq="h", tz="UTC")
POWER_FACTOR = 0.9  # Applies to all load types
BASE_VOLTAGE = 0.415  # kV (415V system)
TIME_ZONE = "UTC+00"

def add_daily_pattern(base_load, daily_curve, noise_level=0.1):
    """Add daily pattern with noise"""
    daily = base_load * daily_curve
    noise = np.random.normal(0, noise_level * base_load, len(daily))
    return np.clip(daily + noise, 0, None)

def residential_load_profile():
    """Generate residential load profile (MW) with morning/evening peaks"""
    base = 0.2  # 200 kW base load
    daily_curve = np.array([
        0.6, 0.5, 0.4, 0.4, 0.5, 0.6, 1.0, 1.2,
        0.8, 0.7, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0,
        1.4, 1.6, 1.8, 2.0, 1.6, 1.4, 1.2, 1.0
    ])
    p_set = add_daily_pattern(base, daily_curve, 0.15)
    q_set = p_set * np.tan(np.arccos(POWER_FACTOR))
    return np.tile(p_set, DAYS), np.tile(q_set, DAYS)

def commercial_load_profile():
    """Generate commercial load profile (MW) with daytime peak"""
    base = 0.3  # 300 kW base load
    daily_curve = np.array([
        0.3, 0.3, 0.3, 0.3, 0.4, 0.5, 0.8, 1.0,
        1.2, 1.4, 1.5, 1.6, 1.6, 1.7, 1.7, 1.6,
        1.4, 1.2, 0.8, 0.6, 0.4, 0.3, 0.3, 0.3
    ])
    p_set = add_daily_pattern(base, daily_curve, 0.1)
    q_set = p_set * np.tan(np.arccos(POWER_FACTOR))
    return np.tile(p_set, DAYS), np.tile(q_set, DAYS)

def industrial_load_profile():
    """Generate industrial load profile (MW) with continuous operation"""
    base = 0.4  # 400 kW base load
    daily_curve = np.array([
        0.8, 0.8, 0.8, 0.8, 1.0, 1.0, 1.0, 1.0,
        1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2,
        1.0, 1.0, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8
    ])
    p_set = add_daily_pattern(base, daily_curve, 0.05)
    q_set = p_set * np.tan(np.arccos(POWER_FACTOR))
    return np.tile(p_set, DAYS), np.tile(q_set, DAYS)

# Profile metadata descriptions
PROFILE_METADATA = {
    "residential_1": "Residential area 1",
    "residential_2": "Residential area 2",
    "residential_3": "Suburban housing",
    "residential_4": "Urban apartments",
    "commercial_1": "Commercial complex A",
    "commercial_2": "Shopping district",
    "commercial_3": "Office park",
    "industrial_1": "Factory zone 1",
    "industrial_2": "Factory zone 2",
    "industrial_3": "Processing plant"
}

# Generate profiles and metadata
metadata_records = []
profiles = {
    # Residential (4 profiles)
    **{f"residential_{i+1}": residential_load_profile() for i in range(4)},
    
    # Commercial (3 profiles)
    **{f"commercial_{i+1}": commercial_load_profile() for i in range(3)},
    
    # Industrial (3 profiles)
    **{f"industrial_{i+1}": industrial_load_profile() for i in range(3)}
}

# Save profiles and collect metadata
for profile_id, (p_set, q_set) in profiles.items():
    # Create profile CSV
    df = pd.DataFrame({
        "time": TIMES.strftime("%Y-%m-%d %H:%M:%S"),
        "p_set": np.round(p_set, 4),  # MW
        "q_set": np.round(q_set, 4)   # MVAr
    })
    
    # Add header comment
    csv_header = (f"# time [{TIME_ZONE}], p_set [MW], q_set [MVAR] "
                  f"(power_factor={POWER_FACTOR})\n")
    Path(f"hybrid_renewable_pypsa/data/load_profiles/{profile_id}.csv").write_text(csv_header + df.to_csv(index=False))
    
    # Add metadata
    load_type = profile_id.split("_")[0]
    metadata_records.append({
        "profile_id": profile_id,
        "load_type": load_type,
        "voltage_kV": BASE_VOLTAGE,
        "time_zone": TIME_ZONE,
        "power_factor": POWER_FACTOR,
        "data_source": "synthetic",
        "description": PROFILE_METADATA[profile_id]
    })

# Save metadata file
pd.DataFrame(metadata_records).to_csv("hybrid_renewable_pypsa/data/load_profiles_metadata.csv", index=False)

print("Successfully generated:")
print(f"- {len(profiles)} load profiles in hybrid_renewable_pypsa/data/load_profiles/")
print("- Metadata file: hybrid_renewable_pypsa/data/load_profiles_metadata.csv")