import re
import pandas as pd
from skillscope import (config, utils, matching, extraction)
from skillscope.fetch import fetch_arbeit

cleaned_arbeit_path = config.CLEANED_DATA_PATH / "arbeit.csv"

def main():
    arbeit_data = utils.load_file(fetch_arbeit.raw_arbeit_path)

    arbeit_cleaned_data = list()

    for job in arbeit_data:
        desc_cleaned = utils.clean_html(job.get("description", "")).replace("\n", "[NEWLINE]")
        
        text: str = " ".join([
            job.get("slug", "").replace("-", " "),
            job.get("title", ""),
            desc_cleaned,
            job.get("location", ""),
            " ".join(job.get("tags", []))
        ]).lower()
        
        determined_work_type = matching.determine_work_type(text)
        
        arbeit_cleaned_data.append(
            {
            "job_name": job.get("title", ""),
            "company": job.get("company_name", ""),
            "country": extract_country(job.get("location", "")),
            "location": job.get("location", ""),
            "min_salary": job.get("salary_min", 0),
            "max_salary": job.get("salary_max", 0),
            "description": desc_cleaned,
            "posted_date": job.get("created_at", ""),
            "work_type": "remote" if determined_work_type == "unknown" and job.get('remote') else determined_work_type,
            "tags": "; ".join(job.get("tags", [])),
            "educational_requirement": extraction.extract_required_edu_background(desc_cleaned),
            "years_of_experience": "to-do",
            "required_tools": "to-do",
            "score": job.get("score", 0),
            "matched": utils.make_hashable(utils.group_values_by_key(*job.get("matched", [{}]))),
            "source": "arbeit"
            }
        )

    arbeit_df = pd.DataFrame(arbeit_cleaned_data)
    arbeit_df = arbeit_df.drop_duplicates().reset_index(drop=True)

    arbeit_df.to_csv(cleaned_arbeit_path)
    print(f"File with {len(arbeit_df)} entries saved to {cleaned_arbeit_path}")

def extract_country(location_str: str) -> str | None:
    LOCATION_MAPPING = {
        # Germany
        "germany": "Germany", "ger": "Germany", "gb": "United Kingdom", "de": "Germany",
        "stuttgart": "Germany", "munich": "Germany", "münchen": "Germany", 
        "cologne": "Germany", "köln": "Germany", "berlin": "Germany", 
        "leipzig": "Germany", "hürth": "Germany", "bielefeld": "Germany", 
        "chemnitz": "Germany", "dresden": "Germany", "bonn": "Germany", 
        "frankfurt": "Germany", "darmstadt": "Germany", "düsseldorf": "Germany",
        "hamburg": "Germany", "sachsen": "Germany", "brandenburg": "Germany",
        "liveeo": "Germany",
        
        # United Kingdom
        "uk": "United Kingdom", "united kingdom": "United Kingdom", "england": "United Kingdom",
        "london": "United Kingdom", "manchester": "United Kingdom", 
        "bicester": "United Kingdom", "cardiff": "United Kingdom", "cambridge": "United Kingdom",
        
        # United States
        "united states": "United States", "california": "United States", "mountain view": "United States"
    }
    
    if not isinstance(location_str, str) or not location_str.strip():
        return None  # Handles empty/blank entries (like index 2, 10, 54, 65, 66)
    
    text = location_str.lower()
    
    # 1. Multi-country string check (e.g., index 8)
    if "or" in text or "," in text:
        matched_countries = []
        for term, country in LOCATION_MAPPING.items():
            if re.search(r'\b' + re.escape(term) + r'\b', text):
                if country not in matched_countries:
                    matched_countries.append(country)
        
        # Check specific listed countries in index 8
        for country in ["Nigeria", "Ethiopia", "India", "Rwanda"]:
            if country.lower() in text and country not in matched_countries:
                matched_countries.append(country)
                
        if len(matched_countries) > 1:
            return ", ".join(matched_countries)
        elif len(matched_countries) == 1:
            return matched_countries[0]

    # 2. Single direct match check
    for term, country in LOCATION_MAPPING.items():
        if re.search(r'\b' + re.escape(term) + r'\b', text):
            return country

    # 3. Handle pure Remote/All Offices without location context
    if "remote" in text or "all offices" in text:
        return "Remote"

    return "Unknown"

if __name__ == "__main__":
    main()