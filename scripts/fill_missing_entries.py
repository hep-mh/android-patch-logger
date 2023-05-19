# numpy
import numpy as np
# datetime
import datetime as dt
# sys
import sys

input_file = sys.argv[1]
# -->
output_file = input_file

data = np.loadtxt(input_file, dtype=str)

result = []

# Initialize the relevant variables with the first entry...
last_data = data[0]
# -->
last_date = dt.datetime.strptime(last_data[0], "%Y-%m-%d").date()

result.append([*last_data])

# Loop over the remaining entries
for i, current_data in enumerate(data[1:]):
    current_date = dt.datetime.strptime(current_data[0], "%Y-%m-%d").date()

    # Skip over double entries
    if current_date <= last_date:
        continue

    print(current_date)

    # Increase the date by one and check if the entry exists
    while True:
        last_date += dt.timedelta(days=1)

        if last_date != current_date:
            result.append( [last_date.strftime("%Y-%m-%d"), *last_data[1:]] )
        else:
            result.append( [current_date.strftime("%Y-%m-%d"), *current_data[1:]] )

            last_data = current_data
            break
        

# Write the result to the output file
with open(output_file, "w") as f:
    for r in result:
        line = " ".join(r) + "\n"
        f.write(line)
