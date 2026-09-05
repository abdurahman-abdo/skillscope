import requests
from skillscope import (config, utils, matching)

raw_muse_path = config.RAW_DATA_PATH / "muse.json"

def main() -> None:
    muse_countries: list[str] = [
        "United States",
        "Canada",
        "United Kingdom",
        "Germany",
        "France",
        "Netherlands",
        "Australia",
        "India"
    ]

    muse_raw_data: list = []
    
    for country in muse_countries:
        for page in range(100):
            data: list[dict] = fetch_from_muse(page, country)
            muse_raw_data.extend(data)

    print(f"Fetched {len(muse_raw_data)} job listings from The Muse API.")

    final_raw_muse: list = []
    
    for data in muse_raw_data:
        match_keys: dict = {
            "title": data['name'],
            "slug": data['short_name'].replace("-", " "),
            "tags": data.get("categories", [])[0].get("name", "") if data["categories"] else '',
            "description": data['contents'],
        }
        
        if matching.filter_matches(data, match_keys):
            final_raw_muse.append(data)

    utils.save_file(raw_muse_path, final_raw_muse)
    print(f"File with {len(final_raw_muse)} entries saved to {raw_muse_path}")

def fetch_from_muse(page: int, country: str) -> list[dict]:
    url: str = "https://www.themuse.com/api/public/jobs"

    params: dict = {
        "page": page,
        "location": country
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    data: dict = response.json()

    return data['results']

if __name__ == "__main__":
    main()