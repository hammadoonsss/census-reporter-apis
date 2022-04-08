import json
import requests

from rest_framework.views import APIView
from rest_framework.response import Response


base_url = "https://api.censusreporter.org"


def convert_list_string(code_list):
    
    try:

        if len(code_list) and type(code_list) == list:
            code_string = (',').join(code_list)
            print('code_string:-------------- ', code_string)
            return code_string
        else:
            print("In else+++++++++")
            return None
    except Exception as e:
        print("Error in CLS")


def get_state_dict(state):

    state_code = {
        "FL": "050|04000US12",
        "MA": "050|04000US25",
        "NJ": "050|04000US34",
        "NY": "050|04000US36",
        "OH": "050|04000US39",
    }

    state_list = []
    try:
        print("------0-00", state)

        for i in state:
            if i in state_code:
                state_list.append(state_code[i])
            else:
                return None
        return state_list
    except Exception as e:
        print("Error as in GSD")




def make_request(method, endpoint, data):
    """
        Function to make request to base_url with specific endpoints a/c to the method given
    """

    if method == "GET":
        try:
            print("_______________", base_url + endpoint,)
            response = requests.get(base_url + endpoint, params=data)
            print("---------------")
        except Exception as e:
            print("Error in make Request GET")

    else:
        raise ValueError()

    if response.status_code == 200:
        return response.json()
    else:
        print("Error while making get request")



class AmericanCommunitySurveyData(APIView):

    def get(self, request):

        try:
            response = requests.get(
                f"{base_url}/data/show/acs2020_5yr?table_ids=B01001,B01002&geo_ids=16000US5367000")
            data_value = response.json()
            print('data_value: \n', data_value)

            return Response(data_value)

        except Exception as e:
            print("Error : ", e)


class TabulationData(APIView):

    def get(self, request):

        try:
            response = requests.get(
                f"{base_url}/tabulation/02001")
            tabulation_data = response.json()
            print('tabulation_data: \n', tabulation_data)

            return Response(tabulation_data)

        except Exception as e:
            print("Error in CRD: ", e)

class AllStatesData(APIView):

    def get(self, request):

        try:
            response = requests.get(
                f"{base_url}/1.0/geo/show/tiger2020?geo_ids=040|01000US")

            all_states_data = response.json()
            # print('all_states_data: \n', all_states_data)
            json0_data = json.dumps(all_states_data)
            json1_data = json.loads(json0_data)
            # print('json1_data: \n', json1_data['features'])
            # for i in json1_data['features']:
            #     print ("____________", i)
            

            return Response(all_states_data)

        except Exception as e:
            print("Error in ASD: ", e)


class AllCountiesData(APIView):

    def get(self, request):

        try:
            response = requests.get(
                "https://api.censusreporter.org/1.0/data/show/latest?table_ids=B02001&geo_ids=050|04000US53")

            all_counties_data = response.json()
            print('all_counties_data: \n', all_counties_data)

            return Response(all_counties_data)

        except Exception as e:
            print("Error in ACD: ", e)


class RaceStateData(APIView):

    def post(self, request):

        try:
            print('request.data: ', request.data)

            symbol_list = request.data.get('Symbol')
            multi_symbol = convert_list_string(symbol_list)

            state_list = request.data.get('State')
            state_code_list = get_state_dict(state_list)
            multi_state = convert_list_string(state_code_list)

            response = requests.get(
                f"{base_url}/1.0/data/show/latest?table_ids={multi_symbol}&geo_ids={multi_state}")

            race_data = response.json()

            return Response(race_data)

        except Exception as e:
            return Response({"Error in RSSD":  f"{e}"})


class RaceMultipleStateData(APIView):

    def post(self, request):

        try:
            data = dict()
            # data['latest'] = 'latest'
            print('request.data: ', request.data)

            symbol_list = request.data.get('Symbol')
            multi_symbol = convert_list_string(symbol_list)
            data['table_ids'] = multi_symbol

            state_list = request.data.get('State')
            state_code_list = get_state_dict(state_list)
            multi_state = convert_list_string(state_code_list)
            data['geo_ids'] = multi_state

            data_value = make_request("GET", "/1.0/data/show/latest", data)
            print("data_value: -----------", data_value)

            # response = requests.get(
            #     f"{base_url}/data/show/latest?table_ids={multi_symbol}&geo_ids={multi_state}")

            # race_data = response.json()

            return Response(data_value)

        except Exception as e:
            return Response({"Error in RMSD":  f"{e}"})