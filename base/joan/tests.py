from django.test import TestCase
from adaptor.model import CsvModel, CsvDbModel, ImproperlyConfigured,\
    CsvException, CsvDataException, TabularLayout, SkipRow,\
    GroupedCsvModel, CsvFieldDataException
from tests.test_app.models import *


class TestCsvDBOnlyModel(CsvDbModel):
    class MyCSvModel(CsvModel):
        feature_heading = CharField()
        requirement = ForeignKey(key=requirement.reqd_id)
        feature_text = CharField()

    class Meta:
        dbModel = Feature
        has_header = True
        delimiter = ";"
    #        exclude = ['id']
