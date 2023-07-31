from bs4 import BeautifulSoup
import re, os
import sqlite3
from pathlib import Path
import pandas as pd
import json, csv

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
        subdata=data[2].text.splitlines()
        casttime=re.search('\d+',subdata[0]).group().strip()
        actiontype=subdata[0].split()[-1].strip()
        the_range=subdata[1].replace("Range: ", "").strip()
        components=subdata[2].replace("Components: ", "").strip()
        duration=subdata[3].replace("Duration: ", "").strip()
        spelllists=data[-1].text.replace("Spell Lists. ", "")
        description="" 
        for i in data[3:-1]:
            description = description + i.text          
        print(description)
    except Exception as e:
        print(name)
        raise(e)


    # out structure
    out = {
        "name": name,
        "source": source,
        "level":level,
        "school": school,
        "casttime": casttime,
        "actiontype": actiontype,
        "range": the_range,
        "components": components,
        "duration": duration,
        "spelllists": spelllists,
        "description": description
    }
    out_all.append(out)

    #print(out)

out_all_str = json.dumps(out_all)
if Path("spell_data.json").is_file():
    os.remove("spell_data.json")
json_file = open("spell_data.json", "w")
json_file.write(out_all_str)
json_file.close()

if Path("spell_data.csv").is_file():
    os.remove("spell_data.csv")


# with open("spell_data.csv", "w") as csv_file:
#     csv_writer = csv.writer(csv_file)
#     out_keys = list(out_all[0].keys())
#     csv_writer.writerow(out_keys)


#     for row in out_all:
#         csv_writer.writerow([
#             row["name"],
#             row["source"],
#             row["level"],
#             row["school"],
#             row["casttime"],
#             row["actiontype"],
#             row["range"], 
#             row["components"],
#             row["duration"],
#             row["spelllists"],
#             row["description"]
#         ])

pd.read_json(out_all).to_csv('spell_data.csv', encoding='utf-8', index=False)
