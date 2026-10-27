from pathlib import Path
import pandas as pd

# Locate the project and dataset folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

# Find CSV files
csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    print("ERROR: No CSV file found in the data folder.")
    print(f"Please check this folder: {DATA_DIR}")
else:
    for csv_file in csv_files:
        print("\n" + "=" * 60)
        print(f"FILE: {csv_file.name}")
        print("=" * 60)

        try:
            df = pd.read_csv(csv_file, encoding="utf-8")

            print("\nDataset shape:", df.shape)

            print("\nColumn names:")
            print(df.columns.tolist())

            print("\nFirst 5 rows:")
            print(df.head().to_string())

            print("\nMissing values:")
            print(df.isnull().sum())

        except Exception as error:
            print(f"Could not read this file: {error}")