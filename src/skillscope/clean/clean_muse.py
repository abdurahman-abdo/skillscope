import pandas as pd
from skillscope import (config, utils, matching)

def main() -> None:
    muse_data = utils.load_file(config.raw_muse_path)

    # print("".join([json.dumps(muse['locations'], indent=4) for muse in muse_data]))

    muse_cleaned_data = list()

    for job in muse_data:
        work_type, country, location = get_exact_location(job.get("locations", {}))
        
        muse_cleaned_data.append(
            {
            "job_name": job.get("name", ""),
            "company": job.get("company", {}).get("name", ""),
            "country": country,
            "location": location,
            "min_salary": job.get("min_salary", 0),
            "max_salary": job.get("max_salary", 0),
            "description": job.get("contents", "").replace("\n", " ").strip(),
            "posted_date": job.get("publication_date", ""),
            "work_type": work_type,
            "score": job.get("score", 0),
            "matched": utils.make_hashable(utils.clean_matched(*job.get("matched", [{}]))),
            "source": "muse"
            }
        )

    # print(len(muse_cleaned_data))
    # print(json.dumps(muse_cleaned_data, indent=4))
    muse_df = pd.DataFrame(muse_cleaned_data)
    muse_df = muse_df.drop_duplicates().reset_index(drop=True)

    cleaned_muse_path = config.CLEANED_DATA_PATH / "muse.csv"

    muse_df.to_csv(cleaned_muse_path)
    print(f"Successfully saved the cleaned version with {len(muse_df)} entries to {cleaned_muse_path}")


def get_exact_location(data: list[dict]) -> tuple:
    """Returns `work_type`, `country`, and `location` **respectively** given an input like:  
        ```
        data: list[dict] = [  
            {  
                "name": "Flexible / Remote"  
            },  
            {  
                "name": "New York, NY"  
            }  
        ],
        ```
    """
    
    if not data:
        return "unknown", "N/A", "N/A"
    
    work_type, country, location = "unknown", "N/A", "N/A"
    
    temp = data.copy()
    for component in temp:
        if '/' in component['name']:
            data.remove(component)
            work_type = matching.determine_work_type(component)
        elif ',' in component['name']:
            location, country = component['name'].split(",")
            
            if country.strip() in ["CA", "NY", "DC"]:
                country = "United States"
        

    return work_type, country.strip(), location.strip()

if __name__ == "__main__":
    main()