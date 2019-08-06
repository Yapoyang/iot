from django.shortcuts import render,render_to_response
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.core import serializers
import json
from datetime import datetime,timedelta
import requests
import urllib.request
import random
from iot_test.models import light_control,sensor_data,er,summary,oc,sensor_max,medical_record
from iot_test.form import Userform
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from socket import *
from sklearn import datasets
from sklearn import svm
from sklearn.externals import joblib
import time
from sqlalchemy import create_engine
import pandas as pd
import threading

def show_test(request):
    return HttpResponse('this site had been closed')

def load_test(request):
    return HttpResponse('this site had been closed')
def contact(request):
    return HttpResponse('this site had been closed')
def sensor_location():
    return HttpResponse('this site had been closed')
def find(request):
    if request.method=='GET':
       req=er.objects.all()
       req_dict=er.toDict(req.count(),req)
       req_json=json.dumps(req_dict)
       req_out=json.loads(req_json)
       return JsonResponse(req_out,safe=False)

def pr(request):
    dat=requests.get('http://192.168.0.110/vlc/gw/get/today/latest',timeout=.5).text
    #dat#
    #dat='"{\\"reply\\":1,\\"msg\\":{\\"GatewaySeqMin\\":207,\\"GatewaySeqMax\\":207,\\"DateTimeMin\\":\\"2019-2-20 17:09:56\\",\\"DateTimeMax\\":\\"2019-2-20 17:09:56\\",\\"GatewayHistoryCount\\":1,\\"GatewayHistoryMember\\":[{\\"GatewaySeq\\":207,\\"GatewayIP\\":\\"192.168.0.110\\",\\"GatewayMAC\\":\\"0c:54:15:6a:cd:a4\\",\\"Datetime\\":\\"2019-2-20 17:09:56\\",\\"devPkgCount\\":3,\\"devPkgMember\\":[{\\"type\\":2,\\"seq\\":6,\\"mac\\":\\"cc:78:ab:6b:fc:06\\",\\"lId1\\":3,\\"lId2\\":45,\\"br1\\":321,\\"br2\\":210,\\"Gx\\":2,\\"Gy\\":225,\\"Gz\\":255,\\"batPow\\":1,\\"labelX\\":0,\\"labelY\\":0,\\"labelH\\":256,\\"other\\":{\\"weight\\":5,\\"speed\\":150,\\"time\\":1},\\"rxLightCount\\":3,\\"rxLightInfo\\":[{\\"recLightID\\":6,\\"rssi\\":-64},{\\"recLightID\\":8,\\"rssi\\":-68},{\\"recLightID\\":9,\\"rssi\\":-66}]},{\\"type\\":1,\\"seq\\":194,\\"mac\\":\\"cc:78:ab:6c:05:03\\",\\"lId1\\":6,\\"lId2\\":0,\\"br1\\":45,\\"br2\\":0,\\"Gx\\":0,\\"Gy\\":255,\\"Gz\\":31,\\"batPow\\":79,\\"labelX\\":0,\\"labelY\\":0,\\"labelH\\":0,\\"other\\":{},\\"rxLightCount\\":2,\\"rxLightInfo\\":[{\\"recLightID\\":1,\\"rssi\\":-74},{\\"recLightID\\":6,\\"rssi\\":-49}]},{\\"type\\":1,\\"seq\\":141,\\"mac\\":\\"cc:78:ab:6b:fb:07\\",\\"lId1\\":5,\\"lId2\\":0,\\"br1\\":44,\\"br2\\":0,\\"Gx\\":0,\\"Gy\\":255,\\"Gz\\":31,\\"batPow\\":78,\\"labelX\\":0,\\"labelY\\":0,\\"labelH\\":0,\\"other\\":{},\\"rxLightCount\\":1,\\"rxLightInfo\\":[{\\"recLightID\\":9,\\"rssi\\":-64}]}]}]}}"'

    sel_macid=['cc:78:ab:6b:fc:00','cc:78:ab:6b:fc:06','cc:78:ab:6b:fb:04','cc:78:ab:6c:01:00',
               'cc:78:ab:6b:fe:80']
    sel_macid_dict={sel_macid[i]:str(i+1) for i in range(len(sel_macid))}
    #drop : 1,2,3
    dat_int_id=dat
    for i,j in sel_macid_dict.items():
        dat_int_id=dat_int_id.replace(i,j)
    try:
        dat_json=json.loads(json.loads(dat_int_id))
    except json.decoder.JSONDecodeError:
        dat_json=json.loads(json.loads(dat_int_id[:int(len(dat_int_id)/2)]))
    datetimenow=dat_json['msg']['GatewayHistoryMember'][0]['Datetime']
    dat_json_revise=dat_json['msg']['GatewayHistoryMember'][0]['devPkgMember']
    dat_uni=[]
    for j in range(1,(len(sel_macid)+1)):
        j=str(j)
        dat_temp= [dat_json_revise[i] for i in range(len(dat_json_revise)) if dat_json_revise[i]['mac']==j]
        if len(dat_temp)>0: dat_uni.append(dat_temp[0])
    dat_drop=[dat_uni[i] for i in range(len(dat_uni)) if dat_uni[i]['type']==2]
    k=['room','lid','iv','time','remaindertime','remainderweight','dripspeed','batterypower','patient_id','patient_bed','status',]
    val=[[str(dat_drop[j]['lId1']),str(dat_drop[j]['lId1']),str(dat_drop[j]['mac']),datetimenow]+\
        [str(dat_drop[j]['other'][i]) for i in ['time','weight']]+\
        [str(float(dat_drop[j]['other']['speed'])/10),str(dat_drop[j]['batPow']),'M01','R4102A'] for j in range(len(dat_drop))]
    for i in val:
        if float(i[5])>65000:
            temp='available'
        elif float(i[5])<20 and float(i[6])>=0:
            temp='drop is running out'
        elif float(i[7])<15:
            temp='battary is runnung out'
        elif float(i[4])==0 and float(i[5])>0 and float(i[6])==0:
            temp='stop'
        elif float(i[6])<0.3 and float(i[6])>0:
            temp='drip speed is too fast'
        elif float(i[6])>8:
            temp='drip speed is too slow'    
        else:
            temp=i[4]
        i.append(temp)
    for i in range(len(val)):
        if float(val[i][5])>65000:
            val[i][5]='0'
        difftime=datetime.now()-datetime.strptime(val[i][3],'%Y-%m-%d %H:%M:%S')
        if difftime.total_seconds()>60:
            val[i][10]='signal lost'
            
    exist_tag=[i[2] for i in val]
    engine = create_engine("mysql://root:itrieosl@127.0.0.1/iot")
    old_data=pd.read_sql('select * from iot.dropsys_temp_save',engine)
    old_data=old_data[k]
    update_data=old_data
    for i in val:
        update_data=update_data.loc[update_data.iv!=i[2]].append(pd.DataFrame([i],index=[int(i[2])-1],columns=k))
        update_data=update_data.sort_index()

    for i in range(update_data.shape[0]):    
        difftime=datetime.now()-datetime.strptime(update_data['time'][i],'%Y-%m-%d %H:%M:%S')
        if difftime.total_seconds()>60:
            update_data['status'][i]='signal lost'


    update_data.to_sql('dropsys_temp_save', engine, if_exists= 'replace',index=False)
    dat_out=update_data.to_dict('records')
    out={'member':dat_out}

    return JsonResponse(out)
    #for i in range(1,len(sel_macid)+1):
    #    i=str(i)
    #    if i not in exist_tag:
    #        val=val+[['-','-',i,datetimenow,'-','-','-','-','-','-','signal lost']]

    
    #dat_out_drop=[dict(zip(k,val[i])) for i in range(len(val))]
    #dat_out=[]
    #for j in range(1,(len(sel_macid)+1)):
    #    j=str(j)
    #    dat_temp= [dat_out_drop[i] for i in range(len(dat_out_drop)) if dat_out_drop[i]['iv']==j]
    #    dat_out=dat_out+dat_temp
