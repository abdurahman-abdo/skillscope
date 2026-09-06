def main():
    print("""This is the extraction module. 
            It contains functions to extract more information from provided job description like: 
            educational background, years of experience, and required tools.
          """)

def extract_required_edu_background(desc: str) -> tuple[str, ...]:
    bachelors_keywords: list[str] = [
        "bachelor",
        "bachelor's",
        "bsc",
        "b.s.",
        "bs"
    ]
    
    doctorate_keywords: list[str] = [
        "phd",
        "ph.d",
        "doctorate"
    ]
    
    masters_keywords: list[str] = [
        "master's",
        "msc",
        "m.s.",
        "master degree",
        "masters in "
    ]
    
    desc_lower: str = desc.lower()
    return_values: list = []
    
    if any(key in desc_lower for key in doctorate_keywords):
        return_values.append("PhD")
    if any(key in desc_lower for key in masters_keywords):
        return_values.append("Master's")
    if any(key in desc_lower for key in bachelors_keywords):
        return_values.append("Bachelor's")
    
    return tuple(return_values)

def extract_years_of_experience(description: str) -> int:
    # working on this in Jupyter notebook
    pass

def extract_required_tools(description: str) -> list[str]:
    # working on this in my jupyter notebook
    pass

if __name__ == "__main__":
    main()