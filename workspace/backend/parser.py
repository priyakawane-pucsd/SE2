from backend import Employee,Employee_leves, db
import json 
#fs = open("/home/piu/workspace/LeaveManagement/data.json","r")
with open('/home/piu/se2/workspace/LeaveManagement/data.json') as json_file:
	Employee_leves.query.delete()
	events = json.load(json_file)
	for event in events:
		print(event['leave_type'])
		emp = Employee.query.filter_by(email=event['creater']).first()
		if not emp:
			creater = event['creater']
			emp = Employee(creater)
			db.session.add(emp)
			db.session.commit()
			leave_type = str(event['leave_type'])
			leave_status= str(event['status'])
			leave_creator= str(event['creater'])
			start_time= str(event['start_time'])
			end_time= str(event['end_time'])
			summary= str(event['summary'])
			total_leave_days= int(event['total_leave_days'])
			emp_id = emp
			leave = Employee_leves(leave_type,leave_status,leave_creator,start_time,end_time,summary,total_leave_days,emp_id.id)
			db.session.add(leave)
			db.session.commit()
		else:
			leave_type = str(event['leave_type'])
			leave_status= str(event['status'])
			leave_creator= str(event['creater'])
			start_time= str(event['start_time'])
			end_time= str(event['end_time'])
			summary= str(event['summary'])
			total_leave_days= int(event['total_leave_days'])
			emp_id = emp
			print("emp",emp.id)
			leave = Employee_leves(leave_type,leave_status,leave_creator,start_time,end_time,summary,total_leave_days,emp_id.id)
			db.session.add(leave)
			db.session.commit()