def request_rep():
    out={'socketRemoteServerIP':'192.168.0.106','socketRemoteServerPort':'6996'}
    while True:
        requests.post('http://192.168.0.107/vlc/gw/post/remoteServer/',out)
    print('1')
    return('ok')


def medical_record_post(request,value):
    f=[medical_record.objects.values_list('name')[i][0] for i in range(0,medical_record.objects.count())]
    f=['']+f
    if request.method=='GET':
        if 'patient' in request.GET:
            name=request.GET['patient']
            #obj=medical_record.objects.get(name=request.GET['patient'])
            #if len(request.GET['blood_pressure'])>0:
            #   obj.blood_pressure=request.GET['blood_pressure']
            #   obj.body_temperature=request.GET['body_temperature']
            #   obj.save()
            return render_to_response('load.html',locals())

        elif 'blood_pressure' in request.GET:
            obj=medical_record.objects.get(name=value)
            obj.blood_pressure=request.GET['blood_pressure']
            obj.body_temperature=request.GET['body_temperature']
            obj.save()
            name=obj.name
            age=obj.age
            gender=obj.gender
            clinic=obj.clinic
            blood_pressure=obj.blood_pressure
            body_temperature=obj.body_temperature
            return render_to_response('medical_record.html',locals())
        else:
            try:
                obj=medical_record.objects.get(name=value)
                name=obj.name
                age=obj.age
                gender=obj.gender
                clinic=obj.clinic
                blood_pressure=obj.blood_pressure
                body_temperature=obj.body_temperature
                return render_to_response('medical_record.html',locals())
            except (MultiValueDictKeyError and ObjectDoesNotExist) as e:
                name,age,gender,clinic,blood_pressure,body_temperature='','','','','',''
                return render_to_response('medical_record.html',locals())

    if request.method=='POST':
       headers=json.dumps({'contenttype':'application/json'})
       name=request.POST['name']
       age=request.POST['age']
       gender=request.POST['gender']
       clinic=request.POST['clinic']
       bp=request.POST['blood_pressure']
       bt=request.POST['body_temperature']
       payload={'name':name,'age':age,'gender':gender,'clinic':clinic,'blood_pressure':bp,'body_temperature':bt}
       try:
            obj=medical_record.objects.get(name=name)
            obj.age=age
            obj.gender=gender
            obj.clinic=clinic
            obj.blood_pressure=bp
            obj.body_temperature=bt
            obj.save()
       except ObjectDoesNotExist:
            requests.post('http://192.168.0.100/medical_load/',json.dumps(payload),headers)
       return render_to_response('load.html',locals())


