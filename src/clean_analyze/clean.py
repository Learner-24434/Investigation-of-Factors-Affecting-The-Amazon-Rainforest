import regex as re

new = open("../data/Sahara/new_east_vel_850hpa.csv", "w")

with open("../data/Sahara/east_vel_850hpa.csv", "r") as old:
    for line in old.readlines():

        pattern = r"^(?P<month>0?[1-9]|1[0-2])-(?P<day>0?[1-9]|[12]\d|3[01])-(?P<year>\d{4}) (?P<time>\d{2}:\d{2}:\d{2}),(?P<value>-?\d+(?:\.\d+)?)$"

        match = re.match(pattern, line)

        if match:
            # Extract directly in Year, Month, Day order
            year = match.group("year")
            month = match.group("month").zfill(2)
            day = match.group("day").zfill(2)
            time = match.group("time")
            value = match.group("value")

            print(f"Year: {year}, Month: {month}, Day: {day}")
            print(f"YMD format: {year}-{month.zfill(2)}-{day.zfill(2)}")
            print(f"Time: {time}, Value: {value}")

            line = year+"-"+month+" "+day+" "+time+","+value + '\n'

            new.write(line)

new.close()