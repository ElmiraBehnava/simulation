from random_generetors import exponential, uniform
from tools import shift


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

        if shift(clock) == 1:
            event_time = clock + exponential(1 / 3)
        if shift(clock) == 2:
            event_time = clock + exponential(1 / 1)
        if shift(clock) == 3:
            event_time = clock + exponential(1 / 2)
    elif event_type == "End of Service":
        if served_by:
            if "Expert" in served_by:
                event_time = clock + uniform(0, 3)
            elif "Amateur" in served_by:
                event_time = clock + uniform(0, 7)

        else:
            event_time = clock + uniform(10, 25)

    new_event = {
        "Event Type": event_type,
        "Event Time": event_time,
        "Customer": customer,
        "Customer Type": customer_type,
        "served_by": served_by,
    }
    future_event_list.append(new_event)
