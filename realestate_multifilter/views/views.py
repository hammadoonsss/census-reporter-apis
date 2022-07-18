from django.db.models import F

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import (
    County, State, 
    RaceEstimate, RaceStateTotal, 
    IncomeEstimate, IncomeStateTotal
)

from realestate_education.models import (
    EducationEstimate, EducationStateTotal
)

from realestate_poverty.models import (
    PovertyEstimate, PovertyStateTotal
)

import collections
import functools
import operator

# -----------------------------------------------TOP State -------------------------------------------------------------


class TopicTopState(APIView):

    def post(self, request):
        if request.data:

            topic_name = request.data.get('Topic_Name')
            print('topic_name: ', topic_name)
            count = request.data.get('Count')
            print('count: ', count)
            type_filter = request.data.get('Type')
            print('type_filter: ', type_filter)
            # filter = request.data.get('Filter')
            # print('filter: ', filter)

            first_data = 'B02001002'
            second_data = 'B19001002'
            third_data = 'B15003002'
            fourth_data = 'B17001002'

            list1 = []
            list2 = []
            list3 = []
            list4 = []

            if topic_name[0]['Race'] == first_data:
                Race_value = topic_name[0]['value']

                race_state_top = RaceStateTotal.objects.exclude(race_id='B02001001').annotate(
                    percent=F('race_total')*100/F('state_total'))

                if type_filter == "Top":
                    race_state_top = race_state_top.order_by(
                        '-percent')[:count]
                    print('race_state_top------------: ', race_state_top)

                elif type_filter == "Bottom":
                    race_state_top = race_state_top.order_by(
                        'percent')[:count]
                    print('race_state_top********------------:',
                          race_state_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                # print('Race State TOP:*******************>>>>> ', race_state_top)
                race_state_top_list = []
                if race_state_top.exists():

                    for data in race_state_top:
                        ra_st_data = {}
                        ra_st_data['State_name'] = data.state.state_name

                        race_state_top_list.append(ra_st_data)
                        list1.append(data.state.state_name)
                        dic = {}
                        dic[data.state.state_name] = Race_value/count
                        list2.append(dic)
                        print('list2::Race-------: ', list2)
                        print("******list1:: Race", list1)

            else:
                return Response({"error": "Invalid Input value topic name RACE"})

            if topic_name[1]['Income'] == second_data:
                income_value = topic_name[1]['value']

                income_state_top = IncomeStateTotal.objects.exclude(income_id='B19001001').annotate(
                    percent=F('income_total')*100/F('state_total'))
                # print('Income State TOP: ----------->>>>>>', income_state_top)
                if type_filter == "Top":
                    income_state_top = income_state_top.order_by(
                        '-percent')[:count]
                    print('income_state_top: ', income_state_top)

                elif type_filter == "Bottom":
                    income_state_top = income_state_top.order_by(
                        'percent')[:count]
                    print('income_state_top:',
                          income_state_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                income_state_top_list = []
                if income_state_top.exists():
                    for data in income_state_top:
                        in_st_data = {}
                        in_st_data['State_name'] = data.state.state_name

                        income_state_top_list.append(in_st_data)
                        list1.append(data.state.state_name)
                        dic = {}
                        dic[data.state.state_name] = income_value/count
                        list2.append(dic)
                        print("list2::Income------", list2)
                        print("******list1:: Income", list1)

                        # result = dict(functools.reduce(operator.add,map(collections.Counter, list2)))
                        # print('result: ', result)

            else:
                return Response({"error": "Invalid Input value topic name INCOME"})

            if topic_name[2]['Education'] == third_data:
                education_value = topic_name[2]['value']

                education_state_top = EducationStateTotal.objects.exclude(education_id='B15003001').annotate(
                    percent=F('education_total')*100/F('state_total'))
                # print('Income State TOP: ----------->>>>>>', education_state_top)
                if type_filter == "Top":
                    education_state_top = education_state_top.order_by(
                        '-percent')[:count]
                    print('education_state_top: ', education_state_top)

                elif type_filter == "Bottom":
                    education_state_top = education_state_top.order_by(
                        'percent')[:count]
                    print('education_state_top:',
                          education_state_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                education_state_top_list = []
                if education_state_top.exists():
                    for data in education_state_top:
                        ed_st_data = {}
                        ed_st_data['State_name'] = data.state.state_name

                        education_state_top_list.append(ed_st_data)
                        list3.append(data.state.state_name)
                        dic = {}
                        dic[data.state.state_name] = education_value/count
                        list2.append(list3)
                        list2.append(dic)
                        print('list2::Education------: ', list2)

            else:
                return Response({"error": "Invalid Input value topic name EDUCATION"})

            if topic_name[3]['Poverty'] == fourth_data:
                poverty_value = topic_name[3]['value']

                poverty_state_top = PovertyStateTotal.objects.exclude(poverty_id='B17001001').annotate(
                    percent=F('poverty_total')*100/F('state_total'))
                # print('Income State TOP: ----------->>>>>>', poverty_state_top)
                if type_filter == "Top":
                    poverty_state_top = poverty_state_top.order_by(
                        '-percent')[:count]
                    print('poverty_state_top: ', poverty_state_top)

                elif type_filter == "Bottom":
                    poverty_state_top = poverty_state_top.order_by(
                        'percent')[:count]
                    print('poverty_state_top:',
                          poverty_state_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                poverty_state_top_list = []
                if poverty_state_top.exists():
                    for data in poverty_state_top:
                        pv_st_data = {}
                        pv_st_data['State_name'] = data.state.state_name

                        poverty_state_top_list.append(pv_st_data)
                        list4.append(data.state.state_name)
                        dic = {}
                        dic[data.state.state_name] = poverty_value/count
                        list2.append(list4)
                        list2.append(dic)
                        print('list2::Poverty--------- ', list2)

                        result = functools.reduce(
                            operator.add, map(collections.Counter, list2))
                        print('result: ', result)
                        result = sorted(
                            result.items(), key=operator.itemgetter(1), reverse=True)
                        result = result[:count]
                        result = dict(result)
                        print("result----------", result)
            else:
                return Response({"error": "Invalid Input value topic name Poverty"})

            return Response({"result": result})
        else:
            return Response({'error': 'invalid request'})

# -----------------------------------------------TOP County-------------------------------------------------------------


class TopicTopCounty(APIView):

    def post(self, request):

        if request.data:

            topic_name = request.data.get('Topic_Name')
            print('topic_name: ', topic_name)
            count = request.data.get('Count')
            print('count: ', count)
            type_filter = request.data.get('Type')
            print('type_filter: ', type_filter)

            first_data = 'B02001002'
            second_data = 'B19001002'
            third_data = 'B15003002'
            fourth_data = 'B17001002'

            list1 = []
            list2 = []
            list3 = []
            list4 = []

            if topic_name[0]['Race'] == first_data:
                Race_value = topic_name[0]['value']

                race_county_top = RaceEstimate.objects.exclude(race_id='B02001001').annotate(
                    percent=F('race_estimate_value')*100/F('county__race_total'))

                if type_filter == "Top":
                    race_county_top = race_county_top.order_by(
                        '-percent')[:count]
                    print('race_county_top------------: ', race_county_top)

                elif type_filter == "Bottom":
                    race_county_top = race_county_top.order_by(
                        'percent')[:count]
                    print('race_county_top********------------:',
                          race_county_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                race_county_top_list = []
                if race_county_top.exists():

                    for data in race_county_top:
                        ra_ct_data = {}
                        ra_ct_data['County_name'] = data.county.county_name

                        race_county_top_list.append(ra_ct_data)
                        list1.append(data.county.county_name)
                        dic = {}
                        dic[data.county.county_name] = Race_value/count
                        list2.append(dic)
                        print('list2:/----/ ', list2)

            else:
                return Response({"error": "Invalid Input value topic name RACE"})

            if topic_name[1]['Income'] == second_data:
                income_value = topic_name[1]['value']

                income_county_top = IncomeEstimate.objects.exclude(income_id='B19001001').annotate(
                    percent=F('income_estimate_value')*100/F('county__income_total'))

                if type_filter == "Top":
                    income_county_top = income_county_top.order_by(
                        '-percent')[:count]
                    print('income_county_top: ', income_county_top)

                elif type_filter == "Bottom":
                    income_county_top = income_county_top.order_by(
                        'percent')[:count]
                    print('income_county_top:',
                          income_county_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                income_county_top_list = []
                if income_county_top.exists():
                    for data in income_county_top:
                        in_ct_data = {}
                        in_ct_data['County_Name'] = data.county.county_name

                        income_county_top_list.append(in_ct_data)
                        list1.append(data.county.county_name)
                        dic = {}
                        dic[data.county.county_name] = income_value/count
                        list2.append(dic)

            else:
                return Response({"error": "Invalid Input value topic name INCOME"})

            if topic_name[2]['Education'] == third_data:
                education_value = topic_name[2]['value']

                education_county_top = EducationEstimate.objects.exclude(education_id='B15003001').annotate(
                    percent=F('education_estimate_value')*100/F('county__education_total'))

                if type_filter == "Top":
                    education_county_top = education_county_top.order_by(
                        '-percent')[:count]
                    print('education_county_top: ', education_county_top)

                elif type_filter == "Bottom":
                    education_county_top = education_county_top.order_by(
                        'percent')[:count]
                    print('education_county_top:',
                          education_county_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                education_county_top_list = []
                if education_county_top.exists():
                    for data in education_county_top:
                        ed_ct_data = {}
                        ed_ct_data['County_Name'] = data.county.county_name

                        education_county_top_list.append(ed_ct_data)
                        list3.append(data.county.county_name)
                        dic = {}
                        dic[data.county.county_name] = education_value/count
                        list2.append(list3)
                        list2.append(dic)

            else:
                return Response({"error": "Invalid Input value topic name EDUCATION"})

            if topic_name[3]['Poverty'] == fourth_data:
                poverty_value = topic_name[3]['value']

                poverty_county_top = PovertyEstimate.objects.exclude(poverty_id='B17001001').annotate(
                    percent=F('poverty_estimate_value')*100/F('county__poverty_total'))

                if type_filter == "Top":
                    poverty_county_top = poverty_county_top.order_by(
                        '-percent')[:count]
                    print('poverty_county_top: ', poverty_county_top)

                elif type_filter == "Bottom":
                    poverty_county_top = poverty_county_top.order_by(
                        'percent')[:count]
                    print('poverty_county_top:',
                          poverty_county_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                poverty_county_top_list = []
                if poverty_county_top.exists():
                    for data in poverty_county_top:
                        pv_ct_data = {}
                        pv_ct_data['County_Name'] = data.county.county_name

                        poverty_county_top_list.append(pv_ct_data)
                        list4.append(data.county.county_name)
                        dic = {}
                        dic[data.county.county_name] = poverty_value/count
                        list2.append(list4)
                        list2.append(dic)
                        print('list3: ', list3)
                        print("list2****---", list2)
                        print("******list1*****", list1)

                        result = dict(functools.reduce(
                            operator.add, map(collections.Counter, list2)))
                        print('result: ', result)
                        result = sorted(
                            result.items(), key=operator.itemgetter(1), reverse=True)
                        result = result[:count]
                        result = dict(result)

            else:
                return Response({"error": "Invalid Input value topic name Poverty"})

            return Response({"result": result})
        else:
            return Response({'error': 'invalid request'})

# -----------------------------------------------TOP State County-------------------------------------------------------------


class TopicTopStateCounty(APIView):

    def post(self, request):
        if request.data:
            topic_name = request.data.get('Topic_Name')
            print('topic_name: ', topic_name)
            count = request.data.get('Count')
            print('count: ', count)
            type_filter = request.data.get('Type')
            print('filter_type: ', type_filter)
            state_name = request.data.get("State")
            print('state_name: ', state_name)

            state_id = State.objects.get(state_name=state_name)
            print('state_id: ', state_id)

            first_data = 'B02001002'
            second_data = 'B19001002'
            third_data = 'B15003002'
            fourth_data = 'B17001002'

            list1 = []
            list2 = []
            list3 = []
            list4 = []
            if topic_name[0]["Race"] == first_data:
                Race_value = topic_name[0]['value']
                print('Race_value: ', Race_value)

                race_state_county = RaceEstimate.objects.exclude(race_id='B02001001').annotate(
                    percent=F('race_estimate_value')*100 / F('county__race_total')).filter(
                        county__state_id=state_id,
                        race_id=first_data)
                print('race_state_county: ', race_state_county)
                if type_filter == "Top":
                    race_state_county = race_state_county.order_by(
                        '-percent')[:count]
                    print('race_state_county------------: ', race_state_county)

                elif type_filter == "Bottom":
                    race_state_county = race_state_county.order_by(
                        'percent')[:count]
                    print('race_state_top********------------:',
                          race_state_county)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                race_state_county_list = []
                if race_state_county.exists():

                    for data in race_state_county:
                        ra_st_data = {}
                        ra_st_data['County_name'] = data.county.county_name

                        race_state_county_list.append(ra_st_data)
                        list1.append(data.county.county_name)
                        dic = {}
                        dic[data.county.county_name] = Race_value/count
                        list2.append(dic)

            else:
                return Response({"error": "Invalid Input value topic name RACE"})
            if topic_name[1]['Income'] == second_data:
                income_value = topic_name[1]['value']

                income_state_county = IncomeEstimate.objects.exclude(income_id='B19001001').annotate(
                    percent=F('income_estimate_value')*100/F('county__income_total')).filter(
                        county__state_id=state_id,
                        income_id=second_data)
                if type_filter == "Top":
                    income_state_county = income_state_county.order_by(
                        '-percent')[:count]
                    print('income_state_county: ', income_state_county)

                elif type_filter == "Bottom":
                    income_state_county = income_state_county.order_by(
                        'percent')[:count]
                    print('income_state_county:',
                          income_state_county)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                income_state_county_list = []
                if income_state_county.exists():
                    for data in income_state_county:
                        in_ct_data = {}
                        in_ct_data['County_Name'] = data.county.county_name

                        income_state_county_list.append(in_ct_data)
                        list1.append(data.county.county_name)
                        dic = {}
                        dic[data.county.county_name] = income_value/count
                        list2.append(dic)

            else:
                return Response({"error": "Invalid Input value topic name INCOME"})

            if topic_name[2]['Education'] == third_data:
                education_value = topic_name[2]['value']

                education_state_county = EducationEstimate.objects.exclude(education_id='B15003001').annotate(
                    percent=F('education_estimate_value')*100/F('county__education_total')).filter(county__state_id=state_id, education_id=third_data)
                if type_filter == "Top":
                    education_state_county = education_state_county.order_by(
                        '-percent')[:count]
                    print('education_state_county: ', education_state_county)

                elif type_filter == "Bottom":
                    education_state_county = education_state_county.order_by(
                        'percent')[:count]
                    print('education_state_county:',
                          education_state_county)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                education_state_county_list = []
                if education_state_county.exists():
                    for data in education_state_county:
                        ed_ct_data = {}
                        ed_ct_data['County_Name'] = data.county.county_name

                        education_state_county_list.append(ed_ct_data)
                        list3.append(data.county.county_name)
                        dic = {}
                        dic[data.county.county_name] = education_value/count
                        list2.append(list3)
                        list2.append(dic)

            else:
                return Response({"error": "Invalid Input value topic name EDUCATION"})

            if topic_name[3]['Poverty'] == fourth_data:
                poverty_value = topic_name[3]['value']

                poverty_state_county = PovertyEstimate.objects.exclude(poverty_id='B17001001').annotate(
                    percent=F('poverty_estimate_value')*100/F('county__poverty_total')).filter(
                        county__state_id=state_id,
                        poverty_id=fourth_data)
                if type_filter == "Top":
                    poverty_state_county = poverty_state_county.order_by(
                        '-percent')[:count]
                    print('poverty_state_county: ', poverty_state_county)

                elif type_filter == "Bottom":
                    poverty_state_county = poverty_state_county.order_by(
                        'percent')[:count]
                    print('poverty_state_county:',
                          poverty_state_county)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                poverty_state_county_list = []
                if poverty_state_county.exists():
                    for data in poverty_state_county:
                        pv_ct_data = {}
                        pv_ct_data['County_Name'] = data.county.county_name

                        poverty_state_county_list.append(pv_ct_data)
                        list4.append(data.county.county_name)
                        dic = {}
                        dic[data.county.county_name] = poverty_value/count
                        list2.append(list4)
                        list2.append(dic)
                        print('list3: ', list3)
                        print("list2****---", list2)
                        print("******list1*****", list1)

                        result = dict(functools.reduce(
                            operator.add, map(collections.Counter, list2)))
                        print('result: ', result)
                        result = sorted(
                            result.items(), key=operator.itemgetter(1), reverse=True)
                        result = result[:count]
                        result = dict(result)
                        print('result: ', result)

                return Response({"result": result})
            else:
                return Response({"error": "Invalid Input value topic name Poverty"})

        else:
            return Response({'error': 'invalid Request'})
