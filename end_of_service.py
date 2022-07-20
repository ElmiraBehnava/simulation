from fel_maker import fel_maker


def end_of_service(future_event_list, state, clock, data, customer, served_by):
    if served_by == "First Amateur Server":
        data["Cumulative Stats"]["First Amateur Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    if served_by == "Second Amateur Server":
        data["Cumulative Stats"]["Second Amateur Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    if served_by == "Third Amateur Server":
        data["Cumulative Stats"]["Third Amateur Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    if served_by == "First Expert Server":
        data["Cumulative Stats"]["First Expert Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    if served_by == "Second Expert Server":
        data["Cumulative Stats"]["Second Expert Server Busy Time"] += (
            clock - data["Customers"][customer]["Time Service Begins"]
        )
        data["Customers"].pop(customer, None)  # remove customer from data

    if state["Regular Queue Length"] == 0 and state["VIP Queue Length"] == 0:
        state["First Amateur Server Status"] = state[
            "Second Amateur Server Status"
        ] = state["Third Amateur Server Status"] = state[
            "First Expert Server Status"
        ] = state[
            "Second Expert Server Status"
        ] = 0

    else:
        first_regular_customer_in_queue = first_vip_customer_in_queue = None
        if len(data["Regular Queue Customers"]) != 0:
            first_regular_customer_in_queue = min(
                data["Regular Queue Customers"],
                key=data["Regular Queue Customers"].get,
            )

            data["Customers"][first_regular_customer_in_queue][
                "Time Service Begins"
            ] = clock

            data["Cumulative Stats"]["Regular Queue Waiting Time"] += (
                clock
                - data["Customers"][first_regular_customer_in_queue][
                    "Arrival Time"
                ]
            )

            data["Cumulative Stats"][
                "Area Under Regular Queue Length Curve"
            ] += state["Regular Queue Length"] * (
                clock - data["Last Time Regular Queue Length Changed"]
            )

            state["Regular Queue Length"] -= 1
            data["Cumulative Stats"]["Service Starters"] += 1
            data["Regular Queue Customers"].pop(
                first_regular_customer_in_queue, None
            )
            data["Last Time Regular Queue Length Changed"] = clock
            fel_maker(
                future_event_list,
                "End of Service",
                clock,
                first_regular_customer_in_queue,
                "Regular",
            )

        if len(data["VIP Queue Customers"]) != 0:
            first_vip_customer_in_queue = min(
                data["VIP Queue Customers"],
                key=data["VIP Queue Customers"].get,
            )
            data["Customers"][first_vip_customer_in_queue][
                "Time Service Begins"
            ] = clock

            data["Cumulative Stats"]["VIP Queue Waiting Time"] += (
                clock
                - data["Customers"][first_vip_customer_in_queue][
                    "Arrival Time"
                ]
            )

            data["Cumulative Stats"][
                "Area Under VIP Queue Length Curve"
            ] += state["VIP Queue Length"] * (
                clock - data["Last Time VIP Queue Length Changed"]
            )

            state["VIP Queue Length"] -= 1
            data["Cumulative Stats"]["Service Starters"] += 1
            data["VIP Queue Customers"].pop(first_vip_customer_in_queue, None)
            data["Last Time VIP Queue Length Changed"] = clock
            fel_maker(
                future_event_list,
                "End of Service",
                clock,
                first_vip_customer_in_queue,
                "VIP",
            )

        # if first_regular_customer_in_queue is not None:
        #     data["Customers"][first_regular_customer_in_queue][
        #         "Time Service Begins"
        #     ] = clock
        #     # first_customer_in_queue_type = data["Customers"][
        #     #     first_customer_in_queue
        #     # ].get("Customer Type")
        #     data["Cumulative Stats"]["Regular Queue Waiting Time"] += (
        #         clock
        #         - data["Customers"][first_regular_customer_in_queue][
        #             "Arrival Time"
        #         ]
        #     )

        #     # data["Cumulative Stats"]["Regular Queue Waiting Time"] += (
        #     #     clock
        #     #     - data["Customers"][first_vip_customer_in_queue][
        #     #         "Arrival Time"
        #     #     ]
        #     # )

        #     data["Cumulative Stats"]["Area Under Queue Length Curve"] += state[
        #         "Regular Queue Length"
        #     ] * (clock - data["Last Time Queue Length Changed"])

        #     state["Regular Queue Length"] -= 1
        #     data["Cumulative Stats"]["Service Starters"] += 1
        #     data["Queue Customers"].pop(first_vip_customer_in_queue, None)
        #     data["Last Time Queue Length Changed"] = clock
        #     fel_maker(
        #         future_event_list,
        #         "End of Service",
        #         clock,
        #         first_vip_customer_in_queue,
        #         "Regular",
        #     )
