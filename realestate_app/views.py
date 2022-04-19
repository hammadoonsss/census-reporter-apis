import os
import json
import time
import ftplib
import requests

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import County, Race, RaceError, RaceEstimate, State
from realestate_app.serializers import CountySerializer, RaceSerializer, StateSerializer

from realestate_bot.settings import FTP_HOST, FTP_PASS, FTP_USER


base_url = "https://api.censusreporter.org"
base_path = os.getcwd()


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


def upload_file():
    """
        Function to Upload JSON file on the FTP Server
    """

    try:
        ftp = ftp_connect()

        filename = f"{base_path}/static/upload/racedata.json"
        ftp.set_pasv(False)

        with open(filename, "rb") as file:
            # data = file.read()
            # print('data: ', data)
            ftp.storbinary("STOR Housing_App_Unit/racestatedata01.json", file)

    except Exception as e:
        print("Error in UPF:", e)


def get_server_file():
    """
        Funtion to get JSON file from the FTP Server
    """

    try:
        ftp = ftp_connect()

        filename = f"{base_path}/static/download/racedata.json"
        ftp.set_pasv(False)

        with open(filename, 'wb') as file:
            ftp.retrbinary(
                "RETR Housing_App_Unit/racestatedata01.json", file.write)

    except Exception as e:
        print("Error in GTF: ", e)


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


def get_state_dict(state):
    """
        Function to get US State Code based on their abbreviation dictionary
    """

    state_code = {
        "AL": "050|04000US01",
        "AK": "050|04000US02",
        "AZ": "050|04000US04",
        "AR": "050|04000US05",
        "CA": "050|04000US06",
        "CO": "050|04000US08",
        "CT": "050|04000US09",
        "DE": "050|04000US10",
        "DC": "050|04000US11",
        "FL": "050|04000US12",
        "GA": "050|04000US13",
        "HI": "050|04000US15",
        "ID": "050|04000US16",
        "IL": "050|04000US17",
        "IN": "050|04000US18",
        "IA": "050|04000US19",
        "KS": "050|04000US20",
        "KY": "050|04000US21",
        "LA": "050|04000US22",
        "ME": "050|04000US23",
        "MD": "050|04000US24",
        "MA": "050|04000US25",
        "MI": "050|04000US26",
        "MN": "050|04000US27",
        "MS": "050|04000US28",
        "MO": "050|04000US29",
        "MT": "050|04000US30",
        "NE": "050|04000US31",
        "NV": "050|04000US32",
        "NH": "050|04000US33",
        "NJ": "050|04000US34",
        "NM": "050|04000US35",
        "NY": "050|04000US36",
        "NC": "050|04000US37",
        "ND": "050|04000US38",
        "OH": "050|04000US39",
        "OK": "050|04000US40",
        "OR": "050|04000US41",
        "PA": "050|04000US42",
        "RI": "050|04000US44",
        "SC": "050|04000US45",
        "SD": "050|04000US46",
        "TN": "050|04000US47",
        "TX": "050|04000US48",
        "UT": "050|04000US49",
        "VT": "050|04000US50",
        "VA": "050|04000US51",
        "WA": "050|04000US53",
        "WV": "050|04000US54",
        "WI": "050|04000US55",
        "WY": "050|04000US56",
        "PR": "050|04000US72",
        "VI": "050|04000US78",
    }

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


def write_json_file(data):
    """
        Function to Write JSON File
    """

    try:
        file_path = f"{base_path}/static/upload/racedata.json"

        with open(file_path, "w") as f:
            f.write(data)

            f.close()

    except Exception as e:
        print("Error in WJF", e)


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


def read_json_file():

    try:
        file_path = f"{base_path}/static/download/racedata.json"

        with open(file_path, "r") as f:
            data = f.read()
            print('data in RJF:', type(data))
            f.close()

        data_dict = json.loads(data)
        print('data_dict in RJF:', type(data_dict))

        return data_dict

    except Exception as e:
        print("Error in RJF: ", e)


class AmericanCommunitySurveyData(APIView):

    def get(self, request):

        try:
            response = requests.get(
                f"{base_url}/data/show/acs2020_5yr?table_ids=B01001,B01002&geo_ids=16000US5367000")
            data_value = response.json()
            # print('data_value: \n', data_value)

            return Response(data_value)

        except Exception as e:
            print("Error : ", e)


