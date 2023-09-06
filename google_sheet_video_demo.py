import gspread
from ox_script import *
import datetime

worksheet: gspread.client = []


def connect_to_worksheet(google_connection_key):
    global worksheet

    gc = gspread.service_account(filename=google_connection_key)
    sh = gc.open("google_sheet_print_demo")
    worksheet = sh.sheet1


def print_label(row_values):
    cmd = PTK_UpdateAllFormVariables(
        "rfid.prn",
        Input1=str(row_values[0]),
        Input2=str(row_values[1]),
        Input3=str(row_values[2]),
        Input4=str(row_values[3]),
    )
    PTK_SendCmdToPrinter(cmd)


def update_document(row, tid):
    global worksheet

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.update_cell(row, 6, now)  # Update "Printed_At" column
    worksheet.update_cell(row, 7, "GX Series")
    worksheet.update_cell(row, 8, tid)


TID_controller = None
row = 2


def one_cycle():
    global TID_controller
    global worksheet
    global row

    data = PTK_ReadRFID(TID)
    if data != -1:
        data = data[0:20]
        PTK_SetLabelHeight(height=32.6)
        print_label(worksheet.row_values(row))
        TID_controller.update(data)
        update_document(row, data)
        row += 1


if __name__ == "__main__":
    connect_to_worksheet("sound-service-378703-af433ab42907.json")
    PTK_UIInit(
        PTK_UIPage(
            TID_controller := PTK_UITextBox(title="Tag TID:", value="--"),
            PTK_UIButton(title="Start Reading", Onpressed=one_cycle),
        ),
    )
