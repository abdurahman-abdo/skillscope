import pandas as pd
from skillscope import (config, utils, matching, extraction)
from skillscope.fetch import fetch_muse

cleaned_muse_path = config.CLEANED_DATA_PATH / "muse.csv"

def main() -> None:
    muse_data = utils.load_file(fetch_muse.raw_muse_path)

    muse_cleaned_data = list()

    for job in muse_data:
        work_type, country, location = get_exact_location(job.get("locations", {}))
        
        desc_cleaned = utils.clean_html(job.get("contents", "")).replace("\n", "[NEWLINE]")
        
        muse_cleaned_data.append(
            {
            "job_name": job.get("name", ""),
            "company": job.get("company", {}).get("name", ""),
            "country": country,
            "location": location,
            "min_salary": job.get("min_salary", 0),
            "max_salary": job.get("max_salary", 0),
            "description": desc_cleaned,
            "posted_date": job.get("publication_date", ""),
            "work_type": work_type,
            "tags": job.get("tags", [{}])[0].get("short_name", "") if job.get("tags", [{}]) != [] else '',
            "educational_requirement": extraction.extract_required_edu_background(desc_cleaned),
            "years_of_experience": utils.make_hashable(extraction.extract_years_of_experience(desc_cleaned)),
            "required_tools": "to-do",
            "score": job.get("score", 0),
            "matched": utils.make_hashable(utils.group_values_by_key(*job.get("matched", [{}]))),
            "source": "muse"
            }
        )

    muse_df = pd.DataFrame(muse_cleaned_data)
    muse_df = muse_df.drop_duplicates().reset_index(drop=True)

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
            work_type = matching.determine_work_type(component['name'].replace("/", " "))
        elif ',' in component['name']:
            location, country = component['name'].split(",")
            
            if country.strip() in ["CA", "NY", "DC"]:
                country = "United States"
        

    return work_type, country.strip(), location.strip()

if __name__ == "__main__":
    main()