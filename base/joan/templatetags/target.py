# from django import template
# from django.template.loader import get_template
# from datetime import timedelta, date
# from django.utils.timezone import localtime, now
# register = template.Library()
# target = get_template('joan/target_status.html')
#
# #Soon Note: need to add more logic based on release_status
# @register.inclusion_tag(target)
# def target_status(to_date):
#     from_date = localtime(now()).date()
#     try:
#         #future
#         if to_date > from_date:
#             return {'target': 'On Target'}
#         elif to_date == from_date:
#             return {'target': 'Due Today'}
#         else:
#             return {'target': 'Late'}
#
#
#     except AttributeError:
#         return ''
