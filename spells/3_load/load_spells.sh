# create spell table from schema
sqlite3 DandD.db < ./create_spell_table.sql


# populate spells table
sqlite3 DandD.db <<EOF
.mode csv
.import ../2_transform/spell_data.csv spells
EOF


# output info
echo "Rows in spells database:"
sqlite3 DandD.db "SELECT COUNT(*) FROM spells"


# create csv file 
sqlite3 DandD.db <<EOF
.mode csv
.headers on
.output ../format/spells.csv
SELECT * FROM spells
EOF

# create html file
rm ../format/spells.html
python3 ./csv_to_html.py

