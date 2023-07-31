from bs4 import BeautifulSoup
import re, os
import sqlite3
from pathlib import Path
import pandas as pd
import json 

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
        description=data[3].text,
        spelllists=data[4].text.replace("Spell Lists. ", "")
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
        "description": description,
        "spelllists": spelllists
    }
    out_all.append(out)

    #print(out)

out_all = json.dumps(out_all)
os.remove("spell_data.json")
json_file = open("spell_data.json", "w")
json_file.write(out_all)
json_file.close()


csv_string = pd.read_json(out_all).to_csv('spell_data.csv', encoding='utf-8', index=False)
