# run_front_server.py

# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# with open('../../features_names.txt', 'r') as f:
# 	feature_names = f.readlines()[0].split()

feature_names = '''
	timestamp full_sq life_sq floor max_floor material build_year num_room 
	kitch_sq state product_type sub_area area_m raion_popul green_zone_part indust_part children_preschool
	preschool_quota preschool_education_centers_raion children_school school_quota school_education_centers_raion 
	school_education_centers_top_20_raion hospital_beds_raion healthcare_centers_raion university_top_20_raion 
	sport_objects_raion additional_education_raion culture_objects_top_25 culture_objects_top_25_raion shopping_centers_raion 
	office_raion thermal_power_plant_raion incineration_raion oil_chemistry_raion radiation_raion railroad_terminal_raion 
	big_market_raion nuclear_reactor_raion detention_facility_raion full_all male_f female_f young_all young_male young_female 
	work_all work_male work_female ekder_all ekder_male ekder_female 0_6_all 0_6_male 0_6_female 7_14_all 7_14_male 7_14_female 
	0_17_all 0_17_male 0_17_female 16_29_all 16_29_male 16_29_female 0_13_all 0_13_male 0_13_female raion_build_count_with_material_info 
	build_count_block build_count_wood build_count_frame build_count_brick build_count_monolith build_count_panel build_count_foam 
	build_count_slag build_count_mix raion_build_count_with_builddate_info build_count_before_1920 build_count_1921-1945 build_count_1946-1970 
	build_count_1971-1995 build_count_after_1995 ID_metro metro_min_avto metro_km_avto metro_min_walk metro_km_walk kindergarten_km 
	school_km park_km green_zone_km industrial_km water_treatment_km cemetery_km incineration_km railroad_station_walk_km 
	railroad_station_walk_min ID_railroad_station_walk railroad_station_avto_km railroad_station_avto_min ID_railroad_station_avto
	public_transport_station_km public_transport_station_min_walk water_km water_1line mkad_km ttk_km sadovoe_km bulvar_ring_km kremlin_km 
	big_road1_km ID_big_road1 big_road1_1line big_road2_km ID_big_road2 railroad_km railroad_1line zd_vokzaly_avto_km ID_railroad_terminal
	bus_terminal_avto_km ID_bus_terminal oil_chemistry_km nuclear_reactor_km radiation_km power_transmission_line_km thermal_power_plant_km 
	ts_km big_market_km market_shop_km fitness_km swim_pool_km ice_rink_km stadium_km basketball_km hospice_morgue_km detention_facility_km 
	public_healthcare_km university_km workplaces_km shopping_centers_km office_km additional_education_km preschool_km big_church_km 
	church_synagogue_km mosque_km theater_km museum_km exhibition_km catering_km ecology green_part_500 prom_part_500 office_count_500 
	office_sqm_500 trc_count_500 trc_sqm_500 cafe_count_500 cafe_sum_500_min_price_avg cafe_sum_500_max_price_avg cafe_avg_price_500 
	cafe_count_500_na_price cafe_count_500_price_500 cafe_count_500_price_1000 cafe_count_500_price_1500 cafe_count_500_price_2500 
	cafe_count_500_price_4000 cafe_count_500_price_high big_church_count_500 church_count_500 mosque_count_500 leisure_count_500 
	sport_count_500 market_count_500 green_part_1000 prom_part_1000 office_count_1000 office_sqm_1000 trc_count_1000 trc_sqm_1000 
	cafe_count_1000 cafe_sum_1000_min_price_avg cafe_sum_1000_max_price_avg cafe_avg_price_1000 cafe_count_1000_na_price cafe_count_1000_price_500 
	cafe_count_1000_price_1000 cafe_count_1000_price_1500 cafe_count_1000_price_2500 cafe_count_1000_price_4000 cafe_count_1000_price_high 
	big_church_count_1000 church_count_1000 mosque_count_1000 leisure_count_1000 sport_count_1000 market_count_1000 green_part_1500 prom_part_1500 
	office_count_1500 office_sqm_1500 trc_count_1500 trc_sqm_1500 cafe_count_1500 cafe_sum_1500_min_price_avg cafe_sum_1500_max_price_avg 
	cafe_avg_price_1500 cafe_count_1500_na_price cafe_count_1500_price_500 cafe_count_1500_price_1000 cafe_count_1500_price_1500 
	cafe_count_1500_price_2500 cafe_count_1500_price_4000 cafe_count_1500_price_high big_church_count_1500 church_count_1500 mosque_count_1500 
	leisure_count_1500 sport_count_1500 market_count_1500 green_part_2000 prom_part_2000 office_count_2000 office_sqm_2000 trc_count_2000 
	trc_sqm_2000 cafe_count_2000 cafe_sum_2000_min_price_avg cafe_sum_2000_max_price_avg cafe_avg_price_2000 cafe_count_2000_na_price 
	cafe_count_2000_price_500 cafe_count_2000_price_1000 cafe_count_2000_price_1500 cafe_count_2000_price_2500 cafe_count_2000_price_4000 
	cafe_count_2000_price_high big_church_count_2000 church_count_2000 mosque_count_2000 leisure_count_2000 sport_count_2000 market_count_2000 
	green_part_3000 prom_part_3000 office_count_3000 office_sqm_3000 trc_count_3000 trc_sqm_3000 cafe_count_3000 cafe_sum_3000_min_price_avg 
	cafe_sum_3000_max_price_avg cafe_avg_price_3000 cafe_count_3000_na_price cafe_count_3000_price_500 cafe_count_3000_price_1000 
	cafe_count_3000_price_1500 cafe_count_3000_price_2500 cafe_count_3000_price_4000 cafe_count_3000_price_high big_church_count_3000 
	church_count_3000 mosque_count_3000 leisure_count_3000 sport_count_3000 market_count_3000 green_part_5000 prom_part_5000 office_count_5000 
	office_sqm_5000 trc_count_5000 trc_sqm_5000 cafe_count_5000 cafe_sum_5000_min_price_avg cafe_sum_5000_max_price_avg cafe_avg_price_5000 
	cafe_count_5000_na_price cafe_count_5000_price_500 cafe_count_5000_price_1000 cafe_count_5000_price_1500 cafe_count_5000_price_2500 
	cafe_count_5000_price_4000 cafe_count_5000_price_high big_church_count_5000 church_count_5000 mosque_count_5000 leisure_count_5000 
	sport_count_5000 market_count_5000
				'''
feature_names=feature_names.split()
	
# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)

modelpath = "/app/app/models/xgboost_pipeline.dill"
load_model(modelpath)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	logger.info('predict method entered!')
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		logger.info('flask.request.method == "POST": True')
		d = {}
		request_json = flask.request.get_json()
		for feat in feature_names:
			if request_json[feat]:
				d[feat] = request_json[feat]
			else:
				d[feat] = None	

		logger.info(f'{dt} Data received')
		try:
			logger.info('trying model predicting!')
			preds = model.predict(pd.DataFrame([d]))
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return flask.jsonify(data)

		data["predictions"] = preds[:, 1][0]
		# indicate that the request was a success
		data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 4140))
	app.run(host='0.0.0.0', debug=True, port=port)
