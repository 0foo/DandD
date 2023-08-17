import pandas as pd
import csv, json

def csv_to_json(in_csv_file, out_json_file):
    out_json_list = []
    with open(in_csv_file) as csv_file:
        csvReader = csv.DictReader(csv_file)
        for row in csvReader:
            out_json_list.append(row)
    with open(out_json_file, "w") as json_file:
        json_file.write(json.dumps(out_json_list))


a = pd.read_csv("../format/spells.csv")
a.to_html("../format/spells.html", table_id="spells_table")
csv_to_json("../format/spells.csv", "../format/spells.json")
# a.to_json("../format/spells.json", orient="records")