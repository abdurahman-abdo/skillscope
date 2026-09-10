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

"""The constants below build up a set of regex patterns(CASE_1 .. CASE_11) 
that each target a variety of possible ways job postings phrasea 
"years of experience in X" requirement. 

`extract_years_of_experience` runs them against a description and returns whatever it finds.

All tests and development history could be found in main.ipynb —
run any modified cells there before/after changing anything below.
"""

# ---------------------------------------------------------
# Core, reused constants used for essential scanning 
# ---------------------------------------------------------

SPACE = r"\s{0,2}?"
HTML_TAGS = r"(?:\[NEWLINE\]|\[BULLET\]|\[P\]|\[LIST\]|\[H\])" # Tokens inserted by clean_html() (see utils.py) in place of structural HTML tags.
LINKING_WORDS = r"(?i:in|with|building|leading|working\s+(?i:in|with|on)|shipping|of|as|across|within|demonstrated\s+experience|proven\s+(?:track\s+record|experience)\s+on|leveraging|integrating|developing|implementing)"

# Matches the common "We are looking for (someone who has) ..."
LOOKING_FOR_PATTERN = r"We\sare\slooking(?:\sfor|\sfor\ssomeone|\sfor\ssomeone\swho\shas)?:?"

# ---------------------------------------------------------
# Critical patterns that are always used to detect years
# ---------------------------------------------------------

TEXTUAL = r"(?:one|two|three|four|five|six|seven|eight|nine|ten)"
NUMERIC = r"(?:1[0-5]|[1-9])"

# Matches: "years", "year(s)", or "year"
# used (?!\w) because \b is useless since it could end with ')'
YEARS = r"\b(?:years|year\(s\)|year)(?!\w)"

# ---------------------------------------------------------
# Building blocks that combine the core constants above 
# ---------------------------------------------------------

# Matches lead-ins like "with at least", "a minimum of", "with ~10.." that precede a years mention
WITH_PATTERN = rf"(?:with\s+at\s+least|at\s+least|with{SPACE}(?:~|(?:about|approximately|a\sminimum\sof))|a\sminimum\sof){SPACE}"
SAME_SENTENCE_WILDCARD = rf"(?:(?!{HTML_TAGS})[^.\n;]){{0,50}}?"
RANGE_SEPARATOR = rf"{SPACE}(?:-|to){SPACE}"

# Numeric chain-patterns
POSSIBLE_NUMBERS = rf"(?:{NUMERIC}|{TEXTUAL})"
CAPTURED_NUMBER = rf"(?P<years>{POSSIBLE_NUMBERS}(?:{RANGE_SEPARATOR}{POSSIBLE_NUMBERS})?{SPACE}\+?)"
UNNAMED_CAPTURED_NUMBER = rf"(?:{POSSIBLE_NUMBERS}(?:{RANGE_SEPARATOR}{POSSIBLE_NUMBERS})?{SPACE}\+?)"

# Structured patterns derived from the numeric ones
MAIN_PATTERN = rf"{CAPTURED_NUMBER}{SPACE}{YEARS}"
UNNAMED_MAIN_PATTERN = rf"{UNNAMED_CAPTURED_NUMBER}{SPACE}{YEARS}"
LINKED_INFORMATION_PATTERN = rf"(?:(?!{WITH_PATTERN}{UNNAMED_CAPTURED_NUMBER}|{UNNAMED_MAIN_PATTERN}|{HTML_TAGS})[^.\n;])+"

# ---------------------------------------------------------
# Critical patterns to detect field information 
# ---------------------------------------------------------

# Field capture for "... years [linking word] FIELD", e.g. "5 years in Python".
FIELD_INFO_AFTER = rf"(?P<field>{LINKING_WORDS}\s+{LINKED_INFORMATION_PATTERN})"

# Field capture for "Header: FIELD ... years" (field precedes the number), or
# "years FIELD experience" (field is in between years and the word 'experience')
FIELD_INFO_MIDDLE = rf"(?P<field>(?:(?!{UNNAMED_MAIN_PATTERN}|{HTML_TAGS})[^.\n;]){{0,50}}?)"

FIELD_AFTER_BRACKETS = rf"(?P<field>{LINKED_INFORMATION_PATTERN})"

# Field capture for "... years ... experience [linking word] FIELD", where
# the word "experience" itself sits between the years mention and the field.
EXPERIENCE_CAPTURED_AFTER = rf"(?P<field>{SAME_SENTENCE_WILDCARD}experience\s+{LINKING_WORDS}\s+{LINKED_INFORMATION_PATTERN})"

# ---------------------------------------------------------
# All case scenarios 
# ---------------------------------------------------------

