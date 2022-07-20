def starting_state():

    state = dict()
    state["VIP Queue Length"] = 0
    state["Regular Queue Length"] = 0
    state["Recall Queue Length"] = 0

    state["First Expert Server Status"] = 0  # expert
    state["Second Expert Server Status"] = 0  # expert
    state["First Amateur Server Status"] = 0  # noob
    state["Second Amateur Server Status"] = 0  # noob
    state["Third Amateur Server Status"] = 0  # noob

    # Data: will save everything
    data = dict()
    data["Customers"] = dict()
    data["Last Time Regular Queue Length Changed"] = 0
    data["Last Time VIP Queue Length Changed"] = 0

    # data["Queue Customers"] = dict()
    data["Regular Queue Customers"] = dict()
    data["VIP Queue Customers"] = dict()
    data["Recall Queue Customers"] = dict()

    # Cumulative Stats
    data["Cumulative Stats"] = dict()
    data["Cumulative Stats"]["First Expert Server Busy Time"] = 0
    data["Cumulative Stats"]["Second Expert Server Busy Time"] = 0
    data["Cumulative Stats"]["First Amateur Server Busy Time"] = 0
    data["Cumulative Stats"]["Second Amateur Server Busy Time"] = 0
    data["Cumulative Stats"]["Third Amateur Server Busy Time"] = 0
    data["Cumulative Stats"]["Regular Queue Waiting Time"] = 0
    data["Cumulative Stats"]["VIP Queue Waiting Time"] = 0

    data["Cumulative Stats"]["Area Under Queue Length Curve"] = 0
    data["Cumulative Stats"]["Area Under VIP Queue Length Curve"] = 0
    data["Cumulative Stats"]["Area Under Regular Queue Length Curve"] = 0

    data["Cumulative Stats"]["Service Starters"] = 0

    # Starting FEL
    future_event_list = list()
    future_event_list.append(
        {
            "Event Type": "Arrival",
            "Event Time": 0,
            "Customer": "C1",
            "Customer Type": "Regular",
            "served_by": None,
        }
    )
    return state, future_event_list, data
