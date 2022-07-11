import pandas as pd


def create_row(step, current_event, state, data, future_event_list):

    sorted_fel = sorted(future_event_list, key=lambda x: x["Event Time"])

    # What should this row contain?
    # 1. Step, Clock, Event Type and Event Customer
    row = [
        step,
        current_event["Event Time"],
        current_event["Event Type"],
        current_event["Customer"],
    ]
    # 2. All state variables
    row.extend(list(state.values()))
    # 3. All Cumulative Stats
    row.extend(list(data["Cumulative Stats"].values()))

    # row = [step, current_event['Event Type'], current_event['Event Time'],
    #        state['Queue Length'], state['Server Status'],
    # data['Cumulative Stats']['Server Busy Time'],

    #        data['Cumulative Stats']['Queue Waiting Time'],
    #        data['Cumulative Stats']['Area Under Queue Length Curve'],
    # data['Cumulative Stats']['Service Starters']]

    # 4. All events in fel ('Event Time', 'Event Type' & 'Event Customer'
    # for each event)
    for event in sorted_fel:
        row.append(event["Event Time"])
        row.append(event["Event Type"])
        row.append(event["Customer"])
    return row


def justify(table):
    # This function adds blanks to short rows in order
    # to match their lengths to the maximum row length

    # Find maximum row length in the table
    row_max_len = 0
    for row in table:
        if len(row) > row_max_len:
            row_max_len = len(row)

    # For each row, add enough blanks
    for row in table:
        row.extend([""] * (row_max_len - len(row)))


def create_main_header(state, data):
    # This function creates the main part of header (returns a list)
    # A part of header which is used for future events will be
    # created in create_excel()

    # Header consists of ...
    # 1. Step, Clock, Event Type and Event Customer
    header = ["Step", "Clock", "Event Type", "Event Customer"]
    # 2. Names of the state variables
    header.extend(list(state.keys()))
    # 3. Names of the cumulative stats
    header.extend(list(data["Cumulative Stats"].keys()))
    return header


def create_excel(table, header):
    # This function creates and fine-tunes the Excel output file

    # Find length of each row in the table
    row_len = len(table[0])

    # Find length of header (header does not include cells for
    # fel at this moment)
    header_len = len(header)

    # row_len exceeds header_len by (max_fel_length * 3)
    # (Event Type, Event Time & Customer for each event in FEL)
    # Extend the header with
    # 'Future Event Time', 'Future Event Type', 'Future Event Customer'
    # for each event in the fel with maximum size
    i = 1
    for col in range((row_len - header_len) // 3):
        header.append("Future Event Time " + str(i))
        header.append("Future Event Type " + str(i))
        header.append("Future Event Customer " + str(i))
        i += 1

    # Dealing with the output
    # First create a pandas DataFrame
    df = pd.DataFrame(table, columns=header, index=None)

    # Create a handle to work on the Excel file
    writer = pd.ExcelWriter("output.xlsx", engine="xlsxwriter")

    # Write out the Excel file to the hard drive
    df.to_excel(
        writer,
        sheet_name="Single-server Queue Output",
        header=False,
        startrow=1,
        index=False,
    )

    # Use the handle to get the workbook
    # (just library syntax, can be found with a simple search)
    workbook = writer.book

    # Get the sheet you want to work on
    worksheet = writer.sheets["Single-server Queue Output"]

    # Create a cell-formatter object
    # (this will be used for the cells in the header, hence: header_formatter!)
    header_formatter = workbook.add_format()

    # Define whatever format you want
    header_formatter.set_align("center")
    header_formatter.set_align("vcenter")
    header_formatter.set_font("Times New Roman")
    header_formatter.set_bold("True")

    # Write out the column names and apply the format to the cells in headerrow
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_formatter)

    # Auto-fit columns
    # Copied from
    # https://stackoverflow.com/questions/29463274/simulate-autofit-column-in-xslxwriter
    for i, width in enumerate(get_col_widths(df)):
        worksheet.set_column(i - 1, i - 1, width)

    # Create a cell-formatter object for the body of excel file
    main_formatter = workbook.add_format()
    main_formatter.set_align("center")
    main_formatter.set_align("vcenter")
    main_formatter.set_font("Times New Roman")

    # Apply the format to the body cells
    for row in range(1, len(df) + 1):
        worksheet.set_row(row, None, main_formatter)

    # Save your edits
    writer.save()


def get_col_widths(dataframe):
    # Copied from
    # https://stackoverflow.com/questions/29463274/simulate-autofit-column-in-xslxwriter
    # First we find the maximum length of the index column
    idx_max = max(
        [len(str(s)) for s in dataframe.index.values]
        + [len(str(dataframe.index.name))]
    )
    # Then, we concatenate this to the max of the lengths of column name and
    # its values for each column, left to right
    return [idx_max] + [
        max([len(str(s)) for s in dataframe[col].values] + [len(col)])
        for col in dataframe.columns
    ]
