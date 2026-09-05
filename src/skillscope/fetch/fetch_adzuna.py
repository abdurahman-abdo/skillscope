import requests
from skillscope import (config, utils, matching)

raw_adzuna_path = config.RAW_DATA_PATH / "adzuna.json"

adzuna_app_id: str = config.ADZUNA_APP_ID
adzuna_app_key: str = config.ADZUNA_APP_KEY
ADZUNA_RESULTS_PER_PAGE: int = 5

def main():
    adzuna_countries: list[str] = [
        "us",
        "gb",
        "ca",
        "au",
        "de",
        "in"
    ]

    print("Retrieving data...")

    adzuna_raw_data: list = []
    for role in matching.TARGET_ROLES:
        for country in adzuna_countries:
            for page in range(1, 21, 2):
                print(f"Round: {-(-page // 2)} completed successfully for role: {role} in country: {country}.")
                jobs: list[dict] = fetch_jobs_from_adzuna(role, page, country, ADZUNA_RESULTS_PER_PAGE)
                adzuna_raw_data.extend(jobs)
    
    print("Data retrieved successfully.")
    print("Storing data with additional keys...")
    
    final_raw_adzuna: list = []
    
    for data in adzuna_raw_data:
        match_keys: dict = {
            "title": data['title'],
            "slug": data.get("category", {}).get("tag", "").replace("-", " "),
            "tags": data.get("category", {}).get("label", ""),
            "description": data['description'],
        }
        
        if matching.filter_matches(data, match_keys):
            final_raw_adzuna.append(data)

    utils.save_file(raw_adzuna_path, final_raw_adzuna)
    print(f"File with {len(final_raw_adzuna)} entries saved to {raw_adzuna_path}")

def fetch_jobs_from_adzuna(role: str, page: int, country: str, results_per_page: int) -> list[dict]:
    url: str = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"

    params: dict = {
        "app_id": adzuna_app_id,
        "app_key": adzuna_app_key,
        "what": role,
        "results_per_page": results_per_page
    }

    response = requests.get(url, params=params)

    response.raise_for_status()    

    data: dict = response.json()

    return data["results"]

if __name__ == "__main__":
    main()