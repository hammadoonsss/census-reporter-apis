import collections
import functools
import operator

from django.db.models import F

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import(
    State,
    Race, RaceEstimate,
    Income, IncomeEstimate,
)

from realestate_app.utils import check_similar_value

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

from realestate_app.services import TotalPercentage

from realestate_multifilter.config import (
    race_id_dict,
    income_id_dict,
    education_id_dict,
    poverty_id_dict,
    tenure_id_dict,
    mobility_id_dict,
    age_id_dict,
)

# -------------- State/Counties - MultiFilter - Second Flow -------------


class StateCountiesMultiFilter(APIView):

    def post(self, request):
        try:
            if request.data:

                topic_name = request.data.get('Topic_Name')
                print('topic_name: ', topic_name)
                state = request.data.get('State')
                print('state: ', state)
                count = request.data.get('Count')
                print('count: ', count)
                filter_type = request.data.get('Type')
                print('type_filter: ', filter_type)

                # For State_ID
                try:
                    state_id = State.objects.get(state_name=state)
                    print('state_id: ', state_id)
                except:
                    print(
                        "Error: Given Value is Invalid :: State", state)
                    return Response({'error': f"State :: Given Value is Invalid :: {state}"})

                # For Topic_Name_List
                topic_name_list = []
                list_length = len(topic_name)
                print('list_length:======= ', list_length)

                for i in range(list_length):
                    a = list(topic_name[i].keys())[0]
                    topic_name_list.append(a)
                print('topic_name_list:----------- ', topic_name_list)

                all_combine_list = []

                # For Race
                if topic_name_list[0] == "Race":
                    print("________Race_________")

                    race_total_list = []

                    race_data = topic_name[0]['Race']
                    print('race_data: ', race_data)

                    race_value = topic_name[0]['value']
                    print('race_value: ', race_value)

                    topic = 'race'

                    if race_value > 0:
                        print('race_value: in IF--', race_value)

                        for data in race_data:
                            print('data: ', data)

                            lis1 = list(data.items())
                            print('lis1: ', lis1)

                            sub_r_value = lis1[1][1]
                            print('sub_r_value: ', sub_r_value)

                            s_r_id = lis1[0][1]
                            print('s_r_id: ', s_r_id)

                            try:
                                sub_r_id = race_id_dict[s_r_id]
                                print('sub_r_id: ', sub_r_id)
                            except:
                                print(
                                    "Error: Given Value is Invalid :: Race", s_r_id)
                                return Response({'error': f"Race :: Given Value is Invalid :: {s_r_id}"})

                            try:
                                r_id = Race.objects.get(race_id=sub_r_id)
                                print('r_id: ', r_id)
                            except:
                                print(
                                    "Error: Invalid ID :: Race", sub_r_id)
                                return Response({'error': f"Race :: Invalid ID :: {sub_r_id}"})

                            race_id = r_id.race_id
                            print('race_id: ', race_id)

                            race_counties, error = TotalPercentage.state_top_counties_data(
                                RaceEstimate, topic, race_id, state_id, count, filter_type
                            )

                            print('race_counties: ', race_counties)
                            print('error: ', error)

                            if error is not None:
                                print("Inside error----")
                                return Response({'error': error})

                            if race_counties.exists():

                                for data in race_counties:
                                    print("------------",
                                          data.county.county_name)
                                    dic = {}
                                    dic[data.county.county_name] = sub_r_value/count
                                    race_total_list.append(dic)
                                print(
                                    'list: race_total_list: Race:---->>> ', race_total_list)

                            else:
                                print(
                                    "Error: No Data Avaliable in Topic_Name :: Race")
                                return Response({'error': 'No Data Avaliable in Topic_Name :: Race'})

                        race_result_list = dict(functools.reduce(operator.add,
                                                                 map(collections.Counter, race_total_list)))
                        print('race_result_list: --------', race_result_list)
                        race_sorted_result = sorted(
                            race_result_list.items(), key=operator.itemgetter(1), reverse=True)
                        race_sorted_result = race_sorted_result[:count]
                        print('race_sorted_result: ', race_sorted_result)

                        race_final_dict = dict(race_sorted_result)
                        print('race_final_dict: >>>>>>>>>>>.', race_final_dict)

                        for ele in race_final_dict:
                            race_final_dict.update({ele: race_value})
                        print('race_final_dict:------------->> ', race_final_dict)

                        all_combine_list.append(race_final_dict)

                    else:
                        print('In Else :: Race Data: ', race_data)
                        print('In Else :: Race Value: ', race_value)

                    # return Response({"result": "Top Counties Multi Filter"})

                else:
                    print("[[[[[[[[[[[[--Not Working::Race--]]]]]]]]]]]]]")
                    return Response({'error': 'Invalid Topic Name'})

                # For Income
                if topic_name_list[1] == "Income":
                    print("________Income_________")

                    income_total_list = []
                    income_id_list = []
                    income_combine_list = []

                    topic = 'income'

                    income_data = topic_name[1]['Income']
                    print('income_data:-->>>> ', income_data)

                    income_value = topic_name[1]['value']
                    print('income_value: ', income_value)

                    if income_value > 0:

                        if len(income_data) > 0:

                            for data in income_data:
                                print("data-------------", data)

                                try:
                                    sub_i_list = income_id_dict[data]
                                    print('sub_i_list: ', sub_i_list)
                                    income_combine_list.extend(sub_i_list)
                                    print('income_combine_list: ',
                                          income_combine_list)
                                except:
                                    print(
                                        "Error: Given Value is Invalid :: Income", data)
                                    return Response({'error': f"Income :: Given Value is Invalid :: {data}"})

                            for id in income_combine_list:

                                try:
                                    inc_id = Income.objects.get(income_id=id)
                                    print('inc_id: >>>>>>>>>>>>',
                                          inc_id.income_id)
                                    income_id_list.append(inc_id.income_id)
                                except:
                                    print(
                                        "Error: Invalid ID :: Income", id)
                                    return Response({'error': f"Income :: Invalid ID :: {id}"})
                            print('income_id_list: ', income_id_list)

                        else:
                            print("No Value -------------")
                            return Response({'error': 'No Income ID'})

                        for data in income_id_list:
                            print("data------->", data)

                            inc_state, error = TotalPercentage.state_top_counties_data(
                                IncomeEstimate, topic, data, state_id, count, filter_type
                            )

                            print('inc_state: ', inc_state)
                            print('error: ', error)

                            if error is not None:
                                print("error", error)
                                return Response({"error": f'{error}'})

                            if inc_state.exists():
                                for data in inc_state:
                                    print("------------",
                                          data.county.county_name)
                                    dic = {}
                                    dic[data.county.county_name] = income_value/count

                                    income_total_list.append(dic)
                                print('income_total_list: ---->>',
                                      income_total_list)

                            else:
                                print(
                                    "Error: No Data Avaliable in Topic_Name: Income")
                                return Response({'error': 'No Data Avaliable in Topic_Name :: Income'})

                        inc_result_list = dict(functools.reduce(
                            operator.add, map(collections.Counter, income_total_list)))
                        print('inc_result_list:======>>> ', inc_result_list)

                        inc_sorted_result = sorted(
                            inc_result_list.items(), key=operator.itemgetter(1), reverse=True)
                        inc_sorted_result = inc_sorted_result[:count]

                        inc_final_dict = dict(inc_sorted_result)
                        print('inc_final_dict: ', inc_final_dict)

                        for ele in inc_final_dict:
                            inc_final_dict.update({ele: income_value})
                        print('inc_final_dict:------------->> ', inc_final_dict)

                        all_combine_list.append(inc_final_dict)

                    else:
                        print("In Else :: Income Data", income_data)
                        print("In Else :: Income Value", income_value)

                else:
                    print("[[[[[[[[[[[[--Not Working::Income--]]]]]]]]]]]]]")
                    return Response({'error': 'Invalid Topic Name'})

                # For Education
                if topic_name_list[2] == "Education":
                    print("________Education_________")

                    edu_total_list = []

                    edu_data = topic_name[2]['Education']
                    print('edu_data: ', edu_data)

                    edu_value = topic_name[2]['value']
                    print('edu_value: ', edu_value)

                    topic = 'education'

                    if edu_value > 0:

                        try:
                            sub_e_id = education_id_dict[edu_data]
                            print('sub_e_id: ', sub_e_id)
                        except:
                            print(
                                "Error: Given Value is Invalid :: Education", edu_data)
                            return Response({'error': f"Education :: Given Value is Invalid :: {edu_data}"})

                        try:
                            e_id = Education.objects.get(education_id=sub_e_id)
                            print('edu_id: ------', type(e_id))
                        except:
                            print(
                                "Error: Invalid ID :: Education", sub_e_id)
                            return Response({'error': f"Education :: Invalid ID :: {sub_e_id}"})

                        edu_id = e_id.education_id
                        print('edu_id: ', type(edu_id))
                        print('edu_id: ', edu_id)

                        edu_state, error = TotalPercentage.state_top_counties_data(
                            EducationEstimate, topic, edu_id, state_id, count, filter_type
                        )

                        print('edu_state: ', edu_state)
                        print('error: ', error)

                        if error is not None:
                            print("error", error)
                            return Response({"error": f'{error}'})

                        if edu_state.exists():
                            for data in edu_state:
                                print("-----------", data.county.county_name)
                                dic = {}
                                dic[data.county.county_name] = edu_value/count
                                edu_total_list.append(dic)

                            print('edu_total_list: ', edu_total_list)

                            edu_result_list = dict(functools.reduce(
                                operator.add, map(collections.Counter, edu_total_list)))
                            print('edu_result_list: ', edu_result_list)

                            for ele in edu_result_list:
                                edu_result_list.update({ele: edu_value})
                            print('edu_result_list:------------->> ',
                                  edu_result_list)

                            all_combine_list.append(edu_result_list)

                        else:
                            print(
                                "Error: No Data Avaliable in Topic_Name: Education")
                            return Response({"error": "No Data Avaliable in Topic_Name: Education"})

                    else:
                        print("In Else :: Edu Data", edu_data)
                        print("In Else :: Edu Value: ", edu_value)

                else:
                    print("[[[[[[[[[[[[--Not Working::Education--]]]]]]]]]]]]]")
                    return Response({'error': 'Invalid Topic Name'})

                # For Poverty
                if topic_name_list[3] == "Poverty":
                    print("________Poverty_________")

                    pov_total_list = []

                    pov_data = topic_name[3]['Poverty']
                    print('pov_data: ', pov_data)

                    pov_value = topic_name[3]['value']
                    print('pov_value: ', pov_value)

                    topic = 'poverty'

                    if pov_value > 0:

                        try:
                            sub_p_id = poverty_id_dict[pov_data]
                            print('sub_p_id: ', sub_p_id)
                        except:
                            print(
                                "Error: Given Value is Invalid :: Poverty", pov_data)
                            return Response({'error': f"Poverty :: Given Value is Invalid :: {pov_data}"})

                        try:
                            p_id = Poverty.objects.get(poverty_id=sub_p_id)
                            print('p_id: ', p_id)
                        except:
                            print(
                                "Error: Invalid ID :: Poverty", sub_p_id)
                            return Response({'error': f"Poverty :: Invalid ID :: {sub_p_id}"})

                        pov_id = p_id.poverty_id
                        print('pov_id: ', type(pov_id))
                        print('pov_id: ', pov_id)

                        pov_state, error = TotalPercentage.state_top_counties_data(
                            PovertyEstimate, topic, pov_id, state_id, count, filter_type
                        )
                        print('pov_state: ', pov_state)
                        print('error: ', error)

                        if error is not None:
                            print("Error", error)
                            return Response({"error", f'{error}'})

                        if pov_state.exists():

                            for data in pov_state:
                                print("-----------", data.county.county_name)
                                dic = {}
                                dic[data.county.county_name] = pov_value/count
                                pov_total_list.append(dic)

                            print('pov_total_list: ', pov_total_list)

                        else:
                            print("Error:No Data Avaliable in Topic_Name: Poverty")
                            return Response({'error': 'No Data Avaliable in Topic_Name: Poverty'})

                        pov_result_list = dict(functools.reduce(
                            operator.add, map(collections.Counter, pov_total_list)))
                        print('pov_result_list: ', pov_result_list)

                        for ele in pov_result_list:
                            pov_result_list.update({ele: pov_value})
                        print('pov_result_list:------------->> ', pov_result_list)

                        all_combine_list.append(pov_result_list)

                    else:
                        print('In Else :: Pov Data: ', pov_data)
                        print('In Else :: Pov Value: ', pov_value)

                else:
                    print("[[[[[[[[[[[[--Not Working::Poverty--]]]]]]]]]]]]]")
                    return Response({'error': 'Invalid Topic Name'})

                #  For Tenure
                if topic_name_list[4] == "Tenure":
                    print("________Tenure_________")

                    ten_total_list = []

                    ten_data = topic_name[4]['Tenure']
                    print('ten_data: ', ten_data)

                    ten_value = topic_name[4]['value']
                    print('ten_value: ', ten_value)

                    topic = 'tenure'

                    if ten_value > 0:

                        for data in ten_data:
                            print('data: ', data)
                            print('data:------- ', type(data.items()))
                            print('data List:------- ', list(data.items()))
                            lis1 = list(data.items())
                            print('lis1: ---------', lis1)

                            sub_t_value = lis1[1][1]
                            print('sub_t_value: ', sub_t_value)

                            s_t_id = lis1[0][1]
                            print('s_t_id: ', s_t_id)

                            try:
                                sub_t_id = tenure_id_dict[s_t_id]
                                print('sub_t_id: ', sub_t_id)
                            except:
                                print(
                                    "Error: Given Value is Invalid :: Tenure", s_t_id)
                                return Response({'error': f"Tenure :: Given Value is Invalid :: {s_t_id}"})

                            try:
                                t_id = Tenure.objects.get(tenure_id=sub_t_id)
                                print('t_id: ', t_id)
                            except:
                                print(
                                    "Error: Invalid ID :: Tenure", sub_t_id)
                                return Response({'error': f"Tenure :: Invalid ID :: {sub_t_id}"})

                            tenure_id = t_id.tenure_id
                            print('tenure_id: ', tenure_id)

                            ten_state, error = TotalPercentage.state_top_counties_data(
                                TenureEstimate, topic, tenure_id, state_id, count, filter_type)
                            print('ten_state: ', ten_state)
                            print('error: ', error)

                            if error is not None:
                                print("Inside error----")
                                return Response({'error': error})

                            if ten_state.exists():

                                for data in ten_state:
                                    print("-----------",
                                          data.county.county_name)
                                    dic = {}
                                    # print('sub_r_value/count: ', sub_t_value)
                                    dic[data.county.county_name] = sub_t_value/count
                                    ten_total_list.append(dic)
                                print(
                                    'list: ten_total_list: Tenure:-->>> ', ten_total_list)
                            else:
                                print("Error: ")
                                return Response({'error': 'No Data Avaliable in Topic_Name: Tenure'})

                        tenure_result_list = dict(functools.reduce(operator.add,
                                                                   map(collections.Counter, ten_total_list)))
                        print('tenure_result_list:-------- ', tenure_result_list)

                        ten_sorted_result = sorted(
                            tenure_result_list.items(), key=operator.itemgetter(1), reverse=True)
                        ten_sorted_result = ten_sorted_result[:count]
                        print('ten_sorted_result: ', ten_sorted_result)

                        ten_final_dict = dict(ten_sorted_result)
                        print('ten_final_dict: ', ten_final_dict)

                        for ele in ten_final_dict:
                            ten_final_dict.update({ele: ten_value})
                        print('ten_final_dict:------------->> ', ten_final_dict)

                        all_combine_list.append(ten_final_dict)

                    else:
                        print('In Else :: Ten Data: ', ten_data)
                        print('In Else :: Ten Value: ', ten_value)

                else:
                    print("[[[[[[[[[[[[--Not Working::Tenure--]]]]]]]]]]]]]")
                    return Response({'error': 'Invalid Topic Name'})

                # For Mobility
                if topic_name_list[5] == "Mobility":
                    print("________Mobility_________")

                    mob_total_list = []

                    mob_data = topic_name[5]['Mobility']
                    print('mob_data: ', mob_data)

                    mob_value = topic_name[5]['value']
                    print('mob_value: ', mob_value)

                    topic = 'mobility'

                    if mob_value > 0:

                        try:
                            sub_m_id = mobility_id_dict[mob_data]
                            print('sub_m_id: ', sub_m_id)

                        except:
                            print(
                                "Error: Given Value is Invalid :: Mobility", mob_data)
                            return Response({'error': f"Mobility :: Given Value is Invalid :: {mob_data}"})

                        try:
                            m_id = Mobility.objects.get(mobility_id=sub_m_id)
                            print('m_id: ', m_id)
                        except:
                            print(
                                "Error: Invalid ID :: Mobility", sub_m_id)
                            return Response({'error': f"Mobility :: Invalid ID :: {sub_m_id}"})

                        mob_id = m_id.mobility_id
                        print('mob_id: ', type(mob_id))
                        print('mob_id: ', mob_id)

                        mob_state, error = TotalPercentage.state_top_counties_data(
                            MobilityEstimate, topic, mob_id, state_id, count, filter_type
                        )

                        print('mob_state: ', mob_state)
                        print('error: ', error)

                        if error is not None:
                            print("error", error)
                            return Response({"error": f'{error}'})

                        if mob_state.exists():
                            for data in mob_state:
                                print("-----------",
                                      data.county.county_name)
                                dic = {}
                                dic[data.county.county_name] = mob_value/count
                                mob_total_list.append(dic)

                            print('mob_total_list: ', mob_total_list)

                        else:
                            print("Error: No Data Avaliable in Topic_Name: Mobility")
                            return Response({"error": "No Data Avaliable in Topic_Name: Mobility"})

                        mob_result_list = dict(functools.reduce(
                            operator.add, map(collections.Counter, mob_total_list)))
                        print('mob_result_list: ', mob_result_list)

                        for ele in mob_result_list:
                            mob_result_list.update({ele: mob_value})
                        print('mob_result_list:------------->> ', mob_result_list)

                        all_combine_list.append(mob_result_list)

                    else:
                        print('In Else :: Mob Data: ', mob_data)
                        print('In Else :: Mob Value: ', mob_value)

                else:
                    print("[[[[[[[[[[[[--Not Working::Mobility--]]]]]]]]]]]]]")
                    return Response({'error': 'Invalid Topic Name'})

                # For Age
                if topic_name_list[6] == "Age":
                    print("________Age_________")

                    age_list = []

                    age_data = topic_name[6]['Age']
                    print('age_data: --->>', age_data)

                    age_value = topic_name[6]['value']
                    print('age_value: --->>', age_value)

                    topic = 'sex_age'

                    if age_value > 0:

                        for age in age_data:

                            age_id = list(age.items())

                            age_id_value = age_id[1][1]
                            print('age_id_value: ', age_id_value)

                            age_id_data = age_id[0][1]
                            print('age_id_data: ', age_id_data)

                            try:
                                sub_a_id_list = age_id_dict[age_id_data]
                                print('sub_a_id_list: ', sub_a_id_list)

                            except:
                                print(
                                    "Error: Given Value is Invalid :: Age", age_id_data)
                                return Response({'error': f"Age :: Given Value is Invalid :: {age_id_data}"})

                            for id in sub_a_id_list:
                                print("id----", id)

                                try:
                                    a_id = SexAge.objects.get(sex_age_id=id)
                                    print('a_id: ', a_id)

                                except:
                                    print(
                                        "Error: Invalid ID :: Age", id)
                                    return Response({'error': f"Age :: Invalid ID :: {id}"})

                                age_id = a_id.sex_age_id
                                print('age_id: ', age_id)

                                age_state, error = TotalPercentage.state_top_counties_data(
                                    SexAgeEstimate, topic, age_id, state_id, count, filter_type
                                )

                                print('age_state: ', age_state)
                                print('error: ', error)

                                if error is not None:
                                    print("Error", error)
                                    return Response({"error", f'{error}'})

                                if age_state.exists():

                                    for data in age_state:
                                        print("-----------",
                                              data.county.county_name)
                                        dic = {}
                                        dic[data.county.county_name] = age_id_value/count
                                        age_list.append(dic)

                                    print('age_list:---->>>', age_list)

                                else:
                                    print(
                                        "Error: No Data Avaliable in Topic_Name: Age")
                                    return Response({"error": "No Data Avaliable in Topic_Name: Age"})

                        age_result_list = dict(functools.reduce(
                            operator.add, map(collections.Counter, age_list)))
                        print('age_result_list:-------- ', age_result_list)

                        age_sorted_result = sorted(
                            age_result_list.items(), key=operator.itemgetter(1), reverse=True)
                        age_sorted_result = age_sorted_result[:count]
                        print('age_sorted_result: ', age_sorted_result)

                        age_final_dict = dict(age_sorted_result)
                        print('age_final_dict: ', age_final_dict)

                        for ele in age_final_dict:
                            age_final_dict.update({ele: age_value})
                        print('age_final_dict:------------->> ', age_final_dict)

                        all_combine_list.append(age_final_dict)

                    else:
                        print('In Else :: Age Data: ', age_data)
                        print('In Else :: Age Value: ', age_value)

                else:
                    print("[[[[[[[[[[[[--Not Working::Age--]]]]]]]]]]]]]")
                    return Response({'error': 'Invalid Topic Name'})

                print('\n all_combine_list:------------------\n', all_combine_list)

                if all_combine_list:

                    all_result_list = dict(functools.reduce(
                        operator.add, map(collections.Counter, all_combine_list)))
                    print('all_result_list:------------- ', all_result_list)

                    # Check for Similar Value
                    check = check_similar_value(all_result_list)

                    # If all keys have similar value : Sort by Alphabets
                    if check:
                        all_sorted_result = sorted(
                            all_result_list.items(), key=operator.itemgetter(0))
                        print('In If : all_sorted_result: ------------',
                              all_sorted_result)

                    # Else : Sort by Value
                    else:
                        all_sorted_result = sorted(
                            all_result_list.items(), key=operator.itemgetter(1), reverse=True)
                        print('In Else : all_sorted_result: ----------',
                              all_sorted_result)

                    all_sorted_result = all_sorted_result[:count]
                    print('all_sorted_result:--------- ', all_sorted_result)

                    all_final_dict = dict(all_sorted_result)
                    print('all_final_dict:=======> ', all_final_dict)

                    return Response({"result": all_final_dict})

                else:
                    return Response({'error': 'Select at-least one Topic'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in TCMF': f'{e}'})
