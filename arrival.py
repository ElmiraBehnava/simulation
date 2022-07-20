import random

from fel_maker import fel_maker


def update_server_status(
    future_event_list, clock, data, customer, customer_type, server_name
):
    fel_maker(
        future_event_list,
        "End of Service",
        clock,
        customer,
        customer_type,
        server_name,
    )
    data["Customers"][customer]["Time Service Begins"] = clock
    data["Cumulative Stats"]["Service Starters"] += 1


def add_customer_to_queue(data, state, clock, customer, customer_type):
    if customer_type == "Regular":
        data["Cumulative Stats"][
            "Area Under Regular Queue Length Curve"
        ] += state["Regular Queue Length"] * (
            clock - data["Last Time Regular Queue Length Changed"]
        )
        if state["Regular Queue Length"] > 4:
            use_recall = random.choices(["Yes", "No"], weights=[50, 50], k=1)[
                0
            ]
            if use_recall == "Yes":
                state["Recall Queue Length"] += 1
                data["Recall Queue Customers"][customer] = clock
                print(data["Recall Queue Customers"])
            else:
                state["Regular Queue Length"] += 1

                data["Regular Queue Customers"][
                    customer
                ] = clock  # add this customer to the queue
                data["Last Time Regular Queue Length Changed"] = clock
        else:
            state["Regular Queue Length"] += 1
            data["Regular Queue Customers"][
                customer
            ] = clock  # add this customer to the queue
            data["Last Time Regular Queue Length Changed"] = clock
    if customer_type == "VIP":
        data["Cumulative Stats"]["Area Under VIP Queue Length Curve"] += state[
            "VIP Queue Length"
        ] * (clock - data["Last Time VIP Queue Length Changed"])

        if state["VIP Queue Length"] > 4:
            use_recall = random.choices(["Yes", "No"], weights=[50, 50], k=1)[
                0
            ]
            if use_recall == "Yes":
                state["Recall Queue Length"] += 1
                print(state["Recall Queue Length"])
                data["Recall Queue Customers"][customer] = clock
            else:
                state["VIP Queue Length"] += 1
                data["VIP Queue Customers"][
                    customer
                ] = clock  # add this customer to the queue
                data["Last Time VIP Queue Length Changed"] = clock
        else:
            state["VIP Queue Length"] += 1
            data["VIP Queue Customers"][
                customer
            ] = clock  # add this customer to the queue
            data["Last Time VIP Queue Length Changed"] = clock


def arrival(future_event_list, state, clock, data, customer, customer_type):

    data["Customers"][customer] = dict()
    data["Customers"][customer]["Arrival Time"] = clock
    data["Customers"][customer]["Customer Type"] = customer_type
    if customer_type == "Regular":
        if state["First Amateur Server Status"] == 0:
            state["First Amateur Server Status"] = 1
            update_server_status(
                future_event_list,
                clock,
                data,
                customer,
                customer_type,
                "First Amateur Server",
            )
        elif state["Second Amateur Server Status"] == 0:
            state["Second Amateur Server Status"] = 1
            update_server_status(
                future_event_list,
                clock,
                data,
                customer,
                customer_type,
                "Second Amateur Server",
            )
        elif state["Third Amateur Server Status"] == 0:
            state["Third Amateur Server Status"] = 1
            update_server_status(
                future_event_list,
                clock,
                data,
                customer,
                customer_type,
                "Third Amateur Server",
            )
        elif (
            all(
                [
                    state["First Amateur Server Status"] == 1,
                    state["Second Amateur Server Status"] == 1,
                    state["Third Amateur Server Status"] == 1,
                ]
            )
            and customer_type == "Regular"
        ):
            add_customer_to_queue(data, state, clock, customer, customer_type)

    if customer_type == "VIP":
        if state["First Expert Server Status"] == 0:
            state["First Expert Server Status"] = 1
            update_server_status(
                future_event_list,
                clock,
                data,
                customer,
                customer_type,
                "First Expert Server",
            )
        elif state["Second Expert Server Status"] == 0:
            state["Second Expert Server Status"] = 1
            update_server_status(
                future_event_list,
                clock,
                data,
                customer,
                customer_type,
                "Second Expert Server",
            )

        elif (
            all(
                [
                    state["First Expert Server Status"] == 1,
                    state["Second Expert Server Status"] == 1,
                ]
            )
            and customer_type == "VIP"
        ):
            add_customer_to_queue(data, state, clock, customer, customer_type)

    next_customer = "C" + str(int(customer[1:]) + 1)
    next_customer_type = random.choices(
        ["Regular", "VIP"], weights=[70, 30], k=1
    )[0]
    fel_maker(
        future_event_list,
        "Arrival",
        clock,
        next_customer,
        next_customer_type,
        None,
    )
