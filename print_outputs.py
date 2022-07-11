def print_header():
    print(
        "Event Type".ljust(20)
        + "\t"
        + "Time".ljust(15)
        + "\t"
        + "Queue Length".ljust(15)
        + "\t"
        + "Server Status".ljust(25)
    )
    print(
        "---------------------------------------------------"
        + "----------------------------------------------"
    )


def nice_print(current_state, current_event):
    print(
        str(current_event["Event Type"]).ljust(20)
        + "\t"
        + str(round(current_event["Event Time"], 3)).ljust(15)
        + "\t"
        + str(current_state["Queue Length"]).ljust(15)
        + "\t"
        + str(current_state["Server Status"]).ljust(25)
    )