class TabulationData(APIView):

    def get(self, request):

        try:
            response = requests.get(
                f"{base_url}/tabulation/02001")
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
            # print('all_counties_data: \n', all_counties_data)

            return Response(all_counties_data)

        except Exception as e:
            print("Error in ACD: ", e)


class RaceMultipleStateData(APIView):

    def post(self, request):

        try:
            data = dict()
            # data['latest'] = 'latest'
            # print('request.data: ', request.data)

            symbol_list = request.data.get('Symbol')
            multi_symbol = convert_list_string(symbol_list)
            data['table_ids'] = multi_symbol

            state_list = request.data.get('State')
            state_code_list = get_state_dict(state_list)
            multi_state = convert_list_string(state_code_list)
            data['geo_ids'] = multi_state

            data_value = make_request("GET", "/1.0/data/show/latest", data)
            # print("data_value: --++---", data_value)

            # response = requests.get(
            #     f"{base_url}/data/show/latest?table_ids={multi_symbol}&geo_ids={multi_state}")

            # race_data = response.json()

            return Response(data_value)

        except Exception as e:
            return Response({"Error in RMSD":  f"{e}"})


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
            print('race_data============: \n', type(race_data))

            s = json.dumps(race_data)
            print('s===========: \n', type(s))

            write_json_file(s)

            print("Before Ts json file write.")
            time.sleep(2)
            print("After Ts json file write.")

            # sftpExamp()
            try:
                upload_file()

                ftp = ftp_connect()
                ftp.set_pasv(False)
                ftp.dir("Housing_App_Unit/")

            except Exception as e:
                print("Error in ftp_upload inside:::", e)

            try:
                # print("---before getting a file")
                get_server_file()
                # print("---after getting a file")
            except Exception as e:
                print("Error in ftp_get inside::", e)

                ftp.quit()

            return Response(race_data)

        except Exception as e:
            return Response({"Error in RSSD":  f"{e}"})


class RaceCodeData(APIView):

    def get_and_create_race_data(self, data_dict):
        """
            Function to get Race Code Data from dictionary
            and populate Race Table 
        """

        try:
            print("try in GCRD: ", type(data_dict))
            data_value = data_dict['tables'].get('B02001').get('columns')
            print('values: ', data_value)

            for i in data_value:
                race_id = i
                race_name = data_value.get(i).get("name")

                try:
                    race_data = Race.objects.get(race_id=race_id)
                    print('GCRD-race_data: try get: \n', race_data)
                except:
                    racedb_data = Race.objects.create(
                        race_id=race_id,
                        race_name=race_name
                    )
                    print('GCRD-racedb_data: except create \n', racedb_data)

        except Exception as e:
            print("Error in GRD:", e)

    def get(self, request):

        try:
            race_data = Race.objects.all()
            if race_data.exists():
                print("Inside if --")
                race_serializer = RaceSerializer(race_data, many=True)
                return Response(race_serializer.data)
            else:
                print("inside else --")
                return Response("No Data Available")

        except Exception as e:
            print("Error in RRD-GET: ", e)

    def post(self, request):

        try:
            data_dict = read_json_file()
            # print('data_dict:======= ', data_dict)

            self.get_and_create_race_data(data_dict)

            return Response(data_dict)

        except Exception as e:
            print("Error in RRD-POST: ", e)


