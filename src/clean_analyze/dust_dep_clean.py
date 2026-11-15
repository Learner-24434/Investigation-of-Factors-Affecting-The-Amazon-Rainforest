import csv

amzn = open("../data/Amazon/dust_dep.csv", "w")
amzn_ne = open("../data/Amazon/dust_dep_ne.csv", "w")
amzn_sw = open("../data/Amazon/dust_dep_sw.csv", "w")
atlantic = open("../data/Atlantic/dust_dep.csv", "w")
sahara = open("../data/Sahara/dust_dep.csv", "w")

with open("../data/dust_dep_widrl.csv", "r") as db:

    reader = csv.DictReader(db)

    # Add headers
    header = "date,emission_Tg,dry_dep_Tg,sediment_Tg,wet_dep_Tg,conv_scav_Tg,total_dep_Tg,emission_g_m2,total_dep_g_m2\n"

    amzn.write(header)
    amzn_ne.write(header)
    amzn_sw.write(header)
    atlantic.write(header)
    sahara.write(header)

    for record in reader:
        date, box, boxA, emission, dry_dep, sediment, wet_dep, conv_scav, total_dep, emission_gm2, total_dep_gm2 = record.values()
        line = f"{date},{emission},{dry_dep},{sediment},{wet_dep},{conv_scav},{total_dep},{emission_gm2},{total_dep_gm2}\n"
        print(box)
        match box:
            case "Amazon":
                amzn.write(line)
            case "Amazon_NE":
                amzn_ne.write(line)
            case "Amazon_SW":
                amzn_sw.write(line)
            case "Atlantic":
                atlantic.write(line)
            case "Sahara":
                sahara.write(line)

amzn.close()
amzn_ne.close()
amzn_sw.close()
atlantic.close()
sahara.close()
