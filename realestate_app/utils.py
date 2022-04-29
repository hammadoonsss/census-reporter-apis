import json
import ftplib

from realestate_bot.settings import (FTP_HOST, FTP_PASS, FTP_USER,
                                     base_path)


def ftp_connect():
    """
        Function for making Connection to FTP Server
    """
    try:
        # print("___--___", FTP_HOST, FTP_USER, FTP_PASS)
        # Connect to FTP Server
        ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
        print('ftp:--- ', ftp)
        # force utf-8 encoding
        ftp.encoding = "utf-8"
        return ftp

    except Exception as e:
        print("Error in ftp: \n", e)


def convert_list_string(code_list):
    """
        Function to Convert code_list into String format
    """

    try:

        if len(code_list) and type(code_list) == list:
            code_string = (',').join(code_list)
            # print('code_string:------- ', code_string, type(code_string))
            return code_string
        else:
            print("In CLS else")
            return None
    except Exception as e:
        print("Error in CLS")


def get_state_code(state):
    """
        Function to get US State Code 
        Based on their abbreviation dictionary
        From state_codes.json
    """

    try:
        state_code_path = f"{base_path}/static/state_codes.json"

        with open(state_code_path, 'r') as file:
            data = file.read()
            print('data++++++++++: ', data)

        state_code = json.loads(data)
        print('state_code: ', state_code)

    except Exception as e:
        print("Error in SC_JSON: ", e)

    state_list = []
    try:
        print("--state--0-", state)

        for i in state:
            if i in state_code:
                state_list.append(state_code[i])
            else:
                return None
        return state_list
    except Exception as e:
        print("Error as in GSD")


def json_file_write(data, name):
    """
        Function to Write JSON File
    """

    try:
        print('name',  name)
        file_path = f"{base_path}/static/upload/{name}"
        print('file_path: ', file_path)

        with open(file_path, "w") as f:
            f.write(data)
            f.close()
    except Exception as e:
        print("Error in WJF", e)


def upload_file_ftp(name):
    """
        Function to Upload JSON file on the FTP Server
    """

    try:
        ftp = ftp_connect()
        filename = f"{base_path}/static/upload/{name}"
        ftp.set_pasv(False)

        with open(filename, "rb") as file:
            # data = file.read()
            # print('data: ', data)
            ftp.storbinary(f"STOR Housing_App_Unit/{name}", file)
    except Exception as e:
        print("Error in UPF:", e)


def get_file_ftp(name):
    """
        Funtion to Download JSON file from the FTP Server
    """

    try:
        ftp = ftp_connect()
        filename = f"{base_path}/static/download/{name}"
        ftp.set_pasv(False)

        with open(filename, 'wb') as file:
            ftp.retrbinary(
                f"RETR Housing_App_Unit/{name}", file.write)

    except Exception as e:
        print("Error in GTF: ", e)


def json_file_read(name):

    try:
        file_path = f"{base_path}/static/download/{name}"

        with open(file_path, "r") as f:
            data = f.read()
            print('data in RJF:', type(data))
            f.close()

        data_dict = json.loads(data)
        print('data_dict in RJF:', type(data_dict))

        return data_dict

    except Exception as e:
        print("Error in RJF: ", e)
