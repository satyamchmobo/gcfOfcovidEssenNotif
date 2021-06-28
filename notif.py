import requests
from datetime import datetime, timedelta
import pytz
from google.cloud import firestore
import firebase_admin

db = firestore.Client()
firebase_admin.initialize_app()

userRef = db.collection('users')
users = userRef.get()


num_days = 3

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]



header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 


def main(request):
  for user in users:
   
   
   try:
    userinfo=userRef.document(user.id).get().to_dict()
    print(userinfo['email'])
    if(userinfo['notifStatus']=='active'):

      
      uage=userinfo['age']
      # upincode=470003
      upincode=userinfo['PIN']

      URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(upincode, actual_dates[0])
   
      result = requests.get(URL, headers=header)
    else:
      print("notif status for this user is not active")
      continue
   except:
     print("error at rewquest")
    #  result=500
   print(result)
   print("result printed here------------>>>>")
   if result.status_code==200:

     response_json = result.json()
     userRef.document(user.id).set({
                  'availData':response_json["centers"]
                })
     

    #  if len( response_json["centers"])!=0:
     for center in response_json["centers"]:
         for session in center["sessions"]:
             if (session["min_age_limit"] <= uage and session["available_capacity"] > 0 ) :
                 print(f"date: {session['date']}\n{center['name']}\nAddress: {center['address']}\nVaccine type: {session['vaccine']}\ndose1 availability: {session['available_capacity_dose1']}\ndose2 availability: {session['available_capacity_dose2']}\nSlots: {session['slots']}")
                 print("\n")
                # userRef.document(user.id).set({
                #   'availData':response_json["centers"].to_dict()
                # })

             else:

                  print("no slot available right now-----")
    #  else:
    #    print("no center found for this")
   else:
     print('request failed, =--========')   
   
   print("\n") 
   print("\n") 
   print("\n") 
   print("\n") 

  return ' 200 ok '


