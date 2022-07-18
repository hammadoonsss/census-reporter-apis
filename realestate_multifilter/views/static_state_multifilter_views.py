import collections
import functools
import operator

from django.db.models import F, Q

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import (
    County, State,
    RaceEstimate, RaceStateTotal, IncomeEstimate, IncomeStateTotal
)

from realestate_education.models import EducationStateTotal

from realestate_poverty.models import PovertyStateTotal

from realestate_tenure.models import TenureStateTotal

from realestate_mobility.models import MobilityStateTotal

from realestate_sex_age.models import SexAgeStateTotal


class TopicStaticState(APIView):

    def post(self, request):

        try:

            if request.data:
                topic_name = request.data.get('Topic_Name')
                print('topic_name: ', topic_name)
                count = request.data.get('Count')
                print('count: ', count)
                type_filter = request.data.get('Type')
                print('type_filter: ', type_filter)

                topic_name_list = []
                list_length = len(topic_name)
                print('list_length:--->>>>>', list_length)

                for i in range(list_length):
                    a = list(topic_name[i].keys())[0]
                    topic_name_list.append(a)
                print('topic_name_list:<<<<<<<------ ', topic_name_list)

                final_list = []

                # For Race
                print("--------------Race----------------")
                if topic_name_list[0] == "Race":
                    race_value = topic_name[0]['Race']
                    print('Race_value: ', race_value)
                    if race_value > 0:
                        race_state_top = RaceStateTotal.objects.exclude(race_id='B02001001').annotate(
                            percent=F('race_total')*100/F('state_total'))

                        if type_filter == "Top":
                            race_state_top = race_state_top.order_by(
                                '-percent')[:count]

                        elif type_filter == "Bottom":
                            race_state_top = race_state_top.order_by(
                                'percent')[:count]

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if race_state_top.exists():

                            for data in race_state_top:
                                ra_st_data = {}
                                ra_st_data[data.state.state_name] = int(
                                    race_value)/count
                                final_list.append(ra_st_data)
                            print('final_list:: Race ', final_list)

                        else:
                            return Response({"error": "Invalid Input value topic name RACE"})
                    else:
                        print("race_value", race_value)
                else:
                    print("invalid name:Race")
                    return Response({"Error": "Invalid Topic name"})

                # Income
                print("--------------Income----------------")
                if topic_name_list[1] == "Income":
                    income_value = topic_name[1]['Income']
                    print('income_value: ', income_value)
                    if income_value > 0:
                        income_state_top = IncomeStateTotal.objects.exclude(income_id='B19001001').annotate(
                            percent=F('income_total')*100/F('state_total'))

                        if type_filter == "Top":
                            income_state_top = income_state_top.order_by(
                                '-percent')[:count]
                        elif type_filter == "Bottom":
                            income_state_top = income_state_top.order_by(
                                'percent')[:count]
                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if income_state_top.exists():

                            for data in income_state_top:
                                in_st_data = {}
                                in_st_data[data.state.state_name] = int(
                                    income_value)/count

                                final_list.append(in_st_data)
                            print('final_list:: Income:', final_list)

                        else:
                            return Response({"error": "Invalid Input value topic name Income"})
                    else:
                        print("Income_value", income_value)
                else:
                    print("invalid name: Income")
                    return Response({"Error": "Invalid Topic name"})

                # Education
                print("--------------Education----------------")
                if topic_name_list[2] == "Education":
                    education_value = topic_name[2]['Education']
                    print('education_value: ', education_value)
                    if education_value > 0:
                        education_state_top = EducationStateTotal.objects.exclude(education_id='B15003001').annotate(
                            percent=F('education_total')*100/F('state_total'))

                        if type_filter == "Top":
                            education_state_top = education_state_top.order_by(
                                '-percent')[:count]
                        elif type_filter == "Bottom":
                            education_state_top = education_state_top.order_by(
                                'percent')[:count]
                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if education_state_top.exists():
                            for data in education_state_top:
                                ed_st_data = {}
                                ed_st_data[data.state.state_name] = int(
                                    education_value)/count

                                final_list.append(ed_st_data)
                            print('final_list:: Education: ', final_list)

                        else:
                            return Response({'error': "Invalid input value topic name Education"})
                    else:
                        print("Education_value", education_value)
                else:
                    print("invalid name:Education")
                    return Response({"Error": "Invalid Topic name"})

                # Poverty
                print("--------------Poverty----------------")
                if topic_name_list[3] == "Poverty":
                    poverty_value = topic_name[3]['Poverty']
                    if poverty_value > 0:
                        poverty_state_top = PovertyStateTotal.objects.exclude(poverty_id='B17001001').annotate(
                            percent=F('poverty_total')*100/F('state_total'))

                        if type_filter == "Top":
                            poverty_state_top = poverty_state_top.order_by(
                                '-percent')[:count]
                        elif type_filter == "Bottom":
                            poverty_state_top = poverty_state_top.order_by(
                                'percent')[:count]
                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if poverty_state_top.exists():
                            for data in poverty_state_top:
                                pv_st_data = {}
                                pv_st_data[data.state.state_name] = int(
                                    poverty_value)/count

                                final_list.append(pv_st_data)
                            print('final_list:: Poverty: ', final_list)

                        else:
                            return Response({'error': "Invalid input value topic name Poverty"})
                    else:
                        print("Poverty_value", poverty_value)
                else:
                    print("invalid name:Poverty")
                    return Response({"Error": "Invalid Topic name"})

                # Tenure
                print("--------------Tenure----------------")
                if topic_name_list[4] == "Tenure":
                    tenure_value = topic_name[4]['Tenure']
                    print('tenure_value: ', tenure_value)
                    if tenure_value > 0:
                        tenure_state_top = TenureStateTotal.objects.exclude(tenure_id='B25003001').annotate(
                            percent=F('tenure_total')*100/F('state_total'))

                        if type_filter == "Top":
                            tenure_state_top = tenure_state_top.order_by(
                                '-percent')[:count]
                        elif type_filter == "Bottom":
                            tenure_state_top = tenure_state_top.order_by(
                                'percent')[:count]
                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if tenure_state_top.exists():
                            for data in tenure_state_top:
                                tn_st_data = {}
                                tn_st_data[data.state.state_name] = int(
                                    tenure_value)/count

                                final_list.append(tn_st_data)
                            print('final_list:: Tenure: ', final_list)

                        else:
                            return Response({'error': "Invalid input value topic name Tenure"})
                    else:
                        print("Tenure_value", tenure_value)
                else:
                    print("invalid name: Tenure")
                    return Response({"Error": "Invalid Topic name"})

                # Mobility
                print("--------------Mobility----------------")
                if topic_name_list[5] == "Mobility":
                    mobility_value = topic_name[5]['Mobility']
                    print('mobility_value: ', mobility_value)
                    if mobility_value > 0:
                        mobility_state_top = MobilityStateTotal.objects.exclude(mobility_id='B07003001').annotate(
                            percent=F('mobility_total')*100/F('state_total'))

                        if type_filter == "Top":
                            mobility_state_top = mobility_state_top.order_by(
                                '-percent')[:count]

                        elif type_filter == "Bottom":
                            mobility_state_top = mobility_state_top.order_by(
                                'percent')[:count]

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if mobility_state_top.exists():
                            for data in mobility_state_top:
                                mb_st_data = {}
                                mb_st_data[data.state.state_name] = int(
                                    mobility_value)/count

                                final_list.append(mb_st_data)
                            print('final_list:: Mobility: ', final_list)

                        else:
                            return Response({'error': "Invalid input value topic name Mobility"})
                    else:
                        print("Mobility_Value", mobility_value)
                else:
                    print("invalid name: Mobility")
                    return Response({"Error": "Invalid Topic name"})

                # Age
                print("--------------Age----------------")
                if topic_name_list[6] == "Age":
                    age_value = topic_name[6]['Age']
                    print('age_value: ', age_value)
                    if age_value > 0:
                        age_state_top = SexAgeStateTotal.objects.exclude(
                            Q(sex_age_id='B01001001') |
                            Q(sex_age_id='B01001002') |
                            Q(sex_age_id='B01001026')
                        ).annotate(percent=F('sex_age_total')*100/F('state_total'))

                        if type_filter == "Top":
                            age_state_top = age_state_top.order_by(
                                '-percent')[:count]

                        elif type_filter == "Bottom":
                            age_state_top = age_state_top.order_by(
                                'percent')[:count]

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if age_state_top.exists():
                            for data in age_state_top:
                                sex_age_st_data = {}
                                sex_age_st_data[data.state.state_name] = int(
                                    age_value)/count

                                final_list.append(sex_age_st_data)
                            print('final_list:: Age: ', final_list)

                        else:
                            return Response({'error': "Invalid input value topic name Age"})
                    else:
                        print("Age_Value", age_value)
                else:
                    print("inside else not working..")
                    return Response({"Error": "Invalid Topic name"})

                if final_list:

                    all_final_list = dict(functools.reduce(
                        operator.add, map(collections.Counter, final_list)))
                    print('all_final_list: --->>>> ', all_final_list)

                    all_sorted_result = sorted(
                        all_final_list.items(), key=operator.itemgetter(1), reverse=True)
                    all_sorted_result = all_sorted_result[:count]
                    print('all_sorted_result:---->>>>>>>>> ', all_sorted_result)

                    all_final_dict = dict(all_sorted_result)
                    print('all_final_dict:=======> ', all_final_dict)

                    return Response({'Result': all_final_dict})

                else:
                    return Response({'error': 'Select at-least one Topic'})

            else:
                return Response({'error': "Invalid Request"})

        except Exception as e:
            return Response({'Error': f'{e}'})
