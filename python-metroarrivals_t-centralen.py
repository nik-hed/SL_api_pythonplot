

#Usefull links:
#https://sv.wikipedia.org/wiki/Stockholms_tunnelbana
#https://support.trafiklab.se/org/trafiklabse/d/sl-api-problem-med-solna-station/
#https://www.trafiklab.se/api/trafiklab-apis/sl/


import requests
import json
import datetime
import pytz
from io import BytesIO
import pycurl

import matplotlib.pyplot as plt
import math



APIKEY = 'YOUR APIKEY FROM TRAFIKLAB.SE'


"""

OriginIds:

T-centralen=9001

Blåa linjen:

Kungsträdgården=9340
Akalla=9300
Hjulsta=9320

Röda linjen:
    
Norsborg=9280
Ropsten=9220
Fruängen=9260
Mörby centrum=9200

Gröna linjen:

Åkeshov=9108
Skarpnäck=9140
Alvik=9112
Farsta strand=9180
Hässelby strand=9100
Hagsätra=9160

"""

# To get info from sl, based on https://github.com/jfjallid/Stockholm-SL-API-Python-library
#https://github.com/jfjallid/Stockholm-SL-API-Python-library/blob/master/examples/travelPlans.py
def getTravelInfoNowJson(fromStationID, toStationID,position):
     buffer = BytesIO()
     c = pycurl.Curl()
     c.setopt(c.URL, 'https://api.sl.se/api2/TravelplannerV3_1/trip.json?key='+APIKEY +'&originId='+str(fromStationID)+'&destId='+str(toStationID))
     c.setopt(c.WRITEDATA, buffer)
     c.perform()
     c.close()
    
     body = buffer.getvalue()
     obj = json.loads(body.decode('utf-8'))
     arrivaltime = []
     
     for i in obj['Trip']:
         
         for k in i['LegList']['Leg']:
             arrivaltime.append(datetime.datetime.strptime(k['Origin']['time'],"%H:%M:%S")-datetime.datetime.strptime(datetime.datetime.now(pytz.timezone('Europe/Stockholm')).strftime('%H:%M:%S'),"%H:%M:%S"))
      
     x = []  #Time to arrival
     y = []  #Where on the x-axis should the train be plotted, the code was initially written to plot on the y-axis.

     for i in arrivaltime:
         
         if i.total_seconds()/60>0 and i.total_seconds()/60<40:  # Get all trains that are within 40 minutes from T-centralen
             
             y.append(position)
             x.append(math.floor(i.total_seconds()/60))
             
     
        
     return x[:4],y[:4] #Get 4 latest trains





def plot_Trip(direction,x,y,line,linenumber,color):
    
    n=1
    k=list(range(len(x)))
    
    if direction =='up':
        k = [(x+1)*20 for x in k]
        plt.plot(y,k,'*',color=color,label=line, marker=uparrow, markersize=10)
        for a,b in zip(y,x): 
            plt.text(a, n*20,'  '+str(b)+linenumber)           
            n=n+1
    else:
        k = [-(x+1)*20 for x in k]
        plt.plot(y,k,'*',color=color,label=line, marker=downarrow, markersize=10)
        for a,b in zip(y,x): 
            plt.text(a, -n*20, '  '+str(b)+linenumber)
            n=n+1


################Travelinfo for all lines##############################

#Blue line

#Kungsträdgården
x_10_5,y_10_5=getTravelInfoNowJson(9001, 9340,-25)
#Akalla
x_10,y_10=getTravelInfoNowJson(9001, 9300,-10)
#Hjulsta
x_11,y_11=getTravelInfoNowJson(9001, 9320,-47)

#Red line

#Norsborg
x_13_2,y_13_2=getTravelInfoNowJson(9001, 9280,-120)

#Ropsten
x_13_1,y_13_1=getTravelInfoNowJson(9001, 9220,-120)

#Fruängen
x_14_2,y_14_2=getTravelInfoNowJson(9001, 9260,-85)

#Mörby centrum
x_14_1,y_14_1=getTravelInfoNowJson(9001, 9200,-85)

#Green line

#Åkeshov       
x_17_1,y_17_1=getTravelInfoNowJson(9001, 9108,30)
#Skarpnäck
x_17_2,y_17_2=getTravelInfoNowJson(9001, 9140,30)

#Alvik
x_18_1,y_18_1=getTravelInfoNowJson(9001, 9112,70)

#Farsta strand
x_18_2,y_18_2=getTravelInfoNowJson(9001, 9180,70)

#Hässelby strand      
x_19_1,y_19_1=getTravelInfoNowJson(9001, 9100,105)

#Hagsätra 
x_19_2,y_19_2=getTravelInfoNowJson(9001, 9160,105)


        




####################### Make plot   ####################################################

plt.style.use('dark_background')

plt.axis('off')



plt.title('Tunnelbana från T-centralen')


yy = [0, 0]
xx = [-130, 130]

downarrow = u'$\u2193$'
uparrow = u'$\u2191$'


    

plt.plot(xx,yy,color='white',label='T-centralen')



plot_Trip('up',x_19_1,y_19_1,'19-Hässelby Strand','(19)','green')
plot_Trip('up',x_18_1,y_18_1,'18-Alvik','(18)','green')
plot_Trip('up',x_17_1,y_17_1,'17-Åkeshov','(17)','green')
plot_Trip('down',x_19_2,y_19_2,'19-Hagsätra','(19)','green')
plot_Trip('down',x_18_2,y_18_2,'18-Farsta strand','(18)','green')
plot_Trip('down',x_17_2,y_17_2,'17-Skarpnäck','(17)','green')



plot_Trip('up',x_14_1,y_14_1,'14-Mörby Centrum','(14)','red')
plot_Trip('up',x_13_1,y_13_1,'13-Ropsten','(13)','red')
plot_Trip('down',x_14_2,y_14_2,'14-Fruängen','(14)','red')
plot_Trip('down',x_13_2,y_13_2,'13-Norsborg','(13)','red')


plot_Trip('up',x_11,y_11,'11-Hjulsta','(11)','blue')
plot_Trip('up',x_10,y_10,'10-Akalla','(10)','blue')
plot_Trip('down',x_10_5,y_10_5,'10-11-Kungsträdgården','(10,11)','blue')



plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.autoscale(enable=True) 


plt.savefig("MetroArrivals.png", bbox_inches='tight',dpi = 100)

plt.show()

