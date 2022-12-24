from collections import defaultdict
from dateutil.parser import parse
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.enums import enum_utility
from src.models.teman_shipping import TemanShipping
from src.models.teman_docking import TemanDocking
from src.models.teman_shipping_report_loading import TemanShippingReportLoading
from src.models.teman_shipping_report_activity import TemanShippingReportActivity
from src.models.teman_shipping_report_equipment import TemanShippingReportEquipment
from src.utils import exception

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from collections import defaultdict
import datetime
import dateutil.relativedelta

from humanfriendly import format_timespan

router = APIRouter(
    prefix='/dashboard_shipping',
    tags=['Dashboard Shipping']
)

@router.get('/shipping_load')
async def shipping_load(
	db: Session = Depends(database.create_session)
):	
	
	now = datetime.datetime.now()
	previous_month = now + dateutil.relativedelta.relativedelta(months=-1)
	previous_month = previous_month.strftime('%Y-%m-%d')

	teman_shipping = db.query(
		TemanShipping
	).filter(
		TemanShipping.load_schedule >= previous_month
	).all()

	shipping_id = [item.shipping_id for item in teman_shipping]

	teman_shipping_report_loading = db.query(
		TemanShippingReportLoading.shipping_id,
		func.sum(TemanShippingReportLoading.loaded_quantity).label("loaded_quantity"),
		func.sum(TemanShippingReportLoading.total_broken).label("total_broken")
	).filter(
		TemanShippingReportLoading.shipping_id.in_(shipping_id)
	).group_by(
		TemanShippingReportLoading.shipping_id
	).all()

	def mapper(sql_result):
		dict_mapper = defaultdict(lambda:0)
		for item in sql_result:
			dict_mapper[item.shipping_id] = {
				'loaded_quantity': item.loaded_quantity,
				'total_broken': item.total_broken
			}

		return dict_mapper

	teman_shipping_report_loading = mapper(teman_shipping_report_loading)

	result = []
	for item in teman_shipping:
		loaded_quantity, total_broken = 0,0

		if teman_shipping_report_loading[item.shipping_id] != 0:
			loaded_quantity = teman_shipping_report_loading[item.shipping_id]['loaded_quantity']
			total_broken = teman_shipping_report_loading[item.shipping_id]['total_broken']

		result.append({
			'shipping_id': item.shipping_id,
			'schedule': item.load_schedule,
			'reserved_quantity': item.load_plan,
			'loaded_quantity': loaded_quantity,
			'total_broken': total_broken,
			'status':item.status
		})

	result.sort(key=lambda x:x['schedule'])
	return result

@router.get('/docking')
async def docking(
	db: Session = Depends(database.create_session),
	aggregate:str = "count",
	result_type:str =  'all'
):	
	result = []

	if result_type == 'dock':
		dock_query = db.query(TemanDocking.dock).distinct()
		dock = [item[0] for item in dock_query]
		temp_result_dayname = []


		for item in dock:
			result_dayname = {
				'senin':0,
				'selasa':0,
				'rabu':0,
				'kamis':0,
				'jumat':0,
				'sabtu':0,
				'minggu':0
			}
			query = f"select STRING_AGG(FORMAT(CAST(check_in_at  AS DATE), 'ddd'), ',') as dayname from teman_docking where dock='{item}' group by DATEPART(week,check_in_at)"
			group_dock = db.execute(query)

			counter = 0
			for dayname in group_dock:
				counter += 1
				result_dayname['minggu'] = result_dayname['minggu'] + dayname.dayname.count('Sun')
				result_dayname['senin'] = result_dayname['senin'] + dayname.dayname.count('Mon')
				result_dayname['selasa'] = result_dayname['selasa'] + dayname.dayname.count('Tue')
				result_dayname['rabu'] = result_dayname['rabu'] + dayname.dayname.count('Wed')
				result_dayname['kamis'] = result_dayname['kamis'] + dayname.dayname.count('Thu')
				result_dayname['jumat'] = result_dayname['jumat'] + dayname.dayname.count('Fri')
				result_dayname['sabtu'] = result_dayname['sabtu'] + dayname.dayname.count('Sat')

			if(aggregate == "average"):
				result_dayname['minggu'] = round((result_dayname['minggu'] / counter),2)
				result_dayname['senin'] = round((result_dayname['senin'] / counter),2)
				result_dayname['selasa'] = round((result_dayname['selasa'] / counter),2)
				result_dayname['rabu'] = round((result_dayname['rabu'] / counter),2)
				result_dayname['kamis'] = round((result_dayname['kamis'] / counter),2)
				result_dayname['jumat'] = round((result_dayname['jumat'] / counter),2)
				result_dayname['sabtu'] = round((result_dayname['sabtu'] / counter),2)

			temp_result_dayname.append(result_dayname)

		
		for i,item in enumerate(dock):
			result.append({
				'dock_name': item,
				'statistics': temp_result_dayname[i]
			})
	else:
		result_dayname = {
			'senin':0,
			'selasa':0,
			'rabu':0,
			'kamis':0,
			'jumat':0,
			'sabtu':0,
			'minggu':0
		}
		query = f"select STRING_AGG(FORMAT(CAST(check_in_at  AS DATE), 'ddd'), ',') as dayname from teman_docking group by DATEPART(week,check_in_at)"
		group_dock = db.execute(query)

		counter = 0
		for dayname in group_dock:
			counter += 1
			result_dayname['minggu'] = result_dayname['minggu'] + dayname.dayname.count('Sun')
			result_dayname['senin'] = result_dayname['senin'] + dayname.dayname.count('Mon')
			result_dayname['selasa'] = result_dayname['selasa'] + dayname.dayname.count('Tue')
			result_dayname['rabu'] = result_dayname['rabu'] + dayname.dayname.count('Wed')
			result_dayname['kamis'] = result_dayname['kamis'] + dayname.dayname.count('Thu')
			result_dayname['jumat'] = result_dayname['jumat'] + dayname.dayname.count('Fri')
			result_dayname['sabtu'] = result_dayname['sabtu'] + dayname.dayname.count('Sat')

		if(aggregate == "average"):
			result_dayname['minggu'] = round((result_dayname['minggu'] / counter),2)
			result_dayname['senin'] = round((result_dayname['senin'] / counter),2)
			result_dayname['selasa'] = round((result_dayname['selasa'] / counter),2)
			result_dayname['rabu'] = round((result_dayname['rabu'] / counter),2)
			result_dayname['kamis'] = round((result_dayname['kamis'] / counter),2)
			result_dayname['jumat'] = round((result_dayname['jumat'] / counter),2)
			result_dayname['sabtu'] = round((result_dayname['sabtu'] / counter),2)

		result.append({
			'dock_name': 'all',
			'statistics': result_dayname
		})

	return result



