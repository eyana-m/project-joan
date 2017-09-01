from adaptor.model import CsvModel
  class Feature(CsvModel):
...     name = CharField()
...     age = IntegerField()
...     length = FloatField()
...
...     class Meta:
...         delimiter = ";"
...         dbModel = Person

from adaptor.model import CsvModel
    class MyCSvModel(CsvModel):
        feature_heading = CharField()
        requirement = IntegerField()
        feature_text = CharField()

    class Meta:
        delimiter = ","
        dbModel = Feature
