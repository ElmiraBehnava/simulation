from random_generetors import exponential, uniform


def fel_maker(
    future_event_list,
    event_type,
    clock,
    customer=None,
    customer_type=None,
    served_by=None,
):

    event_time = 0

    if event_type == "Arrival":
        event_time = clock + exponential(1 / 20)
    elif event_type == "End of Service":
        event_time = clock + uniform(10, 25)

    new_event = {
        "Event Type": event_type,
        "Event Time": event_time,
        "Customer": customer,
        "Customer Type": customer_type,
        "served_by": served_by,
    }
    future_event_list.append(new_event)
