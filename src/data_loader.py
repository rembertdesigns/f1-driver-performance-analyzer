import os
import fastf1

# Ensure cache folder exists
cache_dir = "cache"
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

# Output folder for race CSVs
output_dir = "data/sessions"
os.makedirs(output_dir, exist_ok=True)

# Use only years that FastF1 supports well (usually 2018–2024)
years = range(2018, 2025)

# Conservative list of common races
races = [
    "Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Australian Grand Prix",
    "Azerbaijan Grand Prix", "Spanish Grand Prix", "Monaco Grand Prix",
    "Canadian Grand Prix", "British Grand Prix", "Hungarian Grand Prix",
    "Belgian Grand Prix", "Dutch Grand Prix", "Italian Grand Prix",
    "Singapore Grand Prix", "Japanese Grand Prix", "United States Grand Prix",
    "Mexico City Grand Prix", "São Paulo Grand Prix", "Abu Dhabi Grand Prix"
]

for year in years:
    for race in races:
        try:
            session = fastf1.get_session(year, race, 'R')
            session.load()

            df = session.laps
            filename = f"{year}_{race.replace(' ', '_')}_RACE.csv"
            path = os.path.join(output_dir, filename)
            df.to_csv(path, index=False)

            print(f"✅ Saved {filename} with {len(df)} laps.")
        except Exception as e:
            print(f"❌ Failed: {year} {race} RACE | {e}")




