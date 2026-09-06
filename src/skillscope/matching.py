def main() -> None:
    print("""This is the matching module. 
            It contains functions to filter and score job listings based on target roles and work types, 
            to determine the work type of a job listing based on its description and other attributes, 
            and defines the constant variable for target roles.
        """)

TARGET_ROLES: list[str] = [
    "data scientist",
    "machine learning",
    "ml engineer",
    "data analyst",
    "ai engineer",
    "data engineer"
]

def determine_work_type(text: str) -> str:
    hybrid_keywords: list = [
        "hybrid",
        "part remote",
        "partially remote"
    ]

    remote_keywords: list = [
        "remote",
        "work from home",
        "work-from-home",
        "wfh",
        "work from anywhere",
        "fully distributed",
        "distributed team",
        "telecommute",
        "home-based"
    ]

    onsite_keywords: list = [
        "on-site",
        "onsite",
        "on site",
        "office-based",
        "office based"
    ]

    if any(keyword in text for keyword in hybrid_keywords):
        return "hybrid"

    if any(keyword in text for keyword in remote_keywords):
        return "remote"

    if any(keyword in text for keyword in onsite_keywords):
        return "onsite"

    return "unknown"

def filter_matches(data: dict, match_keywords: dict) -> bool:
    """This function takes a dictionary data and match_keywords as input 
    to return a boolean if the data's key matched with target roles and modify the dict as a side effect.

    **Args:**
        `data (dict):` a dictionary data with key value pairs. _(A one that have keys specified on math_keywords is recommended!)_  

        `match_keywords (dict):` a dict with information on what to check for as a match, it's structure should be:
        ```python
            match_keywords = {
                "title": data.get("title", ""),
                "slug": data.get("slug", "").replace("-", " "),
                "tags": " ".join(data.get("tags", [])),
                "description": data.get("description", "")
            }
        ```

    **Returns:**
        `bool:` returns whether the data have matching values in the selected keys
    
    **Side effects:**
        Adds two keys: score and matched.
        `data['score']:` shows how much related the data is to the target roles.
        `data['matched']:` a list of dictionaries with which match key matched which target role, respectively.
    """
    
    title: str = match_keywords['title'].lower()
    slug: str = match_keywords['slug'].lower()
    tags: str = match_keywords['tags'].lower()
    description: str = match_keywords['description'].lower()

    data['score'] = 0
    data['matched'] = []
    matched: list = data['matched']

    for role in TARGET_ROLES:
        if role in title:
            data['score'] += 5
            matched.append({'job_title': role})
        if role in slug:
            data['score'] += 3
            matched.append({'slug': role})
        if role in tags:
            data['score'] += 2
            matched.append({'tags': role})
        if role in description:
            data['score'] += 1
            matched.append({'description': role})

    return data['score'] > 0

if __name__ == "__main__":
    main()