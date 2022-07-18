import collections
import functools
import operator


from django.db.models import F, Q

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import (
    RaceEstimate, IncomeEstimate
)

from realestate_education.models import (
    EducationEstimate
)

from realestate_poverty.models import (
    PovertyEstimate
)

from realestate_education.models import EducationEstimate

from realestate_poverty.models import PovertyEstimate

from realestate_tenure.models import TenureEstimate

from realestate_mobility.models import MobilityEstimate

from realestate_sex_age.models import SexAgeEstimate


class TopicStaticCounty(APIView):

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

                # Race
                print("--------------Race----------------")
                if topic_name_list[0] == 'Race':
                    print('topic_name_list: ', topic_name_list[0])
                    Race_value = topic_name[0]['Race']
                    print('Race_value: ', Race_value)
                    if Race_value > 0:
                        race_county_top = RaceEstimate.objects.exclude(race_id='B02001001').annotate(
                            percent=F('race_estimate_value')*100/F('county__race_total'))
                        print('race_county_top: ', race_county_top)

                        if type_filter == "Top":
                            race_county_top = race_county_top.order_by(
                                '-percent')[:count]
                            print('race_county_top------------: ',
                                  race_county_top)

                        elif type_filter == "Bottom":
                            race_county_top = race_county_top.order_by(
                                'percent')[:count]
                            print('race_county_top********------------:',
                                  race_county_top)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if race_county_top.exists():

                            for data in race_county_top:
                                dic = {}
                                dic[data.county.county_name] = Race_value/count
                                final_list.append(dic)
                            print('final_list:/----/ ', final_list)
                    else:
                        print("Race_value", Race_value)

                else:
                    return Response({"error": "Invalid Input value topic name RACE"})

                # Income
                print("--------------Income----------------")
                if topic_name_list[1] == "Income":
                    income_value = topic_name[1]['Income']
                    if income_value > 0:
                        income_county_top = IncomeEstimate.objects.exclude(income_id='B19001001').annotate(
                            percent=F('income_estimate_value')*100/F('county__income_total'))
                        print('income_county_top: ', income_county_top)

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

                        if income_county_top.exists():
                            for data in income_county_top:
                                dic = {}
                                dic[data.county.county_name] = income_value/count
                                final_list.append(dic)
                            print('final_list: ', final_list)
                    else:
                        print("income_value", income_value)

                else:
                    return Response({"error": "Invalid Input value topic name INCOME"})

                # Education
                print("--------------Education----------------")
                if topic_name_list[2] == "Education":
                    education_value = topic_name[2]['Education']
                    if education_value > 0:
                        education_county_top = EducationEstimate.objects.exclude(education_id='B15003001').annotate(
                            percent=F('education_estimate_value')*100/F('county__education_total'))
                        print('education_county_top: ', education_county_top)

                        if type_filter == "Top":
                            education_county_top = education_county_top.order_by(
                                '-percent')[:count]
                            print('education_county_top: ',
                                  education_county_top)

                        elif type_filter == "Bottom":
                            education_county_top = education_county_top.order_by(
                                'percent')[:count]
                            print('education_county_top:',
                                  education_county_top)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if education_county_top.exists():
                            for data in education_county_top:
                                dic = {}
                                dic[data.county.county_name] = education_value/count
                                final_list.append(dic)
                            print('final_list: ', final_list)
                    else:
                        print("education_value", education_value)

                else:
                    return Response({"error": "Invalid Input value topic name EDUCATION"})

                # Poverty
                print("--------------Poverty----------------")
                if topic_name_list[3] == "Poverty":
                    poverty_value = topic_name[3]['Poverty']
                    if poverty_value > 0:
                        poverty_county_top = PovertyEstimate.objects.exclude(poverty_id='B17001001').annotate(
                            percent=F('poverty_estimate_value')*100/F('county__poverty_total'))
                        print('poverty_county_top: ', poverty_county_top)

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

                        if poverty_county_top.exists():
                            for data in poverty_county_top:
                                dic = {}
                                dic[data.county.county_name] = poverty_value/count
                                final_list.append(dic)
                            print("final_list****---", final_list)
                    else:
                        print("poverty_value", poverty_value)
                else:
                    return Response({"error": "Invalid Input value topic name Poverty"})

                # Tenure
                print("--------------Tenure----------------")
                if topic_name_list[4] == "Tenure":
                    tenure_value = topic_name[4]['Tenure']
                    if tenure_value > 0:
                        tenure_county_top = TenureEstimate.objects.exclude(tenure_id='B25003001').annotate(
                            percent=F('tenure_estimate_value')*100/F('county__tenure_total'))
                        print('tenure_county_top: ', tenure_county_top)

                        if type_filter == "Top":
                            tenure_county_top = tenure_county_top.order_by(
                                '-percent')[:count]
                            print('tenure_county_top: ', tenure_county_top)

                        elif type_filter == "Bottom":
                            tenure_county_top = tenure_county_top.order_by(
                                'percent')[:count]
                            print('tenure_county_top:',
                                  tenure_county_top)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if tenure_county_top.exists():
                            for data in tenure_county_top:
                                dic = {}
                                dic[data.county.county_name] = tenure_value/count
                                final_list.append(dic)
                            print("final_list****Tenure---", final_list)
                    else:
                        print("tenure_value", tenure_value)
                else:
                    return Response({"error": "Invalid Input value topic name Tenure"})

                # Mobility
                print("--------------Mobility----------------")
                if topic_name_list[5] == "Mobility":
                    mobility_value = topic_name[5]['Mobility']
                    if mobility_value > 0:
                        mobility_county_top = MobilityEstimate.objects.exclude(mobility_id='B07003001').annotate(
                            percent=F('mobility_estimate_value')*100/F('county__mobility_total'))
                        print('mobility_county_top: ', mobility_county_top)

                        if type_filter == "Top":
                            mobility_county_top = mobility_county_top.order_by(
                                '-percent')[:count]
                            print('mobility_county_top: ', mobility_county_top)

                        elif type_filter == "Bottom":
                            mobility_county_top = mobility_county_top.order_by(
                                'percent')[:count]
                            print('mobility_county_top:',
                                  mobility_county_top)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if mobility_county_top.exists():
                            for data in mobility_county_top:
                                dic = {}
                                dic[data.county.county_name] = mobility_value/count
                                final_list.append(dic)
                            print("final_list****Mobility---", final_list)
                    else:
                        print("mobility_value", mobility_value)
                else:
                    return Response({"error": "Invalid Input value topic name Mobility"})

                # Age
                print("--------------Age----------------")
                if topic_name_list[6] == "Age":
                    sex_age_value = topic_name[6]['Age']
                    print('sex_age_value: ', sex_age_value)

                    if sex_age_value > 0:
                        sex_age_county_top = SexAgeEstimate.objects.exclude(
                            Q(sex_age_id='B01001001') |
                            Q(sex_age_id='B01001002') |
                            Q(sex_age_id='B01001026')).annotate(
                            percent=F('sex_age_estimate_value')*100/F('county__sex_age_total'))
                        print('sex_age_county_top: ', sex_age_county_top)

                        if type_filter == "Top":
                            sex_age_county_top = sex_age_county_top.order_by(
                                '-percent')[:count]
                            print('sex_age_county_top: ', sex_age_county_top)

                        elif type_filter == "Bottom":
                            sex_age_county_top = sex_age_county_top.order_by(
                                'percent')[:count]
                            print('sex_age_county_top:',
                                  sex_age_county_top)

                        else:
                            return Response({'error': 'Invalid Filter Type'})

                        if sex_age_county_top.exists():
                            for data in sex_age_county_top:
                                dic = {}
                                dic[data.county.county_name] = sex_age_value/count
                                final_list.append(dic)
                            print("final_list****Mobility---", final_list)
                    else:
                        print("sex_age_value", sex_age_value)
                else:
                    return Response({"error": "Invalid Input value topic name age"})

                if final_list:
                    result = dict(functools.reduce(
                        operator.add, map(collections.Counter, final_list)))
                    print('result: ', result)
                    result = sorted(
                        result.items(), key=operator.itemgetter(1), reverse=True)
                    result = result[:count]
                    result = dict(result)
                    print('{{{{{-----Result----}}}}}}}', result)

                    return Response({"result": result})

                else:
                    return Response({'error': 'Select at leat one topic'})

            else:
                return Response({'error': 'invalid request'})
        except Exception as e:
            return Response({'Error': f'{e}'})
