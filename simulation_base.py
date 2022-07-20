from arrival import arrival
from create_excel import create_excel, create_main_header, create_row, justify
from end_of_service import end_of_service
from starting_state import starting_state


def simulation(simulation_time):

    state, future_event_list, data = starting_state()
    clock = 0
    table = []
    step = 1

    future_event_list.append(
        {
            "Event Type": "End of Simulation",
            "Event Time": simulation_time,
            "Customer": None,
            "served_by": None,
            "Customer Type": None,
        }
    )

    while clock < simulation_time:
        sorted_fel = sorted(future_event_list, key=lambda x: x["Event Time"])

        current_event = sorted_fel[0]
        clock = current_event["Event Time"]
        customer = current_event["Customer"]
        served_by = current_event["served_by"]
        customer_type = current_event["Customer Type"]
        if clock < simulation_time:
            if current_event["Event Type"] == "Arrival":
                arrival(
                    future_event_list,
                    state,
                    clock,
                    data,
                    customer,
                    customer_type,
                )
            elif current_event["Event Type"] == "End of Service":
                end_of_service(
                    future_event_list, state, clock, data, customer, served_by
                )
            future_event_list.remove(current_event)
        else:
            future_event_list.clear()

        table.append(
            create_row(step, current_event, state, data, future_event_list)
        )
        step += 1

    print(
        "-------------------------------------------------"
        + "------------------------------------------------"
    )
    print("Simulation Ended!\n")
    excel_main_header = create_main_header(state, data)
    justify(table)

    create_excel(table, excel_main_header)
    Lq = (
        (
            data["Cumulative Stats"]["Area Under VIP Queue Length Curve"]
            + data["Cumulative Stats"]["Area Under Regular Queue Length Curve"]
        )
        / simulation_time
        * 5
    )
    Wq = (
        data["Cumulative Stats"]["Regular Queue Waiting Time"]
        + data["Cumulative Stats"]["VIP Queue Waiting Time"]
    ) / data["Cumulative Stats"]["Service Starters"]
    rho = (
        data["Cumulative Stats"]["First Expert Server Busy Time"]
        + data["Cumulative Stats"]["Second Expert Server Busy Time"]
        + data["Cumulative Stats"]["First Amateur Server Busy Time"]
        + data["Cumulative Stats"]["Second Amateur Server Busy Time"]
        + data["Cumulative Stats"]["Third Amateur Server Busy Time"]
    ) / (simulation_time * 5)

    print(f"Lq = {Lq}")
    print(f"Wq = {Wq}")
    print(f"rho = {rho}")

    print("\nChecking Little's Law")
    print(f"Lq = {Lq}")
    print(f"lambda * Wq = {(1 / 20) * Wq}")

    print("\nDo they match?")
    print(f"Ratio: {Lq / ((1 / 20) * Wq)}")

    if 0.9 < Lq / ((1 / 20) * Wq) < 1.1:
        print("Well... Almost!")


simulation(30 * 60 * 24)
