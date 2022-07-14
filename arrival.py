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


def add_customer_to_queue(data, state, clock, customer):
    data["Cumulative Stats"]["Area Under Queue Length Curve"] += state[
        "Queue Length"
    ] * (clock - data["Last Time Queue Length Changed"])
    state["Queue Length"] += 1
    data["Queue Customers"][customer] = clock  # add this customer to the queue
    data["Last Time Queue Length Changed"] = clock


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
                    state["First Amateur Server Status"],
                    state["Second Amateur Server Status"],
                    state["Third Amateur Server Status"],
                ]
            )
            and customer_type == "Regular"
        ):
            add_customer_to_queue(data, state, clock, customer)

        elif (
            all(
                [
                    state["First Amateur Server Status"],
                    state["Second Amateur Server Status"],
                    state["Third Amateur Server Status"],
                ]
            )
            and state["First Expert Server Status"] == 0
            and customer_type == "Regular"
        ):
            state["First Expert Server Status"] = 1
            update_server_status(
                future_event_list,
                clock,
                data,
                customer,
                customer_type,
                "First Expert Server Status",
            )
        elif (
            all(
                [
                    state["First Amateur Server Status"],
                    state["Second Amateur Server Status"],
                    state["Third Amateur Server Status"],
                ]
            )
            and state["Second Expert Server Status"] == 0
            and customer_type == "Regular"
        ):
            state["Second Expert Server Status"] = 1
            update_server_status(
                future_event_list,
                clock,
                data,
                customer,
                customer_type,
                "Second Expert Server Status",
            )

    if customer_type == "Expert":
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

        # if state["First Server Status"] == 0 and customer_type == "Regular":
        #     state["First Server Status"] = 1
        #     fel_maker(
        #         future_event_list,
        #         "End of Service",
        #         clock,
        #         customer,
        #         customer_type,
        #         "First Server",
        #     )
        #     data["Customers"][customer]["Time Service Begins"] = clock
        #     data["Cumulative Stats"]["Service Starters"] += 1

        # elif state["Second Server Status"] == 0 and customer_type == "VIP":
        #     state["Second Server Status"] = 1

        #     fel_maker(
        #         future_event_list,
        #         "End of Service",
        #         clock,
        #         customer,
        #         customer_type,
        #         "Second Server",
        #     )
        #     data["Customers"][customer]["Time Service Begins"] = clock
        #     data["Cumulative Stats"]["Service Starters"] += 1
        elif (
            all(
                [
                    state["First Expert Server Status"],
                    state["Second Expert Server Status"],
                ]
            )
            and customer_type == "VIP"
        ):
            add_customer_to_queue(data, state, clock, customer)

    # elif (
    #     all(
    #         [
    #             state["First Amateur Server Status"],
    #             state["Second Amateur Server Status"],
    #             state["Third Amateur Server Status"],
    #         ]
    #     )
    #     and customer_type == "Regular"
    # ):
    #     add_customer_to_queue(data, state, clock, customer)

    # elif (
    #     state["First Server Status"] == 1 and customer_type == "Regular"
    # ) or (
    #     state["Second Server Status"] == 1 and customer_type == "VIP"
    # ):  # if server is busy -> wait in queue
    #     data["Cumulative Stats"]["Area Under Queue Length Curve"] += state[
    #         "Queue Length"
    #     ] * (clock - data["Last Time Queue Length Changed"])
    #     state["Queue Length"] += 1
    #     data["Queue Customers"][
    #         customer
    #     ] = clock  # add this customer to the queue
    #     data["Last Time Queue Length Changed"] = clock

    next_customer = "C" + str(int(customer[1:]) + 1)
    next_customer_type = random.choices(["Regular", "VIP"], [70, 30])[0]
    fel_maker(
        future_event_list,
        "Arrival",
        clock,
        next_customer,
        next_customer_type,
        None,
    )
