"""
=============================================================================
IT3101 - Data Warehousing & Business Intelligence (DWBI)
Project: Global Airline Route & Revenue Analytics Solution (2010-2026)
Script: download_datasets.py
Description: Automated data acquisition script using Kaggle API to download,
             authenticate, extract, and organize all operational & analytical
             datasets up to 2026.
=============================================================================
"""

import os
import shutil
import sys
from pathlib import Path

# Step 1: Ensure Kaggle credentials are configured
def setup_kaggle_credentials(project_dir: Path) -> None:
    kaggle_json_project = project_dir / "kaggle.json"
    user_kaggle_dir = Path.home() / ".kaggle"
    user_kaggle_json = user_kaggle_dir / "kaggle.json"

    if not user_kaggle_json.exists():
        if kaggle_json_project.exists():
            user_kaggle_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(kaggle_json_project, user_kaggle_json)
            # Set restrictive permissions on Linux/macOS; on Windows file is copied
            try:
                os.chmod(user_kaggle_json, 0o600)
            except Exception:
                pass
            print(f"[OK] Kaggle credentials copied from {kaggle_json_project} to {user_kaggle_json}")
        else:
            print("[ERROR] kaggle.json not found in project root or ~/.kaggle directory.")
            print("Please place your kaggle.json file in the project folder.")
            sys.exit(1)
    else:
        print(f"[OK] Kaggle credentials found at {user_kaggle_json}")


# Step 2: Download datasets using Kaggle API
def download_all_datasets(project_dir: Path) -> None:
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    print("[OK] Successfully authenticated with Kaggle API.")

    data_dir = project_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Datasets catalog for Global Airline Route & Revenue DWBI Solution
    datasets = [
        {
            "id": "sergionefedov/global-aviation-industry-2010-2026",
            "target_dir": data_dir / "global_aviation_2010_2026",
            "description": "Global Aviation Industry (2010-2026) - Multi-year financial, route, regional traffic & fleet orders",
        },
        {
            "id": "waleedfaheem/airline-route-profitability-and-cost-analysis",
            "target_dir": data_dir / "route_profitability",
            "description": "Airline Route Profitability & Cost Breakdown (Flight-level OLTP operational logs)",
        },
        {
            "id": "ahmadrafiee/airports-airlines-planes-and-routes-update-2024",
            "target_dir": data_dir / "airports_airlines_planes",
            "description": "Global Master Dimension Tables (Airports, Airlines, Aircraft Models, and Routes)",
        },
    ]

    for item in datasets:
        dataset_id = item["id"]
        target = item["target_dir"]
        desc = item["description"]

        target.mkdir(parents=True, exist_ok=True)
        print(f"\n--- Downloading: {desc} ---")
        print(f"Dataset Slug: {dataset_id}")
        print(f"Target Directory: {target}")

        try:
            api.dataset_download_files(dataset_id, path=str(target), unzip=True)
            print(f"[SUCCESS] Downloaded and unzipped: {dataset_id}")
        except Exception as e:
            print(f"[FAILED] Error downloading {dataset_id}: {e}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    print("=" * 70)
    print("DWBI Solution: Global Airline Route & Revenue Analytics")
    print(f"Project Working Directory: {project_root}")
    print("=" * 70)

    setup_kaggle_credentials(project_root)
    download_all_datasets(project_root)

    print("\n" + "=" * 70)
    print("[COMPLETED] All datasets have been acquired and organized in /data.")
    print("=" * 70)
