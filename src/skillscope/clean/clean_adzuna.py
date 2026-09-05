import pandas as pd
from pathlib import Path
from skillscope import (config, matching, utils)


def main():
    adzuna_data = utils.load_file(config.raw_adzuna_path)

    adzuna_cleaned_data = list()

    for job in adzuna_data:
        # print(json.dumps(job["location"]["area"], indent=4))
        adzuna_cleaned_data.append(
            {
            "job_name": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", ""),
            "country": job.get("location", {}).get("area", [])[0] if job.get("location", {}).get("area") else "",
            "location": job.get("location", {}).get("display_name", ""),
            "min_salary": job.get("salary_min", 0),
            "max_salary": job.get("salary_max", 0),
            "description": job.get("description", "").replace("\n", " ").strip(),
            "posted_date": job.get("created", ""),
            "work_type": matching.determine_work_type(job),
            "tags": "; ".join([job.get("category", {}).get("tag", "")]),
            "source": "adzuna"
            }
        )

    adzuna_df = pd.DataFrame(adzuna_cleaned_data)
    adzuna_df = adzuna_df.drop_duplicates().reset_index(drop=True)

    cleaned_adzuna_path = config.CLEANED_DATA_PATH / "adzuna.csv"

    adzuna_df.to_csv(cleaned_adzuna_path)
    print(f"File with {len(adzuna_df)} entries saved to {cleaned_adzuna_path}")