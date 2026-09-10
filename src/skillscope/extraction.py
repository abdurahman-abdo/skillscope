import re

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
        "bs",
        "ba",
        "bs/ba",
        "ba/bs"
    ]
    
    doctorate_keywords: list[str] = [
        "phd",
        "ph.d",
        "ph.d.",
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

"""The constants below are part of the wider years_of_experience extractor function after them
    Each of the constants hold holds unique pattern and functionality to predict in what shape/s a 
    years of experience would be found in a plain description of a job posting.
"""
SPACE = r"\s{0,2}?"
HTML_TAGS = r"(?:\[NEWLINE\]|\[BULLET\]|\[P\]|\[LIST\]|\[H\])"
LINKING_WORDS = r"(?i:in|with|building|leading|working\s+(?i:in|with|on)|shipping|of|as|across|within|demonstrated\s+experience|proven\s+(?:track\s+record|experience)\s+on|leveraging|integrating|developing|implementing)"
LOOKING_FOR_PATTERN = r"We\sare\slooking(?:\sfor|\sfor\ssomeone|\sfor\ssomeone\swho\shas)?:?"

WITH_PATTERN = rf"(?:with\s+at\s+least|at\s+least|with{SPACE}(?:~|(?:about|approximately|a\sminimum\sof))|a\sminimum\sof){SPACE}"
SAME_SENTENCE_WILDCARD = rf"(?:(?!{HTML_TAGS})[^.\n;]){{0,50}}?"
RANGE_SEPARATOR = rf"{SPACE}(?:-|to){SPACE}"

TEXTUAL = r"(?:one|two|three|four|five|six|seven|eight|nine|ten)"
NUMERIC = r"(?:1[0-5]|[1-9])"
YEARS = r"\b(?:years|year\(s\)|year)(?!\w)"

POSSIBLE_NUMBERS = rf"(?:{NUMERIC}|{TEXTUAL})"
CAPTURED_NUMBER = rf"(?P<years>{POSSIBLE_NUMBERS}(?:{RANGE_SEPARATOR}{POSSIBLE_NUMBERS})?{SPACE}\+?)"
UNNAMED_CAPTURED_NUMBER = rf"(?:{POSSIBLE_NUMBERS}(?:{RANGE_SEPARATOR}{POSSIBLE_NUMBERS})?{SPACE}\+?)"

MAIN_PATTERN = rf"{CAPTURED_NUMBER}{SPACE}{YEARS}"
UNNAMED_MAIN_PATTERN = rf"{UNNAMED_CAPTURED_NUMBER}{SPACE}{YEARS}"
LINKED_INFORMATION_PATTERN = rf"(?:(?!{WITH_PATTERN}{UNNAMED_CAPTURED_NUMBER}|{UNNAMED_MAIN_PATTERN}|{HTML_TAGS})[^.\n;])+"

FIELD_INFO_AFTER = rf"(?P<field>{LINKING_WORDS}\s+{LINKED_INFORMATION_PATTERN})"
FIELD_INFO_MIDDLE = rf"(?P<field>(?:(?!{UNNAMED_MAIN_PATTERN}|{HTML_TAGS})[^.\n;]){{0,50}}?)"

INFO_AFTER_BRACKETS = rf"(?P<field>{LINKED_INFORMATION_PATTERN})"
EXPERIENCE_CAPTURED_AFTER = rf"(?P<field>{SAME_SENTENCE_WILDCARD}experience\s+{LINKING_WORDS}\s+{LINKED_INFORMATION_PATTERN})"

CASE_1 = rf"(?i:(?:{WITH_PATTERN}|with\s+){MAIN_PATTERN}{INFO_AFTER_BRACKETS})"

CASE_2 = rf"\({MAIN_PATTERN}:?\)[:\s]*{INFO_AFTER_BRACKETS}"
CASE_3 = rf"(?:Experience)(?:\[H\])?:?{SAME_SENTENCE_WILDCARD}{MAIN_PATTERN}\s+{FIELD_INFO_AFTER}"

CASE_4 = rf"(?i:{MAIN_PATTERN}{EXPERIENCE_CAPTURED_AFTER})"
CASE_5 = rf"(?i:{MAIN_PATTERN}{FIELD_INFO_MIDDLE}experience)"

CASE_6 = rf"(?:Qualifications?)(?:\[H\])?:?{SAME_SENTENCE_WILDCARD}{MAIN_PATTERN}\s+{FIELD_INFO_AFTER}"
CASE_7 = rf"(?:Qualifications?)(?:\[H\])?:?{FIELD_INFO_MIDDLE}{MAIN_PATTERN}"

CASE_8 = rf"{TEXTUAL}{SPACE}\((?P<years>{NUMERIC}{SPACE}\+?)\){SPACE}{YEARS}{SAME_SENTENCE_WILDCARD}experience\s+{FIELD_INFO_AFTER}"
CASE_9 = rf"{TEXTUAL}{SPACE}\((?P<years>{NUMERIC}{SPACE}\+?)\){SPACE}{YEARS}{FIELD_INFO_MIDDLE}experience"

CASE_10 = rf"{LOOKING_FOR_PATTERN}{SAME_SENTENCE_WILDCARD}{MAIN_PATTERN}\s+{FIELD_INFO_AFTER}"
CASE_11 = rf"{LOOKING_FOR_PATTERN}{FIELD_INFO_MIDDLE}{MAIN_PATTERN}"

PATTERNS = [CASE_1, CASE_2, CASE_3, CASE_4, CASE_5, CASE_6, CASE_7, CASE_8, CASE_9, CASE_10, CASE_11]

def extract_years_of_experience(description: str) -> list[dict[str, str]]:
    """This function takes a clean description of job posting as an input 
    and returns a list of dictionaries, each with years and field of what it captured.  
    
    **Note:** This function takes pattern and regex pattern from the constants declared outside of this function!
    
    **Args:**  
        `description (str):` a description of job data that was filtered through the clean_html of utils.py.  
            **Warning:** _Calling it on raw HTML will fail to work as expected!_  

    **Returns:**
        `list[dict[str, str]]:` returns a list of dictionary/ies (or empty list if none found) each with a years key and field key
        signaling how many years of experience is required for which field.
    
    **known limitations:**
        This function doesn't take into account if tabular data is in the passed description since clean_html doesn't handle it currently.
    """
    captured_json = []

    remaining = description
    for pattern in PATTERNS:
        while match := re.search(pattern, remaining):
            captured_json.append(match.groupdict())
            remaining = remaining[:match.start()] + remaining[match.end():]

    return captured_json

def extract_required_tools(description: str) -> list[str]:
    # working on this in my jupyter notebook
    pass

if __name__ == "__main__":
    main()