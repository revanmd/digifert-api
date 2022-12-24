from collections import defaultdict
from dateutil.parser import parse
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.enums import enum_utility
from src.models.teman_booking import TemanBooking
from src.models.teman_quota import TemanQuota
from src.models.teman_tracking import TemanTracking

from src.utils import exception

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from collections import defaultdict
import datetime
import dateutil.relativedelta

router = APIRouter(
    prefix='/dashboard_teman',
    tags=['Dashboard']
)

@router.get('/booking_quota')
async def index(
	db: Session = Depends(database.create_session)
):	
	# Enums 
	# NPK Subsidi , Urea Subsidi 
	now = datetime.datetime.now()
	previous_month = now + dateutil.relativedelta.relativedelta(months=-1)
	previous_month = previous_month.strftime('%Y-%m-%d')

	print(previous_month)

	def mapper(sql_result):
		dict_mapper = defaultdict(lambda:0)
		for item in sql_result:
			dict_mapper[str(item.date)] = item.value

		return dict_mapper

	
	tonase_booking = db.query(
		TemanBooking.date, 
		func.sum(TemanBooking.quantity).label("value")
	).filter(
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	
	tonase_urea_booking = db.query(
		TemanBooking.date,
		func.sum(TemanBooking.quantity).label("value")
	).filter(
		TemanBooking.product == 'NPK Subsidi',
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	tonase_npk_booking = db.query(
		TemanBooking.date,
		func.sum(TemanBooking.quantity).label("value")
	).filter(
		TemanBooking.product == 'Urea Subsidi',
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	tonase_urea_quota = db.query(
		TemanQuota.date,
		func.sum(TemanQuota.quantity).label("value")
	).filter(
		TemanQuota.product == 'NPK Subsidi',
		TemanQuota.date >= previous_month
	).group_by(
		TemanQuota.date
	).all()

	tonase_npk_quota = db.query(
		TemanQuota.date,
		func.sum(TemanQuota.quantity).label("value")
	).filter(
		TemanQuota.product == 'Urea Subsidi',
		TemanQuota.date >= previous_month
	).group_by(
		TemanQuota.date
	).all()

	tonase_quota = db.query(
		TemanQuota.date,
		func.sum(TemanQuota.quantity).label("value")
	).filter(
		TemanQuota.date >= previous_month
	).group_by(
		TemanQuota.date
	).all()

	mapper_tonase_booking = mapper(tonase_booking)
	mapper_tonase_urea_booking = mapper(tonase_urea_booking)
	mapper_tonase_npk_booking = mapper(tonase_npk_booking)
	mapper_tonase_urea_quota = mapper(tonase_urea_quota)
	mapper_tonase_npk_quota = mapper(tonase_npk_quota)

	result = []
	for item in tonase_quota:
		result.append({
			'date': item.date,
			'ton_quota':round(item.value,2),
			'ton_urea_quota':round(mapper_tonase_urea_quota[str(item.date)],2),
			'ton_npk_quota':round(mapper_tonase_npk_quota[str(item.date)],2),
			'ton_booking':round(mapper_tonase_booking[str(item.date)],2),
			'ton_urea_booking':round(mapper_tonase_urea_booking[str(item.date)],2),
			'ton_npk_booking':round(mapper_tonase_npk_booking[str(item.date)],2),
			'ton_sisa': round(item.value - mapper_tonase_booking[str(item.date)],2)

		})

	return result


@router.get('/booking_process')
async def index(
	db: Session = Depends(database.create_session)
):	
	now = datetime.datetime.now()
	previous_month = now + dateutil.relativedelta.relativedelta(months=-1)
	previous_month = previous_month.strftime('%Y-%m-%d')

	print(previous_month)

	def mapper(sql_result):
		dict_mapper = defaultdict(lambda:0)
		for item in sql_result:
			dict_mapper[str(item.date)] = item.value

		return dict_mapper


	booking_all = db.query(
		TemanBooking.date, 
		func.count(TemanBooking.date).label("value")
	).filter(
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	booking_finished = db.query(
		TemanBooking.date, 
		func.count(TemanBooking.date).label("value")
	).filter(
		TemanBooking.status == 'finished',
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	booking_canceled = db.query(
		TemanBooking.date, 
		func.count(TemanBooking.date).label("value")
	).filter(
		TemanBooking.status == 'canceled',
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	booking_expired = db.query(
		TemanBooking.date, 
		func.count(TemanBooking.date).label("value")
	).filter(
		TemanBooking.status == 'expired',
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	mapper_booking_finished = mapper(booking_finished)
	mapper_booking_canceled = mapper(booking_canceled)
	mapper_booking_expired = mapper(booking_expired)



	result = []
	for item in booking_all:

		total_booking = item.value
		total_finished = mapper_booking_finished[str(item.date)]
		total_canceled = mapper_booking_canceled[str(item.date)]
		total_expired = mapper_booking_expired[str(item.date)]
		unfinished = total_booking - (total_finished + total_canceled + total_expired)

		result.append({
			'date': item.date,
			'total_booking': total_booking,
			'total_finished': total_finished,
			'total_canceled': total_canceled,
			'total_expired': total_expired,
			'total_unfinished': unfinished
		})

	return result

@router.get('/booking_process_tonase')
async def index(
	db: Session = Depends(database.create_session)
):	
	now = datetime.datetime.now()
	previous_month = now + dateutil.relativedelta.relativedelta(months=-1)
	previous_month = previous_month.strftime('%Y-%m-%d')

	print(previous_month)

	def mapper(sql_result):
		dict_mapper = defaultdict(lambda:0)
		for item in sql_result:
			dict_mapper[str(item.date)] = item.value

		return dict_mapper


	booking_all = db.query(
		TemanBooking.date, 
		func.sum(TemanBooking.quantity).label("value")
	).filter(
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	booking_finished = db.query(
		TemanBooking.date, 
		func.sum(TemanBooking.quantity).label("value")
	).filter(
		TemanBooking.status == 'finished',
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	booking_canceled = db.query(
		TemanBooking.date, 
		func.sum(TemanBooking.quantity).label("value")
	).filter(
		TemanBooking.status == 'canceled',
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	booking_expired = db.query(
		TemanBooking.date, 
		func.sum(TemanBooking.quantity).label("value")
	).filter(
		TemanBooking.status == 'expired',
		TemanBooking.date >= previous_month
	).group_by(
		TemanBooking.date
	).all()

	mapper_booking_finished = mapper(booking_finished)
	mapper_booking_canceled = mapper(booking_canceled)
	mapper_booking_expired = mapper(booking_expired)



	result = []
	for item in booking_all:

		tonase_booking = item.value
		tonase_finished = mapper_booking_finished[str(item.date)]
		tonase_canceled = mapper_booking_canceled[str(item.date)]
		tonase_expired = mapper_booking_expired[str(item.date)]
		unfinished = tonase_booking - (tonase_finished + tonase_canceled + tonase_expired)

		result.append({
			'date': item.date,
			'tonase_booked': round(tonase_booking,2),
			'tonase_finished': round(tonase_finished,2),
			'tonase_canceled': round(tonase_canceled,2),
			'tonase_expired': round(tonase_expired,2),
			'tonase_unfinished': round(unfinished,2)
		})

	return result


@router.get('/inout_trends')
async def index(
	db: Session = Depends(database.create_session)
):
	now = datetime.datetime.now()
	previous_month = now + dateutil.relativedelta.relativedelta(months=-1)
	previous_month = previous_month.strftime('%Y-%m-%d')

	tracking_all = db.query(
		TemanTracking.check_in_at,
		TemanTracking.check_out_at

	).filter(
		TemanTracking.check_point == 'Pos 1B',
		TemanTracking.check_in_at >= previous_month
	).all()


	time = ["0" + str(i) for i in range(0,10)] + [str(i) for i in range(10,25)]

	count_in = [0 for i in range(25)]
	count_out = [0 for i in range(25)]


	# 2022-12-08T15:23:00
	for item in tracking_all :
		observable_time = item.check_in_at.strftime('%H')

		idx = time.index(observable_time)
		count_in[idx] = count_in[idx] + 1


		observable_time = item.check_out_at.strftime('%H')

		idx = time.index(observable_time)
		count_out[idx] = count_out[idx] + 1

	result = []
	for i,item in enumerate(time):
		result.append({
			'time': item,
			'count_in':count_in[i],
			'count_out': count_out[i]
		})


	return result

@router.get('/truck_position')
async def index(
	db: Session = Depends(database.create_session)
):
	now = datetime.datetime.now()
	previous_month = now + dateutil.relativedelta.relativedelta(months=-1)
	previous_month = previous_month.strftime('%Y-%m-%d')

	tracking_all = db.query(
		TemanTracking.check_point_id,
		TemanTracking.check_point,
		TemanTracking.check_in_at,
		TemanTracking.check_out_at,
		TemanTracking.check_in_position,
		TemanTracking.check_out_position
	).filter(
		TemanTracking.check_in_at >= previous_month
	).all()

	result = []
	for item in tracking_all:

		check_in_position = None
		check_out_position = None

		if item.check_in_position != "":
			check_in_position = item.check_in_position.split(',')
			check_in_position = {
				'lat': check_in_position[0],
				'lng': check_in_position[1]
			}

			result.append({
				'status': 'check-in',
				'time': item.check_in_at,
				'check_point': item.check_point,
				'check_point_id': item.check_point_id,
				'position': check_in_position
			})

		if item.check_out_position != "":
			check_out_position = item.check_out_position.split(',')
			check_out_position = {
				'lat': check_out_position[0],
				'lng': check_out_position[1]
			}

			result.append({
				'status': 'check-out',
				'time': item.check_out_at,
				'check_point': item.check_point,
				'check_point_id': item.check_point_id,
				'position': check_out_position
			})

	return result