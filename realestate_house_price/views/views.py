from django.shortcuts import render
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.utils import json_file_read

from realestate_app.models import (County, State,)

from realestate_house_price.models import (
    HousePrice,
    HousePriceEstimate, HousePriceError,
    HousePriceStateTotal
)


# ------------------------------------------------------------------------------------------------------
# --------------------- Populate House_Price Code Data in the HousePrice Table -------------------------

class HousePriceCodeData(APIView):

    def post(self, request):

        try:
            if request.data:
                file_name = request.data.get('File_Name')

                data_dict = json_file_read(file_name)
                # print('data_dict: ', type(data_dict))

                data_value = data_dict.get('tables').get(
                    'B25075').get('columns')
                # print('data_value: ', data_value)

                for code in data_value:
                    sub_hp_id = code
                    sub_hp_name = data_value.get(sub_hp_id).get('name')
                    # print('sub_hp_id: ', sub_hp_id)
                    # print('sub_hp_name: ', sub_hp_name)

                    try:
                        hp_db = HousePrice.objects.get(
                            house_price_id=sub_hp_id)
                        print('hp_db in TRY--->: ', hp_db)

                    except:
                        hpdb_data = HousePrice.objects.create(
                            house_price_id=sub_hp_id,
                            house_price_name=sub_hp_name
                        )
                        print('hpdb_data in EXCEPT===<: ', hpdb_data)

                return Response({'msg': 'HousePrice DB Populated.'})

            else:
                return Response({'error': "Invalid request"})

        except Exception as e:
            return Response({'error in HPCD': f'{e}'})


#   ------------------------------------------------------------------------------------------------------------
#   ------------------- Populate House_Price Error/Estimate Data in their Respective Tables --------------------


class HousePriceEstimateErrorData(APIView):

    def post(self, request):

        try:
            if request.data:
                file_name = request.data.get('File_Name')

                data_dict = json_file_read(file_name)
                # print('data_dict: ', type(data_dict))

                data_value = data_dict.get('data')

                county_data = County.objects.all()

                for county in county_data:

                    if county.county_id in data_value:
                        print('county.county_id: ', county.county_id)

                        house_price_value = data_value.get(
                            county.county_id).get("B25075")
                        # print('house_price_value: --->', house_price_value)

                        house_price_code = HousePrice.objects.all()
                        # print('house_price_code: ', house_price_code)

                        # For houseprice_total in County Table
                        house_price_total = house_price_value.get(
                            'estimate').get("B25075001")

                        if house_price_total:
                            print("In hp_Total=====")

                            county_obj = County.objects.get(
                                county_id=county.county_id)
                            county_obj.house_price_total = house_price_total
                            county_obj.save()

                        else:
                            print("___NO hp_total___")

                        for house_price in house_price_code:
                            print('house_price: ', house_price)

                            # For House_Price Estimate
                            house_price_estimate = house_price_value.get(
                                'estimate').get(house_price.house_price_id)
                            # print('house_price_estimate:---> ',
                            #       house_price_estimate)

                            if house_price_estimate:
                                print('In IF :: house_price_estimate: ',
                                      house_price_estimate)
                                try:
                                    hpest_db = HousePriceEstimate.objects.get(
                                        county_id=county.county_id,
                                        house_price_id=house_price.house_price_id
                                    )
                                    print('hpest_db In TRY --->: ', hpest_db)

                                except:
                                    hpestdb_data = HousePriceEstimate.objects.create(
                                        house_price_estimate_value=house_price_estimate,
                                        county_id=county.county_id,
                                        house_price_id=house_price.house_price_id
                                    )
                                    print('hpestdb_data In EXCEPT ====<: ',
                                          hpestdb_data)

                            else:
                                print('In else_hpest :: No Value',
                                      house_price_estimate)
                                pass

                            # For House_Price Error
                            house_price_error = house_price_value.get(
                                'error').get(house_price.house_price_id)
                            # print('house_price_error:===< ', house_price_error)

                            if house_price_error:
                                print('In IF :: house_price_error: ',
                                      house_price_error)
                                try:
                                    hperr_db = HousePriceError.objects.get(
                                        county_id=county.county_id,
                                        house_price_id=house_price.house_price_id
                                    )
                                    print('hperr_db In TRY -->: ', hperr_db)

                                except:
                                    hperrdb_data = HousePriceError.objects.create(
                                        house_price_error_value=house_price_error,
                                        county_id=county.county_id,
                                        house_price_id=house_price.house_price_id
                                    )
                                    print('hperrdb_data In EXCEPT ==<": ',
                                          hperrdb_data)

                            else:
                                print('In else-hperr :: No Value: ',
                                      house_price_error)
                                pass

                    else:
                        print("In Else HPEED.")
                        pass

                return Response({'msg': 'HousePriceEstimateError DB Populated.'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in HPEED': f'{e}'})


#   ------------------------------------------------------------------------------------------------------------
#   ------------------- Populate House_Price_State_Total Data in the Respective Table --------------------------

class HousePriceStateTotalData(APIView):

    def post(self, request):

        try:
            count = 0
            state_data = State.objects.all()

            for s_id in state_data:
                hp_data = HousePrice.objects.all()

                for hp_id in hp_data:
                    # print('s_id: ', s_id)
                    # print('hp_id: ', hp_id)

                    hp_total = HousePriceEstimate.objects.filter(
                        county__state_id=s_id, house_price_id=hp_id
                    ).aggregate(sum_hp=Sum('house_price_estimate_value'))

                    # print('hp_total:=== ', hp_total)

                    state_total = County.objects.filter(state_id=s_id).aggregate(
                        sum_state=Sum('house_price_total'))

                    # print('state_total: ===', state_total)

                    count += 1
                    print('count:------------------- ', count)

                    if hp_total['sum_hp'] and state_total['sum_state']:
                        print("In If -------->")
                        print('hp_total: ', hp_total['sum_hp'])
                        print('state_total: ', state_total['sum_state'])

                        try:
                            hp_state_db = HousePriceStateTotal.objects.get(
                                state_id=s_id, house_price_id=hp_id
                            )
                            print('hp_state_db: In TRY---> ', hp_state_db)

                        except:
                            hp_state_totaldb = HousePriceStateTotal.objects.create(
                                state_id=s_id,
                                house_price_id=hp_id,
                                state_total=state_total['sum_state'],
                                house_price_total=hp_total['sum_hp']
                            )
                            print('hp_state_totaldb: EXCEPT ===< ',
                                  hp_state_totaldb)

                    else:
                        print("In ELSE::______")
                        print('hp_total: ', hp_total['sum_hp'])
                        print('state_total: ', state_total['sum_state'])

            return Response({'msg': 'HousePriceStateTotal DB Populated.'})

        except Exception as e:
            return Response({'error in HPSTD': f'{e}'})
