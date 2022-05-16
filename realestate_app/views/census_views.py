import os
import requests

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.utils import convert_list_string, get_state_code

from realestate_bot.settings import base_url


def make_request(method, endpoint, data):
    """
        Function to make request to base_url with specific endpoints a/c to the method given
    """

    if method == "GET":
        try:
            # print("____", base_url + endpoint,)
            response = requests.get(base_url + endpoint, params=data)
        except Exception as e:
            print("Error in make Request GET")

    else:
        raise ValueError()

    if response.status_code == 200:
        return response.json()
    else:
        print("Error while making get request")


# Census Reporter APIs Evaluation

class AmericanCommunitySurveyData(APIView):

    def get(self, request):

        try:
            response = requests.get(
                f"{base_url}/1.0/data/show/latest?table_ids=B01001,B01002&geo_ids=16000US5367000")
            #    " https://api.censusreporter.org/1.0/data/show/latest?table_ids=B01001&geo_ids=16000US5367000")
            data_value = response.json()
            # print('data_value: \n', data_value)

            return Response(data_value)

        except Exception as e:
            print("Error : ", e)


class TabulationData(APIView):

    def get(self, request):

        try:
            response = requests.get(
                f"{base_url}/1.0/tabulation/02001")
            tabulation_data = response.json()
            # print('tabulation_data: \n', tabulation_data)

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
            # json0_data = json.dumps(all_states_data)
            # json1_data = json.loads(json0_data)
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
                f"{base_url}/1.0/data/show/latest?table_ids=B02001&geo_ids=050|04000US53")

            all_counties_data = response.json()
            # print('all_counties_data: \n', all_counties_data)

            return Response(all_counties_data)

        except Exception as e:
            print("Error in ACD: ", e)


class SingleTopicStateData(APIView):

    def post(self, request):

        try:
            data = dict()
            # data['latest'] = 'latest'
            # print('request.data: ', request.data)

            symbol_list = request.data.get('Symbol')
            multi_symbol = convert_list_string(symbol_list)
            data['table_ids'] = multi_symbol

            state_list = request.data.get('State')
            state_code_list = get_state_code(state_list)
            multi_state = convert_list_string(state_code_list)
            data['geo_ids'] = multi_state

            # data_value = make_request("GET", "/1.0/data/show/latest", data)
            # print("data_value: --++---", data_value)

            response = requests.get(
                f"{base_url}/1.0/data/show/latest?table_ids={multi_symbol}&geo_ids={multi_state}")

            data_value = response.json()

            return Response(data_value)

        except Exception as e:
            return Response({"Error in RMSD":  f"{e}"})

