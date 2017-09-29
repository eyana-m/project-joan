from django import template
from django.template.loader import get_template
from datetime import timedelta, date
from django.utils.timezone import localtime, now

register = template.Library()
t = get_template('joan/status.html')

@register.inclusion_tag(t)
def show_status(model):
    return {'model': model }


@register.filter(expects_localtime=True)
def count_business_days(to_date):
    from_date = localtime(now()).date()
    try:
        #future
        if to_date > from_date:
            day_generator = (from_date + timedelta(x + 1) for x in range((to_date - from_date).days))
            mandays = sum(1 for day in day_generator if day.weekday() <= 5)
            if mandays > 1: return str(mandays)  + " workdays to go"
            else: return str(mandays)  + " workday to go"
        else:
            day_generator = (from_date + timedelta(x + 1) for x in range((from_date - to_date).days))
            mandays = sum(1 for day in day_generator if day.weekday() <= 5) + 1
            if mandays > 1: return str(mandays)  + " workdays ago"
            else: return str(mandays)  + " workday ago"

    except AttributeError:
        return ''


@register.filter
def get_features(ticket):
    temp = []
    for obj in Feature.objects.filter(ticket__id__exact=self.id):
        temp.append("obj.feature_text")
    if len(temp) >1:
        temp2 = temp[:1]
        temp2.append('more')
        return temp2
    else:
        return temp

@register.filter
def get_done_features(release):
    done = Feature.objects.filter(release__id__exact=self.id).filter(feature_status_exact="DO").count()
    return done
