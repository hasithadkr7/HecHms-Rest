import datetime
import os
from app.hec_single import single_util
from app.hec_single import upload_discharge_util


def init_hec_hms_models(run_name, run_datetime, init_state, run_model='single'):
    run_date = datetime.datetime.strptime(run_datetime, '%Y-%m-%d %H:%M:%S')
    if run_model == 'single':
        print('single')
        init_single(run_name, run_date, init_state)
    elif run_model == 'distributed':
        print('distributed')


def init_hec_hms_models_rf_gen(run_name, run_date, init_state, backward, forward):
    single_util.copy_model_files(run_name, run_date)
    single_util.generate_rainfall(run_name, run_date, backward, forward)
    single_util.update_model_files(run_name, run_date, init_state)
    single_util.update_model(run_name, run_date)
    single_util.csv_to_dss(run_name, run_date)


def init_single(run_name, folder_date, init_state):
    print('init_single')
    single_util.copy_model_files(run_name, folder_date)
    single_util.update_model_files(run_name, folder_date, init_state)
    single_util.update_model(run_name, folder_date)
    single_util.csv_to_dss(run_name, folder_date)


def run_hec_hms_model(run_name, run_datetime):
    run_date = datetime.datetime.strptime(run_datetime, '%Y-%m-%d %H:%M:%S')
    single_util.run_model(run_name, run_date)


def post_model(run_name, run_datetime):
    run_date = datetime.datetime.strptime(run_datetime, '%Y-%m-%d %H:%M:%S')
    single_util.dss_to_csv(run_name, run_date)


def discharge_file_exists(run_name, run_datetime, path_prefix):
    run_date = datetime.datetime.strptime(run_datetime, '%Y-%m-%d %H:%M:%S')
    discharge_file_exists(run_name, run_date, path_prefix)


def upload_discharge_data_to_db(run_name, run_datetime, path_prefix, force_insert=False):
    run_date = datetime.datetime.strptime(run_datetime, '%Y-%m-%d %H:%M:%S')
    date_str = run_date.strftime("%Y-%m-%d")
    discharge_file = os.path.join(path_prefix, date_str, run_name, 'output/DailyDischarge.csv')
    upload_discharge_util.upload_data_to_db(run_datetime, discharge_file, run_name, force_insert)


def upload_discharge(run_name, run_date, path_prefix, force_insert=False):
    date_str = run_date.strftime("%Y-%m-%d")
    discharge_file = os.path.join(path_prefix, date_str, run_name, 'output/DailyDischarge.csv')
    upload_discharge_util.upload_data_to_db(run_date, discharge_file, run_name, force_insert)
