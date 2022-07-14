from fel_maker import fel_maker


def end_of_service(future_event_list, state, clock, data, customer, served_by):
    if served_by == "First Amateur Server":
        data["Cumulative Stats"]["First Amateur Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    elif served_by == "Second Amateur Server":
        data["Cumulative Stats"]["Second Amateur Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    elif served_by == "Third Amateur Server":
        data["Cumulative Stats"]["Third Amateur Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    elif served_by == "First Expert Server":
        data["Cumulative Stats"]["First Expert Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    elif served_by == "Second Expert Server":
        data["Cumulative Stats"]["Second Expert Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    if state["Queue Length"] == 0:
        state["First Expert Server Status"] = state[
            "Second Expert Server Status"
        ] = state["First Amateur Server Status"] = state[
            "Second Amateur Server Status"
        ] = state[
            "Third Amateur Server Status"
        ] = 0

    else:
        first_customer_in_queue = min(
            data["Queue Customers"], key=data["Queue Customers"].get
        )
        data["Customers"][first_customer_in_queue][
            "Time Service Begins"
        ] = clock
        first_customer_in_queue_type = data["Customers"][
            first_customer_in_queue
        ].get("Customer Type")
        data["Cumulative Stats"]["Queue Waiting Time"] += (
            clock - data["Customers"][first_customer_in_queue]["Arrival Time"]
        )

        data["Cumulative Stats"]["Queue Waiting Time"] += (
            clock - data["Customers"][first_customer_in_queue]["Arrival Time"]
        )

        data["Cumulative Stats"]["Area Under Queue Length Curve"] += state[
            "Queue Length"
        ] * (clock - data["Last Time Queue Length Changed"])

        state["Queue Length"] -= 1
        data["Cumulative Stats"]["Service Starters"] += 1
        data["Queue Customers"].pop(first_customer_in_queue, None)
        data["Last Time Queue Length Changed"] = clock
        fel_maker(
            future_event_list,
            "End of Service",
            clock,
            first_customer_in_queue,
            first_customer_in_queue_type,
        )
