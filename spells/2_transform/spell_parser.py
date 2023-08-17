from bs4 import BeautifulSoup
import re, os
import sqlite3
from pathlib import Path
import pandas as pd
import json, csv


def replacer(the_string, to_replace, the_replacers):
    the_diff = len(to_replace) - len(the_replacers)
    if the_diff > 0:
        new_list = the_replacers[-1] * the_diff
        the_replacers = [*the_replacers, *new_list]
    for i, v in enumerate(to_replace):
        the_string = the_string.replace(v, the_replacers[i])
    return the_string


directory="../1_extract/dnd5e.wikidot.com"
 
# iterate over files in
# that directory
the_files=[]
for root, dirs, files in os.walk(directory):
    for filename in files:
        filename=str(filename)
        if "spell:" in filename:
            the_files.append(filename)

out_all = []
for the_file in the_files:
    the_file = f"{directory}/{the_file}"
    with open(the_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    data = soup.find("div", {"id": "page-content"}).findChildren("p")
    #print(data)

    try:
        # data massage
        name=the_file.split(":")[1]
        source=data[0].text.replace("Source: ", "").strip()
        level=data[1].text.split()[0].strip()
        level=re.search('\d+', level)
        if not level:
            level="0"
        else:
            level=level.group().strip()
        school=data[1].text.split()[1].strip()
        is_ritual = False
        if "ritual" in data[1].text:
            is_ritual = True
        subdata=data[2].text.splitlines()
        casttime=re.search('\d+',subdata[0]).group().strip()
        action_type_list = subdata[0].split()[3:]
        actiontype = " ".join(action_type_list).strip()
        the_range=subdata[1].replace("Range: ", "").strip()
        components=subdata[2].replace("Components: ", "").strip()
        duration=subdata[3].replace("Duration: ", "").strip()
        spelllists=data[-1].text.replace("Spell Lists. ", "")
        description="" 
        for i in data[3:-1]:
            description = description + i.text          
       # print(description)
    except Exception as e:
        # print(name)
        raise(e)

    the_id = "SPELL" + "_" + name + "_" + level + "_" + school
    the_id = replacer(the_id, [" ", "-"], ["_"])
    the_id = the_id.upper()

    # out structure
    out = {
        "id" : the_id,
        "name": name,
        "source": source,
        "level":level,
        "school": school,
        "ritual": is_ritual,
        "casttime": casttime,
        "actiontype": actiontype,
        "the_range": the_range,
        "components": components,
        "duration": duration,
        "spelllists": spelllists,
        "description": description
    }
    out_all.append(out)


if Path("spell_data.csv").is_file():
    os.remove("spell_data.csv")


with open("spell_data.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    # out_keys = list(out_all[0].keys())
    # csv_writer.writerow(out_keys)


    for row in out_all:
        csv_writer.writerow([
            row["id"],
            row["name"],
            row["source"],
            row["level"],
            row["school"],
            row["ritual"],
            row["casttime"],
            row["actiontype"],
            row["the_range"], 
            row["components"],
            row["duration"],
            row["spelllists"],
            row["description"]
        ])


    #print(out)

# out_all_str = json.dumps(out_all)
# if Path("spell_data.json").is_file():
#     os.remove("spell_data.json")
# json_file = open("spell_data.json", "w")
# json_file.write(out_all_str)
# json_file.close()


# pd.read_json(out_all_str).to_csv('spell_data.csv', encoding='utf-8', index=False)

