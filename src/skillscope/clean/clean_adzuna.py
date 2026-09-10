import pandas as pd
from pathlib import Path
from skillscope import (config, matching, utils, extraction)
from skillscope.fetch import fetch_adzuna

cleaned_adzuna_path = config.CLEANED_DATA_PATH / "adzuna.csv"

def main():
    adzuna_data = utils.load_file(fetch_adzuna.raw_adzuna_path)

    adzuna_cleaned_data = list()

    for job in adzuna_data:
        desc_cleaned = utils.clean_html(job.get("description", "")).replace("\n", "[NEWLINE]")        
        
        text: str = " ".join([
            job.get("title", ""),
            desc_cleaned,
            job.get("location", {}).get("display_name", ""),
            " ".join(job.get("location", {}).get("area", []))
        ]).lower()
        
        adzuna_cleaned_data.append(
            {
            "job_name": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", ""),
            "country": job.get("location", {}).get("area", [])[0] if job.get("location", {}).get("area") else "",
            "location": job.get("location", {}).get("display_name", ""),
            "min_salary": job.get("salary_min", 0),
            "max_salary": job.get("salary_max", 0),
            "description": desc_cleaned,
            "posted_date": job.get("created", ""),
            "work_type": matching.determine_work_type(text),
            "tags": "; ".join([job.get("category", {}).get("tag", "")]),
            "edu_background": extraction.extract_required_edu_background(desc_cleaned),
            "years_of_experience": utils.make_hashable(extraction.extract_years_of_experience(desc_cleaned)),
            "required_tools": "to-do",
            "score": job.get("score", 0),
            "matched": utils.make_hashable(utils.group_values_by_key(*job.get("matched", [{}]))),
            "source": "adzuna"
            }
        )

    adzuna_df = pd.DataFrame(adzuna_cleaned_data)
    adzuna_df = adzuna_df.drop_duplicates().reset_index(drop=True)

    adzuna_df.to_csv(cleaned_adzuna_path)
    print(f"File with {len(adzuna_df)} entries saved to {cleaned_adzuna_path}")

if __name__ == "__main__":
    main()