from django.shortcuts import render,redirect
from App_vehicle.models import signup,vehicles
import datetime 
from joblib import load
from django.core.mail import BadHeaderError, send_mail



# Create your views here.
def Home(request):
	return render(request,'Landing page.html')


def get_years(d):
  input_datetime = datetime.datetime.fromisoformat(d)
  current_datetime = datetime.datetime.now()
  difference_in_years = (current_datetime - input_datetime).days // 365

  return difference_in_years

def get_days(d):
  date_obj = datetime.datetime.strptime(d, "%Y-%m-%d")
  current_date = datetime.datetime.now()
  difference = current_date -  date_obj 
  return difference.days

def date_after_n_days(date, n):
	date=datetime.datetime.strptime(date, "%Y-%m-%d")
	new_date = date + datetime.timedelta(days=n)
	return new_date.date()	



def Sign_in(request):
	if request.method=="POST":
		mail=request.POST['Email']
		passwd=request.POST['passwd']

		allaccounts=signup.objects.all()
		for i in allaccounts:
			if(i.email==mail):
				if(i.password!=passwd):
					msg="Wrong password"
					return render(request,'Sign In Page.html',{'passwdmsg':msg})
				key=i.id
				return Dashboard(request,key)

		msg="Your Email is Not registered"
		return render(request,'Sign In Page.html',{'passwdmsg':msg})		

	return render(request,'Sign In Page.html')





def Sign_up(request):
	if request.method=="POST":
		user=request.POST['Username']
		mail=request.POST['email']
		passwd=request.POST['passwd']
		passwd2=request.POST['passwd2']

		if(passwd!=passwd2):
			msg="Password not matched"
			return render(request,'Sign Up Page.html',{'passwdmsg':msg})
		else:
			data=signup(name=user,email=mail,password=passwd)
			allaccounts=signup.objects.all()
			for i in allaccounts:
				if(i.email==mail):
					msg="This email already registered"
					return render(request,'Sign Up Page.html',{'passwdmsg':msg})

			data.save()
			msg="SignUp Successfull"
			return render(request,'Sign Up Page.html',{'savemsg':msg})
			
				
			

	return render(request,'Sign Up Page.html')

def Dashboard(request,key):
	user=signup.objects.get(pk=key)
	user=user.name

	veh=vehicles.objects.filter(uid=key)
	count=0
	for i in veh:
		count=count+1
	if count==0:
		overview="You had not registered any vehicle yet "
	else:
		overview="Total "+str(count)+ " Vehicle registered"
	return render(request,'User Dashboard.html',{"USER":user,"Vehicles_count":count,"overview":overview,"KEY":key})

def Add_Entry(request,vid):
	return render(request,"Add entry.html",{"vid":vid})


def Add_Entry(request,vid):
	return render(request,"Add entry.html",{"vid":vid})


def All_Entry(request,vid):
	count=2;
	alldata=vehicles.objects.filter(uid=vid)

	return render(request,"All Entry.html",{'alldata':alldata, 'Sno':count})

def delete_entry(request,vnos):
	data=vehicles.objects.get(pk=vnos)
	key=data.uid
	data.delete()
	return redirect(All_Entry,key)



def Result(request,vid):
	vno=request.POST["V_NO"]

	check=vehicles.objects.filter(uid=vid)
	for i in check:
		if i.vno==vno:
			print("already registered this vehicle")
			return redirect(Add_Entry,vid)



	dop=request.POST["purchase_date"]
	dop_y=get_years(dop)

	rep=request.POST["service_date"]
	rep_d=get_days(rep)
	colant=request.POST["colant"]

	walk=request.POST["walk"]
	Travelwalk=request.POST["Travelwalk"]

	day= (18000-int(walk))//int(Travelwalk)

	newDate=date_after_n_days(rep,day)

	brake=request.POST["brakes"]
	tyre=request.POST["tyre"]
	physical=request.POST.get("physical")

	model= load('MODEL_OIL_RISK.joblib')
	y=model.predict([[dop_y,walk]])
	if y[0]==0:
		y='Very Good'
	elif y[0]==1:
		y='Good'
	elif y[0]==2:
		y='Modrate'
	elif y[0]==3:
		y='Need Action'
	else:
		y='Out of Service'


	pollution="NONE"

	turbo_charger=request.POST["charger"]
	if turbo_charger!=0:
		pollution="Normal"
	else :
		pollution="Your Engine Producing Pollution yet" 

	#-------

	data=vehicles(uid=vid,vno=vno,yop=dop_y,engine_oil=y,repaird=rep_d,brake=brake,tyre=tyre,physical=physical)
	data.save()
	print("DATA SAVED Successfully")
	usermail=signup.objects.get(pk=vid)
	mail=usermail.email
	print(mail)
	subject = "Vehicle Health Check" 
	message = "Dear Customer,\n"+ "Your Vehicle "+ vno+" \nthe overall status of your Vehicle is "+ y+"\n This Vehicle Should be Monitored By mechanic Before "+str(newDate)
	recipient_list = [mail]
	send_mail(subject, message,"shivamrahul2002@gmail.com", recipient_list, fail_silently=True) 

	return render(request,"Result.html",{'vid':vid,'engine_oil':y,"Pollution":pollution,"brake":brake,"tyre":tyre,"physical":physical,"NewDate":str(newDate)})
