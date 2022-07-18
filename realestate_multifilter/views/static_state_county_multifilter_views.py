import collections
import functools
import operator


from django.db.models import F, Q

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import (
    Race, State, RaceEstimate, Income, IncomeEstimate
)

from realestate_education.models import (
    Education, EducationEstimate
)

from realestate_poverty.models import (
    Poverty, PovertyEstimate
)

from realestate_tenure.models import (
    Tenure, TenureEstimate
)

from realestate_mobility.models import (
    Mobility, MobilityEstimate
)

from realestate_sex_age.models import (
    SexAge, SexAgeEstimate
)


class TopicStaticStateCounty(APIView):

    def post(self, request):

        try:

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

                topic_name_list = []
                list_length = len(topic_name)
                print('list_length:--->>>>>', list_length)

                for i in range(list_length):
                    a = list(topic_name[i].keys())[0]
                    topic_name_list.append(a)
                print('topic_name_list:<<<<<<<------ ', topic_name_list)

                final_list = []

                # Race
                print("--------------Race----------------")
                if topic_name_list[0] == "Race":
                    race_value = topic_name[0]['Race']
                    print('race_value: ', race_value)

                    if race_value > 0:

                        race_state_county = RaceEstimate.objects.exclude(race_id='B02001001').annotate(
                            percent=F('race_estimate_value')*100 / F('county__race_total')).filter(
                            county__state_id=state_id)
                        print('race_state_county: ', race_state_county)

                        if type_filter == "Top":
                            race_state_county = race_state_county.order_by(
                                '-percent')[:count]
                            print('race_state_county------------: ',
                                  race_state_county)

                        elif type_filter == "Bottom":
                            race_state_county = race_state_county.order_by(
                                'percent')[:count]
                            print('race_state_county********------------:',
                                  race_state_county)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if race_state_county.exists():

                            for data in race_state_county:
                                dic = {}
                                dic[data.county.county_name] = race_value/count
                                final_list.append(dic)
                            print('final_list:/----/ ', final_list)

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

                        income_state_county = IncomeEstimate.objects.exclude(income_id='B19001001').annotate(
                            percent=F('income_estimate_value')*100 / F('county__income_total')).filter(
                            county__state_id=state_id)
                        print('income_state_county: ', income_state_county)

                        if type_filter == "Top":
                            income_state_county = income_state_county.order_by(
                                '-percent')[:count]
                            print('income_state_county------------: ',
                                  income_state_county)

                        elif type_filter == "Bottom":
                            income_state_county = income_state_county.order_by(
                                'percent')[:count]
                            print('income_state_county*****------:',
                                  income_state_county)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if income_state_county.exists():

                            for data in income_state_county:
                                dic = {}
                                dic[data.county.county_name] = income_value/count
                                final_list.append(dic)
                            print('final_list:/----/ ', final_list)

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

                        education_state_county = EducationEstimate.objects.exclude(education_id='B15003001').annotate(
                            percent=F('education_estimate_value')*100 / F('county__education_total')).filter(
                            county__state_id=state_id)
                        print('education_state_county: ',
                              education_state_county)

                        if type_filter == "Top":
                            education_state_county = education_state_county.order_by(
                                '-percent')[:count]
                            print('education_state_county------------: ',
                                  education_state_county)

                        elif type_filter == "Bottom":
                            education_state_county = education_state_county.order_by(
                                'percent')[:count]
                            print('income_state_county********------------:',
                                  education_state_county)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if education_state_county.exists():

                            for data in education_state_county:
                                dic = {}
                                dic[data.county.county_name] = education_value/count
                                final_list.append(dic)
                            print('final_list:/----/ ', final_list)

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
                    print('poverty_value: ', poverty_value)

                    if poverty_value > 0:

                        poverty_state_county = PovertyEstimate.objects.exclude(poverty_id='B17001001').annotate(
                            percent=F('poverty_estimate_value')*100 / F('county__poverty_total')).filter(
                            county__state_id=state_id)
                        print('poverty_state_county: ', poverty_state_county)

                        if type_filter == "Top":
                            poverty_state_county = poverty_state_county.order_by(
                                '-percent')[:count]
                            print('poverty_state_county------------: ',
                                  poverty_state_county)

                        elif type_filter == "Bottom":
                            poverty_state_county = poverty_state_county.order_by(
                                'percent')[:count]
                            print('poverty_state_county********------------:',
                                  poverty_state_county)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if poverty_state_county.exists():

                            for data in poverty_state_county:
                                dic = {}
                                dic[data.county.county_name] = poverty_value/count
                                final_list.append(dic)
                            print('final_list:/----/ ', final_list)

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

                        tenure_state_county = TenureEstimate.objects.exclude(tenure_id='B25003001').annotate(
                            percent=F('tenure_estimate_value')*100 / F('county__tenure_total')).filter(
                            county__state_id=state_id)
                        print('tenure_state_county: ', tenure_state_county)

                        if type_filter == "Top":
                            tenure_state_county = tenure_state_county.order_by(
                                '-percent')[:count]
                            print('tenure_state_county------------: ',
                                  tenure_state_county)

                        elif type_filter == "Bottom":
                            tenure_state_county = tenure_state_county.order_by(
                                'percent')[:count]
                            print('tenure_state_county********------------:',
                                  tenure_state_county)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if tenure_state_county.exists():

                            for data in tenure_state_county:
                                dic = {}
                                dic[data.county.county_name] = tenure_value/count
                                final_list.append(dic)
                            print('final_list:/----/ ', final_list)

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

                        mobility_state_county = MobilityEstimate.objects.exclude(mobility_id='B07003001').annotate(
                            percent=F('mobility_estimate_value')*100 / F('county__mobility_total')).filter(
                            county__state_id=state_id)
                        print('mobility_state_county: ', mobility_state_county)

                        if type_filter == "Top":
                            mobility_state_county = mobility_state_county.order_by(
                                '-percent')[:count]
                            print('mobility_state_county------------: ',
                                  mobility_state_county)

                        elif type_filter == "Bottom":
                            mobility_state_county = mobility_state_county.order_by(
                                'percent')[:count]
                            print('mobility_state_county********------------:',
                                  mobility_state_county)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if mobility_state_county.exists():

                            for data in mobility_state_county:
                                dic = {}
                                dic[data.county.county_name] = mobility_value/count
                                final_list.append(dic)
                            print('final_list:/----/ ', final_list)

                        else:
                            return Response({'error': "Invalid input value topic name Mobility"})
                    else:
                        print("Mobility_Value", mobility_value)
                else:
                    return Response({"Error": "Invalid Topic name"})

                # Age
                print("--------------Age----------------")
                if topic_name_list[6] == "Age":
                    age_value = topic_name[6]['Age']
                    print('age_value: ', age_value)

                    if age_value > 0:

                        age_state_county = SexAgeEstimate.objects.exclude(
                            Q(sex_age_id='B01001001') |
                            Q(sex_age_id='B01001002') |
                            Q(sex_age_id='B01001026')).annotate(
                            percent=F('sex_age_estimate_value')*100 / F('county__sex_age_total')).filter(
                            county__state_id=state_id)
                        print('age_state_county: ', age_state_county)

                        if type_filter == "Top":
                            age_state_county = age_state_county.order_by(
                                '-percent')[:count]
                            print('age_state_county------------: ',
                                  age_state_county)

                        elif type_filter == "Bottom":
                            age_state_county = age_state_county.order_by(
                                'percent')[:count]
                            print('age_state_county********------------:',
                                  age_state_county)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if age_state_county.exists():

                            for data in age_state_county:
                                dic = {}
                                dic[data.county.county_name] = age_value/count
                                final_list.append(dic)
                            print('final_list:/----/ ', final_list)
                        else:
                            return Response({'error': "Invalid input value topic name Age"})
                    else:
                        print("age_value", age_value)
                else:
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
                    return Response({'error': 'Select at leat one topic'})
            else:
                return Response({'error': 'invalid request'})
        except Exception as e:
            return Response({'Error': f'{e}'})
