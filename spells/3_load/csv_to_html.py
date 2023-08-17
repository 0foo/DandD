import pandas as pd
a = pd.read_csv("../format/spells.csv")
a.to_html("../format/spells.html", table_id="spells_table")