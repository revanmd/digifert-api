from fastapi import APIRouter
from src.endpoints import (
	dashboard,
	dashboard_elogsheet,
	dashboard_teman,
	dashboard_shipping,
	elogsheet_area,
	elogsheet_equipment,
	performa_area,
	performa_equipment,
	job_record,
	measurement_performa,
	master_section,
	master_equipment_sap
)


router = APIRouter()
router.include_router(dashboard.router)
router.include_router(dashboard_elogsheet.router)
router.include_router(dashboard_teman.router)
router.include_router(dashboard_shipping.router)
router.include_router(elogsheet_area.router)
router.include_router(elogsheet_equipment.router)
router.include_router(performa_area.router)
router.include_router(performa_equipment.router)
router.include_router(job_record.router)
router.include_router(master_section.router)
router.include_router(master_equipment_sap.router)

#router.include_router(measurement_performa.router)