class StateCountyDetailData(APIView):

    def get_and_create_state_county_data(self, data_dict):
        """
            Function to get State/County Data from dictionary 
            and populate State/County Table 
        """

        try:
            print("try in GCCD: ", type(data_dict))
            data_value = data_dict['geography']
            # print('data_value: ', data_value)

            for i in data_value:

                code_initial = i
                code_name = data_value.get(code_initial).get("name")

                # Checking and Insert State's Detail
                if code_initial[0:5] == '04000':
                    print("Getting State", code_initial[5:9])

                    state_id = code_initial[5:9]
                    state_name = code_name
                    state_ref_id = code_initial

                    try:
                        state_data = State.objects.get(state_id=state_id)
                        print('GCCD-state_data: try get \n', state_data)
                    except:
                        statedb_data = State.objects.create(
                            state_id=state_id,
                            state_name=state_name,
                            state_ref_id=state_ref_id
                        )
                        print('GCCD-statedb_data: except create', statedb_data)

                # Checking and Insert County's Detail
                elif code_initial[0:5] == '05000':

                    county_id = code_initial
                    county_name = code_name.split(',')[0]
                    state_id = code_initial[5:9]

                    state_data = State.objects.get(state_id=state_id)

                    try:

                        county_data = County.objects.get(county_id=county_id)
                        print('GCCD-county_data: try get \n', county_data)
                    except:
                        county_data = County.objects.create(
                            county_id=county_id,
                            county_name=county_name,
                            state=state_data
                        )
                        print('GCCD-county_data: except create \n', county_data)

                else:
                    print("NOT Relevent Data")

        except Exception as e:
            print("Error in GCCD: ", e)

    def get(self, request):

        try:
            state_data = State.objects.all()
            county_data = County.objects.all()

            new_dict = {}

            if state_data.exists() and county_data.exists():
                print("Inside If --")
                state_serializer = StateSerializer(state_data, many=True)
                print('state_serializer: ', type(state_serializer))
                county_serializer = CountySerializer(county_data, many=True)

                new_dict['State'] = list(state_serializer.data)
                new_dict['County'] = list(county_serializer.data)

                state_county_data = json.dumps(new_dict)
                print('state_county_data: ', type(state_county_data))

                return Response(state_county_data)

            else:
                print("Inside else--")
                return Response("No Data Available")

        except Exception as e:
            print("Error in CD-GET: ", e)

    def post(self, request):

        try:
            data_dict = read_json_file()
            print('data_dict in CD : ', type(data_dict))

            self.get_and_create_state_county_data(data_dict)

            return Response(data_dict)

        except Exception as e:
            print("Error in CD-POST: ", e)


class RaceErrorEstimateData(APIView):

    def get_and_create_race_error_estimate(self, data_dict):

        try:
            print("In GCREE: ", type(data_dict))
            data_value = data_dict['data']
            print('data_value: ', data_value)

            county_data = County.objects.all()

            for county in county_data:

                if county.county_id in data_value:
                    print('county.county_id: ', county.county_id)

                    race_value = data_value.get(county.county_id).get("B02001")
                    print('race_value: ', race_value)

                    race_code = Race.objects.all()

                    for race in race_code:

                        # Race_Estimate
                        race_estimate = race_value.get(
                            'estimate').get(race.race_id)
                        print('race_estimate: -->', race_estimate)

                        try:
                            race_estimate_detail = RaceEstimate.objects.get(
                                county_id=county.county_id, race_id=race.race_id)
                            print('race_estimate_detail: In TRY=== ',
                                  race_estimate_detail)

                        except:

                            race_estimate_detail = RaceEstimate.objects.create(
                                race_estimate_value=race_estimate,
                                county_id=county.county_id,
                                race_id=race.race_id
                            )
                            print('race_estimate_detail: In EXCEPT=== ',
                                  race_estimate_detail)

                        # # Race_Error
                        # race_error = race_value.get('error').get(race.race_id)
                        # print('race_error: ==<', race_error)

                        # try:
                        #     race_error_detail = RaceError.objects.get(
                        #         county_id=county.county_id, race_id=race.race_id)
                        #     print('race_error_detail: In TRY---',
                        #           race_error_detail)

                        # except:

                        #     race_error_detail = RaceError.objects.create(
                        #         race_error_value=race_error,
                        #         county_id=county.county_id,
                        #         race_id=race.race_id
                        #     )
                        #     print('race_error_detail: In EXCEPT--',
                        #           race_error_detail)

        except Exception as e:
            print('Error in GCREE: ', e)

    def get(self, request):

        try:
            return Response("IN REED")
        except Exception as e:
            print("Error in REED-GET:", e)

    def post(self, request):

        try:
            data_dict = read_json_file()
            print('data_dict in REED: ', type(data_dict))

            self.get_and_create_race_error_estimate(data_dict)

            return Response(data_dict)

        except Exception as e:
            print("Error in REED-POST:", e)
