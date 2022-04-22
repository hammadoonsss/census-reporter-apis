import json

from realestate_bot.settings import base_path

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
        print("Error in SC_JSON: ",e)

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
