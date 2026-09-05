import requests, json, time
from skillscope import (config, utils, matching)

raw_arbeit_path = config.RAW_DATA_PATH / "arbeit.json"

def main() -> None:

    print("Retrieving data...")

    raw_arbeit_data: list = []
    
    for page in range(0, 20, 2):
        print(f"Round: {int((page / 2) + 1)}/10 completed successfully.")
        
        raw: list[dict] = fetch_from_arbeit(page)
        raw_arbeit_data.extend(raw)
        
        # to avoid hitting the arbeit rate limit, we can add a delay between requests
        time.sleep(60)  # sleep for 1 minute

    print("Data retrieved successfully.")
    print("Storing data with additional keys...")

    final_raw_arbeit: list = []

    for data in raw_arbeit_data:
        match_keys: dict = {
            "title": data.get("title", ""),
            "slug": data.get("slug", "").replace("-", " "),
            "tags": " ".join(data.get("tags", [])),
            "description": data.get("description", "")
        }
        
        if matching.filter_matches(data, match_keys):
            final_raw_arbeit.append(data)

    utils.save_file(raw_arbeit_path, final_raw_arbeit)
    print(f"File with {len(final_raw_arbeit)} entries saved to {raw_arbeit_path}")

def fetch_from_arbeit(page: int) -> list[dict]:
    url: str = f"https://arbeitnow.com/api/job-board-api?page={page}"

    response = requests.get(url)

    response.raise_for_status()

    data: dict = response.json()

    return data["data"]

if __name__ == "__main__":
    main()
