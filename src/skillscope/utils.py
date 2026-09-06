import json
import re
import html

def main() -> None:
    print("""This is the utilities module.
            It contains functions to load and save JSON files, 
            clean and hash matched job roles,
            and make objects hashable for use in sets or as dictionary keys.""")

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
        tags = r"<[^>]+>"
        consecutive_tags = r"</[^>/]+><[^>/]+>"
        final_desc = re.sub(consecutive_tags, " ", unescaped)
        return re.sub(tags, "", final_desc).strip()

if __name__ == "__main__":
    main()