import random

from fel_maker import fel_maker


def arrival(future_event_list, state, clock, data, customer, customer_type):

    data["Customers"][customer] = dict()
    data["Customers"][customer]["Arrival Time"] = clock
    data["Customers"][customer]["Customer Type"] = customer_type
    if state["First Server Status"] == 0 and customer_type == "":
        state["First Server Status"] = 1
        fel_maker(
            future_event_list,
            "End of Service",
            clock,
            customer,
            customer_type,
            "First Server",
        )
        data["Customers"][customer]["Time Service Begins"] = clock
        data["Cumulative Stats"]["Service Starters"] += 1

    elif state["Second Server Status"] == 0 and customer_type == "VIP":
        state["Second Server Status"] = 1

        fel_maker(
            future_event_list,
            "End of Service",
            clock,
            customer,
            customer_type,
            "Second Server",
        )
        data["Customers"][customer]["Time Service Begins"] = clock
        data["Cumulative Stats"]["Service Starters"] += 1

    elif (
        state["First Server Status"] == 1 and customer_type == "Regular"
    ) or (
        state["Second Server Status"] == 1 and customer_type == "VIP"
    ):  # if server is busy -> wait in queue
        data["Cumulative Stats"]["Area Under Queue Length Curve"] += state[
            "Queue Length"
        ] * (clock - data["Last Time Queue Length Changed"])
        state["Queue Length"] += 1
        data["Queue Customers"][
            customer
        ] = clock  # add this customer to the queue
        data["Last Time Queue Length Changed"] = clock

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