# "with [at least] 5 years [of] experience in Python"
CASE_1 = re.compile(
    rf"(?:{WITH_PATTERN}|with\s+){MAIN_PATTERN}{FIELD_AFTER_BRACKETS}",
    flags=re.IGNORECASE,
)
# "(5+ years) FIELD" (no word "experience")
CASE_2 = re.compile(rf"\({MAIN_PATTERN}:?\)[:\s]*{FIELD_AFTER_BRACKETS}")

# "Experience:" / "Experience[H]" section label, years mentioned nearby
CASE_3 = re.compile(rf"(?:Experience)(?:\[H\])?:?{SAME_SENTENCE_WILDCARD}{MAIN_PATTERN}\s+{FIELD_INFO_AFTER}")

# "5 years ... experience linking_word [FIELD]"
CASE_4 = re.compile(
    rf"(?:{MAIN_PATTERN}{EXPERIENCE_CAPTURED_AFTER})",
    re.IGNORECASE
)

# "5 years [FIELD] experience" (no linking word)
CASE_5 = re.compile(
    rf"(?:{MAIN_PATTERN}{FIELD_INFO_MIDDLE}experience)",
    re.IGNORECASE
)

# "Qualifications:" / "Qualifications[H]" section label, field after years
CASE_6 = re.compile(rf"(?:Qualifications?)(?:\[H\])?:?{SAME_SENTENCE_WILDCARD}{MAIN_PATTERN}\s+{FIELD_INFO_AFTER}")

# same as CASE_6 but field precedes the years mention
CASE_7 = re.compile(rf"(?:Qualifications?)(?:\[H\])?:?{FIELD_INFO_MIDDLE}{MAIN_PATTERN}")

# "five (5+) years of experience in Python" -> textual number spelled out
# with the numeric form in parentheses, field after "experience"
CASE_8 = re.compile(rf"{TEXTUAL}{SPACE}\((?P<years>{NUMERIC}{SPACE}\+?)\){SPACE}{YEARS}{SAME_SENTENCE_WILDCARD}experience\s+{FIELD_INFO_AFTER}")

# same as CASE_8 but field precedes "experience"
CASE_9 = re.compile(rf"{TEXTUAL}{SPACE}\((?P<years>{NUMERIC}{SPACE}\+?)\){SPACE}{YEARS}{FIELD_INFO_MIDDLE}experience")

# "We are looking for someone with 5 years of experience in Python"
CASE_10 = re.compile(rf"{LOOKING_FOR_PATTERN}{SAME_SENTENCE_WILDCARD}{MAIN_PATTERN}\s+{FIELD_INFO_AFTER}")

# same as CASE_10 but field precedes the years mention
CASE_11 = re.compile(rf"{LOOKING_FOR_PATTERN}{FIELD_INFO_MIDDLE}{MAIN_PATTERN}")

# ---------------------------------------------------------
# Final pattern composition, More specific shapes first 
# ---------------------------------------------------------

# since order matters because the function consumes the already matched ones.
PATTERNS = [CASE_1, CASE_2, CASE_3, CASE_4, CASE_5, CASE_6, CASE_7, CASE_8, CASE_9, CASE_10, CASE_11]


def extract_years_of_experience(description: str) -> tuple[dict[str, str], ...]:
    """Extract `years of experience` + `field` mentions from a cleaned job description.

    Runs all patterns in PATTERNS against `description`, collecting every
    non-overlapping match. Matched spans are removed from the working copy
    of the text as they're found, so the same stretch of text can't be
    captured twice by two different patterns.

    **Note:** this function reads its regex patterns from the module-level
    constants above (PATTERNS) rather than building them itself.
    
    **Args:**
        `description:` A job description that has already been passed through
            `clean_html()` ***(see utils.py)***.
            **Warning:** *Calling this on raw HTML will not raise an error but won't work as expected.*

    **Returns:**
        - A tuple of dicts, each dict shaped like `{"years": "5+", "field": "Python"}`.
        - Returns an empty tuple if no years-of-experience mention is found.
        - A single description can produce multiple dicts if it mentions
        experience requirements for more than one thing. "years" is
        returned as str and is NOT converted to int.

    **Known limitations (deliberate):**
        - This function doesn't take into account if tabular data is in the passed description 
        since `clean_html` doesn't handle it currently.
    """
    if "year" not in description.lower():
        return ()
    if re.search(rf"(?:{NUMERIC}|{TEXTUAL})", description) is None:
        return ()
    
    captured_json = []

    remaining = description
    for pattern in PATTERNS:
        while match := pattern.search(remaining):
            captured_json.append(match.groupdict())
            remaining = remaining[:match.start()] + remaining[match.end():]

    return tuple(captured_json)

def extract_required_tools(description: str) -> list[str]:
    # working on this in my jupyter notebook
    pass

if __name__ == "__main__":
    main()