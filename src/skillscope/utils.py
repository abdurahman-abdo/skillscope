import json
import re
import html

def main() -> None:
    print("""This is the utilities module.
            It contains functions to load and save JSON files, 
            clean and hash matched job roles,
            and make objects hashable for use in sets or as dictionary keys.""")
    
    print(clean_html("Skills<ul>text with no li tags</ul>Next"))

def load_file(file_path: str) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_file(file_path: str, data: list[dict], mode: str = 'w') -> None:
    with open(file_path, mode, encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def group_values_by_key(*datas: dict) -> dict:
    dict_keys: list = []
    return_dict: dict = {}
    for data in datas:
        for key in data.keys():
            if key not in dict_keys:
                dict_keys.append(key)
                return_dict[key] = [data[key]]
            else:
                return_dict[key].append(data[key])

    return return_dict

def make_hashable(obj: bool | int | float | str | list | set | tuple | dict) -> tuple:
    if isinstance(obj, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
    if isinstance(obj, (list, set, tuple)):
        return tuple(make_hashable(item) for item in obj)
    return obj

def clean_html(description: str) -> str:
        new_desc = description.replace("&nbsp;", " ")
        unescaped = html.unescape(new_desc)
        
        bullet_tags = r"\s*(?i:</?li[^>]*>)\s*"
        newline_tags = r"\s*(?i:</?div[^>]*>|<br[^>]*>|<hr[^>]*>)\s*"
        list_tags = r"\s*(?i:</?ul[^>]*>|</?ol[^>]*>)\s*"
        consecutive_bullets = r"\[BULLET\]\s{0,2}\[BULLET\]"
        heading_tag = r"\s*</?h[1-6][^>]*>\s*"
        paragraph_tag = r"\s*</?p[^>]*>\s*"
        
        unescaped = re.sub(bullet_tags, "[BULLET]", unescaped)
        unescaped = re.sub(newline_tags, "[NEWLINE]", unescaped)
        unescaped = re.sub(list_tags, "[LIST]", unescaped)
        unescaped = re.sub(consecutive_bullets, "[BULLET]", unescaped)
        unescaped = re.sub(heading_tag, "[H]", unescaped)
        unescaped = re.sub(paragraph_tag, "[P]", unescaped)
        
        tags = r"<[^>]+>"
        consecutive_tags = r"(?i:</[^>/]+><[^>/]+>)"
        
        final_desc = re.sub(consecutive_tags, " ", unescaped)
        return re.sub(tags, "", final_desc).strip()

if __name__ == "__main__":
    main()