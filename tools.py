def shift(clock):
    shifts_in_24 = 3
    # gets the clock and returns the shift number 1 ~ 3
    return clock % (24 * 60) // (24 * 60 // shifts_in_24) + 1

