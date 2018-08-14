from data_layer import models
from app.config import create_app, model_hec, UPLOADS_DEFAULT_DEST
from flask_json import JsonError, json_response
from flask import request
import datetime
import os
import ast
from app.hec_single import single_util
from app.hec_single import model_tasks

trig_api, db = create_app(models.db)


# Gathering required input files to run single hec-hms model
@trig_api.route('/hec_hms/single/init-start', methods=['POST'])
def init_hec_hms_single(db):
    print('init_hec_hms_single')
    req_args = request.args.to_dict()
    if 'run-name' not in req_args.keys() or not req_args['run-name']:
        raise JsonError(status_=400, description='run-name is not specified.')
    run_name = request.args.get('run-name', type=str)
    # Model running date default is current date. Folder created for this date.
    if 'run-datetime' not in req_args.keys() or not req_args['run-datetime']:
        raise JsonError(status_=400, description='run-datetime is not specified.')
    run_datetime = datetime.datetime.strptime(request.args.get('run-datetime', type=str), '%Y-%m-%d %H:%M:%S')
    if 'init-state' not in req_args.keys() or not req_args['init-state']:
        init_state_path = os.path.join(UPLOADS_DEFAULT_DEST,
                                    run_datetime.strftime('%Y-%m-%d'),
                                    run_name,
                                    '2008_2_Events/basinStates')
        init_state = single_util.is_init_state(db, run_datetime.strftime('%Y-%m-%d'), init_state_path)
    else:
        init_state = ast.literal_eval(request.args.get('init-state', type=str))
    input_dir_rel_path = os.path.join(run_datetime.strftime('%Y-%m-%d'), run_name, 'input')
    # Check whether the given run-name is already taken for today.
    input_dir_abs_path = os.path.join(UPLOADS_DEFAULT_DEST, input_dir_rel_path)
    if os.path.exists(input_dir_abs_path):
        raise JsonError(status_=400, description='run-name: %s is already taken for run date: %s.' % (run_name, run_datetime))
    req_files = request.files
    if 'rainfall' in req_files:
        model_hec.save(req_files['rainfall'], folder=input_dir_rel_path, name='DailyRain.csv')
        model_tasks.init_single(run_name, run_datetime.strftime('%Y-%m-%d'), init_state)
        run_id = 'HECHMS:single:%s:%s' % (run_datetime.strftime('%Y-%m-%d'), run_name)
        # TODO save run_id in a DB with the status
        return json_response(status_=200, run_id=run_id, description='Successfully saved files.')
    else:
        raise JsonError(status_=400, description='No required input files found, Rainfall file missing in request.')


# Gathering required input files to run distributed hec-hms model
@trig_api.route('/hec_hms/distributed/init-start', methods=['POST'])
def init_hec_hms_distributed(db):
    req_args = request.args.to_dict()
    # check whether run-name is specified and valid.


# Running hec-hms
@trig_api.route('/hec_hms/init-run', methods=['POST'])
def run_hec_hms():
    print('run_hec_hms')
    req_args = request.args.to_dict()
    if 'run-id' not in req_args.keys() or not req_args['run-id']:
        raise JsonError(status_=400, description='run-id is not specified.')
    run_id = request.args.get('run-id', type=str)
    if single_util.validate_run_id(run_id):
        run_date = run_id.split(':')[2]
        run_name = run_id.split(':')[3]
        single_util.run_hec_model(run_name, run_date)
        single_util.convert_dss_to_csv(run_name, run_date)
        init_state_path = os.path.join(UPLOADS_DEFAULT_DEST,
                                    run_date,
                                    run_name,
                                    '2008_2_Events/basinStates')
        single_util.save_init_state(run_date, init_state_path)
        return json_response(status_=200, run_id=run_id, description='Successfully run Hec-Hms.')
    else:
        raise JsonError(status_=400, description='Invalid run id.')


# Create zip file with input files, run configurations and output files
@trig_api.route('/hec_hms/upload', methods=['POST'])
def upload_data():
    print('upload_data')
    req_args = request.args.to_dict()
    if 'run-id' not in req_args.keys() or not req_args['run-id']:
        raise JsonError(status_=400, description='run-id is not specified.')
    if 'zip-file-name' not in req_args.keys() or not req_args['zip-file-name']:
        raise JsonError(status_=400, description='zip-file-name is not specified.')
    run_id = request.args.get('run-id', type=str)
    zip_file_name = request.args.get('zip-file-name', type=str)  # without zip extension.
    if single_util.validate_run_id(run_id):
        run_date = run_id.split(':')[2]
        run_name = run_id.split(':')[3]
        input_file_path = os.path.join(UPLOADS_DEFAULT_DEST, run_date, run_name, 'input')
        output_file_path = os.path.join(UPLOADS_DEFAULT_DEST, run_date, run_name, 'output')
        single_util.copy_input_file_to_output(input_file_path, output_file_path)
        output_zip = single_util.create_output_zip(zip_file_name, output_file_path, output_file_path)
        return single_util.send_from_directory(directory=os.path.join(UPLOADS_DEFAULT_DEST, ' OUTPUT'), filename=output_zip)
    else:
        raise JsonError(status_=400, description='Invalid run id.')


# Upload discharge data to db by reading DailyDischarge.csv
@trig_api.route('/hec_hms/extract', methods=['POST'])
def extract_data():
    print('extract_data')
    req_args = request.args.to_dict()
    if 'run-id' not in req_args.keys() or not req_args['run-id']:
        raise JsonError(status_=400, description='run-id is not specified.')
    if 'force-insert' not in req_args.keys() or not req_args['force-insert']:
        raise JsonError(status_=400, description='force-insert is not specified.')
    force_insert = ast.literal_eval(request.args.get('force-insert', type=str))
    run_id = request.args.get('run-id', type=str)
    if single_util.validate_run_id(run_id):
        run_date = run_id.split(':')[2]
        run_name = run_id.split(':')[3]
        if single_util.exists_discharge_file(run_name, run_date, UPLOADS_DEFAULT_DEST):
            single_util.upload_discharge(run_name, run_date, UPLOADS_DEFAULT_DEST, force_insert)
            return json_response(status_=200, run_id=run_id, description='Successfully uploaded data.')
        else:
            raise JsonError(status_=400, description='No Discharge data found.')
    else:
        raise JsonError(status_=400, description='Invalid run id.')




