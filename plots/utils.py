# numpy
import numpy as np
# datetime
import datetime as dt


def mavg(x_grid, n=2):
    # Check if n is a positive integer
    if not abs( int(n) ) == n:
        raise ValueError('The parameter n must be a positive integer or zero.')

    # Treat the special case 'n=0'
    if n == 0:
        return x_grid

    cx_grid = np.cumsum( np.insert(x_grid, 0, 0.) )

    # Calculate the averaged grids
    ax_grid = ( cx_grid[n:] - cx_grid[:-n] ) / float(n)

    # Append the first and last element
    #ax_grid = np.array( [ x_grid[0], *ax_grid, x_grid[-1] ] )

    return ax_grid


def correct_data(data):
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

        #print(current_date)

        # Increase the date by one and check if the entry exists
        while True:
            last_date += dt.timedelta(days=1)

            if last_date != current_date:
                result.append( [last_date.strftime("%Y-%m-%d"), *last_data[1:]] )
            else:
                result.append( [current_date.strftime("%Y-%m-%d"), *current_data[1:]] )

                last_data = current_data
                break
    
    return np.array(result)