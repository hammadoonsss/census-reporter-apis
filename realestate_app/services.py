from django.db.models import Count, Min, Max, F, Q, Sum

from rest_framework.response import Response

from realestate_app.models import *


class TotalPercentage():

    @staticmethod
    def top_state_data(table_name, topic_name, topic_id, count, filter_type):
        
        table = table_name
        print('table_name: ', table)
        topic = topic_name
        print('topic: ', topic)
        t_id = topic_id
        print('topic_id: ', t_id)
        filt_ty = filter_type
        print('filter_type: ', filt_ty)
        count_no = count
        print('count: ', count_no)

        lookup = "%s_id" % topic
        print('lookup: ', lookup)

        topic_id_raw = t_id[0:6]
        print('topic_id_raw: ', topic_id_raw)

        exclude_value = "%s001" % topic_id_raw
        print('exclude_value: ', exclude_value)

        topic_state = table.objects.exclude(**{lookup: exclude_value}).annotate(
            percent=(F(f'{topic}_total')*100)/F('state_total')
        ).filter(**{lookup: t_id})

        if filt_ty == "Top":
            topic_state = topic_state.order_by('-percent')[:count_no]
            print('topic_state_top: ', topic_state)

            return topic_state

        elif filt_ty == "Bottom":
            topic_state = topic_state.order_by('percent')[:count_no]
            print('topic_state_bottom: ', topic_state)

            return topic_state

        else:
            return Response({'msg': 'Invalid Filter Type'})

    @staticmethod
    def top_counties_data(table_name, topic_name, topic_id, count, filter_type):

        table = table_name
        print('table_name: ', table)
        topic = topic_name
        print('topic: ', topic)
        t_id = topic_id
        print('topic_id: ', t_id)
        filt_ty = filter_type
        print('filter_type: ', filt_ty)
        count_no = count
        print('count: ', count_no)

        lookup = "%s_id" % topic
        print('lookup: ', lookup)

        topic_id_raw = t_id[0:6]
        print('topic_id_raw: ', topic_id_raw)

        exclude_value = "%s001" % topic_id_raw
        print('exclude_value: ', exclude_value)

        topic_state = table.objects.exclude(**{lookup: exclude_value}).annotate(
            percent=(F(f'{topic}_estimate_value')*100)/F(f'county__{topic}_total')
        ).filter(**{lookup: t_id})

        if filt_ty == "Top":
            topic_state = topic_state.order_by('-percent')[:count_no]
            print('topic_state_top: ', topic_state)

            return topic_state

        elif filt_ty == "Bottom":
            topic_state = topic_state.order_by('percent')[:count_no]
            print('topic_state_bottom: ', topic_state)

            return topic_state

        else:
            return Response({'msg': 'Invalid Filter Type'})

    @staticmethod
    def state_top_counties_data(table_name, topic_name, topic_id, state, count, filter_type):

        table = table_name
        print('table_name: ', table)
        topic = topic_name
        print('topic: ', topic)
        t_id = topic_id
        print('topic_id: ', t_id)
        filt_ty = filter_type
        print('filter_type: ', filt_ty)
        count_no = count
        print('count: ', count_no)
        s_id=state
        print('state_name: ', s_id)

        lookup = "%s_id" % topic
        print('lookup: ', lookup)

        topic_id_raw = t_id[0:6]
        print('topic_id_raw: ', topic_id_raw)

        exclude_value = "%s001" % topic_id_raw
        print('exclude_value: ', exclude_value)

        topic_state = table.objects.exclude(**{lookup: exclude_value}).annotate(
            percent=(F(f'{topic}_estimate_value')*100)/F(f'county__{topic}_total')
        ).filter(**{lookup: t_id}, county__state_id=s_id)

        if filt_ty == "Top":
            topic_state = topic_state.order_by('-percent')[:count_no]
            print('topic_state_top: ', topic_state)

            return topic_state

        elif filt_ty == "Bottom":
            topic_state = topic_state.order_by('percent')[:count_no]
            print('topic_state_bottom: ', topic_state)

            return topic_state

        else:
            return Response({'msg': 'Invalid Filter Type'})
