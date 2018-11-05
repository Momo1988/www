from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient, ASCENDING
import pandas, pymongo, json
import time,datetime
# Create your views here.
# class DataCCC():
#     """docstring for ."""
#     def __init__(self):
#         self.client = MongoClient()
#         self.db = self.client['WeatherData']
#         self.collection = self.db['WeatherData']
#         self.datatypes = ['wind', 'wave', 'temp', 'pressure', 'water', 'chlorophyll', 'salt']

def index(request):
    client = MongoClient()
    db = client['WeatherData']
    collection = db['WeatherData']
    datatypes = ['wind', 'wave', 'temp', 'pressure', 'water', 'chlorophyll', 'salt']
    pd = pandas.DataFrame(list(collection.find().sort('_id', pymongo.ASCENDING)))
    data = pd.tail(10).reindex(columns=['STNM','TYPE','DataCat','TM'])
    grouped = pd.groupby('DataCat')
    # data = list(collection.find({'DataCat': 'wave'}).sort('_id', ASCENDING).limit(5))
    # html = df.to_html(classes=["table-bordered", "table-striped", "table-hover"])
    # print(data)
    # {'data': pd.to_html()}
    context = {'data': data.to_html(index=False, classes="table table-striped table-sm"),
        'group': grouped.size().to_json(),'test':'123123'}
    print(grouped.size().to_json())
        # 'group':grouped.size().to_json()}
    # context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)


def wave(request):
    client = MongoClient()
    db = client['WeatherData']
    collection = db['WeatherData']
    datatypes = ['wind', 'wave', 'temp', 'pressure', 'water', 'chlorophyll', 'salt']
    timeArray = datetime.datetime.utcfromtimestamp(time.time()-24*60*60)
    time_24H_before = timeArray.strftime("%Y-%m-%d %H:%M:%S")

    pd = pandas.DataFrame(list(collection.find({'DataCat':'wave','TM':{"$gt":time_24H_before}}).sort('_id', pymongo.ASCENDING)))
    data = pd.reindex(columns=['STNM','YXBG','ZDBG','LJ','TM'])\
            .rename(columns = {'YXBG':'有效波高','STNM':'浮标','ZDBG':'最大波高','LJ':'浪级','TM':'时间'})
    grouped = data.groupby('浮标')
    # data = list(collection.find({'DataCat': 'wave'}).sort('_id', ASCENDING).limit(5))
    # html = df.to_html(classes=["table-bordered", "table-striped", "table-hover"])
    # print(data)
    # {'data': pd.to_html()}
    dtm = grouped.get_group('1号标')['浮标']
    context = {'data': data.tail(20).to_html(index=False, classes="table table-striped table-sm"),\
        # 'pd':data.to_json(orient='index'),\
        'TM':grouped.get_group('1号标')['时间'].to_json(),\
        'YXBG':grouped.get_group('1号标')['有效波高'].to_json(),\
        'ZDBG':grouped.get_group('1号标')['最大波高'].to_json(),\
        'group': grouped.size().to_json(),'test':'123123'
        }
    # print(json.dumps(dtm.to_json()))
    # print(grouped.get_group('1号标').YXBG.to_json())

        # 'group':grouped.size().to_json()}
    # context['hello'] = 'Hello World!'
    return render(request, 'wave.html', context)