def medical_load(request):
    if request.method=='POST':
       req=json.loads(request.body.decode('utf-8'))
       name=req.get('name')
       gender=req.get('gender')
       age=req.get('age')
       clinic=req.get('clinic')
       bp=req.get('blood_pressure')
       bt=req.get('body_temperature')
       tb_insert_data=medical_record(name=name,gender=gender,age=age,clinic=clinic,blood_pressure=bp,body_temperature=bt)
       tb_insert_data.save()
    else:
       return JsonResponse('wrong request',safe=false)

def medical_record_find(request):
    if request.method=='GET':
       req=medical_record.objects.all()
       req_dict=medical_record.toDict(req.count(),req)
       req_json=json.dumps(req_dict)
       req_out=json.loads(req_json)
       return JsonResponse(req_out,safe=False)

def light_adjust_vlc(request):
    if  request.method=='GET':
        br=request.GET['brightness']
        driverId=str(request.GET['driverId'])
        if  driverId==str(0):
            driverId="255"
        if  'colorTemperature' in request.GET:
            ct=request.GET['colorTemperature']
            out={"brightness":str(br),'driverId':str(driverId),'colorTemperature':str(ct)}
            requests.post('http://192.168.0.110/vlc/gw/post/dimming/colorTemperature/',out)
            return HttpResponse(str(out))
        else:
            out={"brightness":str(br),'driverId':str(driverId)}
            requests.post('http://192.168.0.110/vlc/gw/post/dimming/brightness/',out)
            return HttpResponse(str(out))