@router.get('/docking_load')
async def docking_load(
	db: Session = Depends(database.create_session),
):	
	group_loading = db.query(
		TemanShippingReportLoading.date,
		func.count(TemanShippingReportLoading.id).label("value")
	).group_by(
		TemanShippingReportLoading.date
	).order_by(
		TemanShippingReportLoading.date
	).all()


	return group_loading
	
@router.get('/docking_time')
async def docking_time(
	db: Session = Depends(database.create_session),
):	
	query = db.execute(f"select dock, STRING_AGG(FORMAT(CAST(check_in_at  AS DATE), 'yyyy-MM-dd hh:mm:ss'), ',') as check_in, STRING_AGG(FORMAT(CAST(check_out_at  AS DATE), 'yyyy-MM-dd hh:mm:ss'), ',') as check_out from teman_docking where check_out_at is not NULL group by dock")

	dock = []
	time_delta = []
	time_average = []
	time_max = []
	time_min = []

	minute_average = []
	minute_min = []
	minute_max = []

	for item in query:

		time_dock = []
		dock.append(item.dock)

		list_in_time = item.check_in.split(',')
		list_out_time = item.check_out.split(',')
		

		for i,temp in enumerate(list_in_time):
			in_time = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
			out_time = datetime.datetime.strptime(list_out_time[i], "%Y-%m-%d %H:%M:%S")

			delta = (out_time - in_time).total_seconds()

			if delta > 0 :
				time_dock.append(delta)
		time_delta.append(time_dock)

	for i,item in enumerate(dock):
		minute_max.append(max(time_delta[i]) / 60)
		minute_min.append(min(time_delta[i]) / 60)

		average = (sum(time_delta[i]) / len(time_delta[i]))
		minute_average.append(average)

		time_min.append(format_timespan(datetime.timedelta(seconds=min(time_delta[i]))))
		time_max.append(format_timespan(datetime.timedelta(seconds=max(time_delta[i]))))
		time_average.append(format_timespan(datetime.timedelta(seconds=average)))

	result = []

	for i,item in enumerate(dock):
		result.append({
			'dock': item,
			'max_time': time_max[i],
			'min_time': time_min[i],
			'average_time': time_average[i],
			'minute_max': minute_max[i],
			'minute_min': minute_min[i],
			'minute_average': minute_average[i]

		})
	return result 

	
@router.get('/docking_history')
async def docking_time(
	db: Session = Depends(database.create_session),
):
	now = datetime.datetime.now()
	previous_month = now + dateutil.relativedelta.relativedelta(months=-1)
	previous_month = previous_month.strftime('%Y-%m-%d')

	dock_query = db.query(TemanDocking.dock).distinct()
	dock = [item[0] for item in dock_query]

	r_docking_history = []
	for item in dock:
		q_docking_history = db.query(
			TemanDocking
		).filter(
			TemanDocking.check_in_at >= previous_month
		).order_by(
			TemanDocking.check_in_at.desc()
		).all()

		t_docking_history = []
		for docking_item in q_docking_history:

			

			if docking_item.check_out_at is not None:
				t_docking_history.append({
					'time': docking_item.check_out_at,
					'status': 'check-out',
					'ship': docking_item.ship.lower().title()
				})
			else:
				t_docking_history.append({
					'time': docking_item.check_in_at,
					'status': 'check-in',
					'ship': docking_item.ship.lower().title()
				})

		t_docking_history.sort(key=lambda x:x['time'], reverse=True)
		r_docking_history.append(t_docking_history)

	result = []

	for i,item in enumerate(dock):
		result.append({
			'dock': item,
			'history': r_docking_history[i]
		})


	return result