def dropsys(request):
    dat=requests.get('http://192.168.0.110/vlc/gw/get/today/latest',timeout=.5).text
    #time.sleep(0.1)
    #dat2=requests.get('http://192.168.0.110/vlc/gw/get/today/latest',timeout=.5).text
    #dat='"{\\"reply\\":1,\\"msg\\":{\\"GatewaySeqMin\\":207,\\"GatewaySeqMax\\":207,\\"DateTimeMin\\":\\"2019-2-20 17:09:56\\",\\"DateTimeMax\\":\\"2019-2-20 17:09:56\\",\\"GatewayHistoryCount\\":1,\\"GatewayHistoryMember\\":[{\\"GatewaySeq\\":207,\\"GatewayIP\\":\\"192.168.0.110\\",\\"GatewayMAC\\":\\"0c:54:15:6a:cd:a4\\",\\"Datetime\\":\\"2019-2-20 17:09:56\\",\\"devPkgCount\\":3,\\"devPkgMember\\":[{\\"type\\":2,\\"seq\\":6,\\"mac\\":\\"cc:78:ab:6b:fc:06\\",\\"lId1\\":3,\\"lId2\\":45,\\"br1\\":321,\\"br2\\":210,\\"Gx\\":2,\\"Gy\\":225,\\"Gz\\":255,\\"batPow\\":100,\\"labelX\\":0,\\"labelY\\":0,\\"labelH\\":256,\\"other\\":{\\"weight\\":48,\\"speed\\":15,\\"time\\":1},\\"rxLightCount\\":3,\\"rxLightInfo\\":[{\\"recLightID\\":6,\\"rssi\\":-64},{\\"recLightID\\":8,\\"rssi\\":-68},{\\"recLightID\\":9,\\"rssi\\":-66}]},{\\"type\\":1,\\"seq\\":194,\\"mac\\":\\"cc:78:ab:6c:05:03\\",\\"lId1\\":6,\\"lId2\\":0,\\"br1\\":45,\\"br2\\":0,\\"Gx\\":0,\\"Gy\\":255,\\"Gz\\":31,\\"batPow\\":79,\\"labelX\\":0,\\"labelY\\":0,\\"labelH\\":0,\\"other\\":{},\\"rxLightCount\\":2,\\"rxLightInfo\\":[{\\"recLightID\\":1,\\"rssi\\":-74},{\\"recLightID\\":6,\\"rssi\\":-49}]},{\\"type\\":1,\\"seq\\":141,\\"mac\\":\\"cc:78:ab:6b:fb:07\\",\\"lId1\\":5,\\"lId2\\":0,\\"br1\\":44,\\"br2\\":0,\\"Gx\\":0,\\"Gy\\":255,\\"Gz\\":31,\\"batPow\\":78,\\"labelX\\":0,\\"labelY\\":0,\\"labelH\\":0,\\"other\\":{},\\"rxLightCount\\":1,\\"rxLightInfo\\":[{\\"recLightID\\":9,\\"rssi\\":-64}]}]}]}}"'
    #dat='"{\\"reply\\":1,\\"msg\\":{\\"GatewaySeqMin\\":15524,\\"GatewaySeqMax\\":15524,\\"DateTimeMin\\":\\"2019-3-21 02:40:12\\",\\"DateTimeMax\\":\\"2019-3-21 02:40:12\\",\\"GatewayHistoryCount\\":1,\\"GatewayHistoryMember\\":[{\\"GatewaySeq\\":15524,\\"GatewayIP\\":\\"192.168.0.110\\",\\"GatewayMAC\\":\\"8c:f7:10:34:74:02\\",\\"Datetime\\":\\"2019-3-21 02:40:12\\",\\"devPkgCount\\":2,\\"devPkgMember\\":[{\\"type\\":2,\\"seq\\":37,\\"mac\\":\\"4\\",\\"lId1\\":33,\\"lId2\\":33,\\"br1\\":136,\\"br2\\":76,\\"Gx\\":1,\\"Gy\\":225,\\"Gz\\":0,\\"batPow\\":100,\\"labelX\\":1,\\"labelY\\":0,\\"labelH\\":0,\\"other\\":{\\"weight\\":57,\\"speed\\":0,\\"time\\":0},\\"rxLightCount\\":1,\\"rxLightInfo\\":[{\\"recLightID\\":5,\\"rssi\\":-73}]},{\\"type\\":1,\\"seq\\":163,\\"mac\\":\\"8\\",\\"lId1\\":5,\\"lId2\\":8,\\"br1\\":46,\\"br2\\":44,\\"Gx\\":0,\\"Gy\\":255,\\"Gz\\":32,\\"batPow\\":57,\\"labelX\\":0,\\"labelY\\":0,\\"labelH\\":0,\\"other\\":{},\\"rxLightCount\\":2,\\"rxLightInfo\\":[{\\"recLightID\\":2,\\"rssi\\":-47},{\\"recLightID\\":5,\\"rssi\\":-37}]}]}]}}""{\\"reply\\":1,\\"msg\\":{\\"GatewaySeqMin\\":15524,\\"GatewaySeqMax\\":15524,\\"DateTimeMin\\":\\"2019-3-21 02:40:12\\",\\"DateTimeMax\\":\\"2019-3-21 02:40:12\\",\\"GatewayHistoryCount\\":1,\\"GatewayHistoryMember\\":[{\\"GatewaySeq\\":15524,\\"GatewayIP\\":\\"192.168.0.110\\",\\"GatewayMAC\\":\\"8c:f7:10:34:74:02\\",\\"Datetime\\":\\"2019-3-21 02:40:12\\",\\"devPkgCount\\":2,\\"devPkgMember\\":[{\\"type\\":2,\\"seq\\":37,\\"mac\\":\\"4\\",\\"lId1\\":33,\\"lId2\\":33,\\"br1\\":136,\\"br2\\":76,\\"Gx\\":1,\\"Gy\\":225,\\"Gz\\":0,\\"batPow\\":100,\\"labelX\\":1,\\"labelY\\":0,\\"labelH\\":0,\\"other\\":{\\"weight\\":57,\\"speed\\":0,\\"time\\":0},\\"rxLightCount\\":1,\\"rxLightInfo\\":[{\\"recLightID\\":5,\\"rssi\\":-73}]},{\\"type\\":1,\\"seq\\":163,\\"mac\\":\\"8\\",\\"lId1\\":5,\\"lId2\\":8,\\"br1\\":46,\\"br2\\":44,\\"Gx\\":0,\\"Gy\\":255,\\"Gz\\":32,\\"batPow\\":57,\\"labelX\\":0,\\"labelY\\":0,\\"labelH\\":0,\\"other\\":{},\\"rxLightCount\\":2,\\"rxLightInfo\\":[{\\"recLightID\\":2,\\"rssi\\":-47},{\\"recLightID\\":5,\\"rssi\\":-37}]}]}]}}"'
    sel_macid=['cc:78:ab:6b:fb:07','cc:78:ab:6b:ba:83','cc:78:ab:6b:fb:03','cc:78:ab:6c:01:00',
                'cc:78:ab:6b:fc:07','cc:78:ab:6b:fc:86','cc:78:ab:6b:fd:83','cc:78:ab:6c:09:87',
                'cc:78:ab:6c:09:83',"cc:78:ab:6b:fb:87",'cc:78:ab:6b:fd:87','cc:78:ab:6c:07:87',
                'cc:78:ab:6c:05:03','cc:78:ab:6b:fc:06','cc:78:ab:6b:f9:80','cc:78:ab:6b:fb:04',
                'cc:78:ab:6b:fc:00','c:61:cf:c6:90:ea', 'c:61:cf:c6:93:12']
    sel_macid_dict={sel_macid[i]:str(i+1) for i in range(len(sel_macid))}
    dat_int_id=dat
    #dat_int_id2=dat2
    for i,j in sel_macid_dict.items():
        dat_int_id=dat_int_id.replace(i,j)
    #    dat_int_id2=dat_int_id2.replace(i,j)
    try:
        dat_json=json.loads(json.loads(dat_int_id))
    except json.decoder.JSONDecodeError:
        dat_json=json.loads(json.loads(dat_int_id[:int(len(dat_int_id)/2)]))
    #dat_json=json.loads(json.loads(dat_int_id))
    dat_json_revise=dat_json['msg']['GatewayHistoryMember'][0]['devPkgMember']

    #dat_json2=json.loads(json.loads(dat_int_id2))
    #dat_json_revise2=dat_json2['msg']['GatewayHistoryMember'][0]['devPkgMember']

    #dat_json_revise=dat_json_revise+dat_json_revise2
    #x_test=[[i['br1'],i['br2'],str(i['lId1']),str(i['lId2'])] for i in dat_json_revise ]
   # clf3=joblib.load('/home/pi/Desktop/mmhiot/svm/clf.pkl')
    #svmout=clf3.predict(x_test)

    #for i in range(len(dat_json_revise)):
       # dat_json_revise[i]['lId1']=int(svmout[i])

    #combine drop and sensor data
    dat_drop=[dat_json_revise[i] for i in range(len(dat_json_revise)) if dat_json_revise[i]['type']==2]
    dat_sensor=[dat_json_revise[i] for i in range(len(dat_json_revise)) if dat_json_revise[i]['type']==1]
    k=['lightid1','tagid','time','remaindertime','remainderweight','dripspeed','batterypower']
    datetimenow=str(datetime.now())[:-7]
    val=[[dat_drop[j]['lid1'],dat_drop[j]['mac'],datetimenow]+[str(dat_drop[j]['other'][i]) for i in ['time','weight']]+[str(float(dat_drop[j]['other']['speed'])/10),str(dat_drop[j]['batPow'])] for j in range(len(dat_drop))]
    dat_out_drop=[dict(zip(k,val[i])) for i in range(len(val))]
    val_sensor=[[dat_sensor[i]['lid1'],dat_sensor[i]['mac'],datetimenow,'','','',str(dat_sensor[i]['batPow'])] for i in range(len(dat_sensor))]
    dat_out_sensor=[dict(zip(k,val_sensor[i])) for i in range(len(val_sensor))]
    dat_out_sensor_uni=[]
    for i in range(1,(len(sel_macid)+1)):
        temp=[dat_out_sensor[j] for j in range(len(dat_out_sensor)) if dat_out_sensor[j]['tagid']==str(i)]
        if len(temp)>0:
            dat_out_sensor_uni=dat_out_sensor_uni+[temp[-1]]

    out={'member':dat_out_drop+dat_out_sensor_uni}

    return JsonResponse(out)
