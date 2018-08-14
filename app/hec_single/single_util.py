import os
import subprocess
from distutils.dir_util import copy_tree
from shutil import make_archive
from app.hec_single import get_rain_fall_util
from app.hec_single import model_update_util


def validate_run_id(run_id):
    print(run_id)
    run_id_part_list = run_id.split(':')
    if len(run_id_part_list) == 4:
        return True
    else:
        return False


def read_file(filename):
    with open(filename, 'rb') as f:
        file_data = f.read()
    return file_data


def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)


def save_init_state(db, date, init_data):
    try:
        sql = 'UPDATE tbl_hec_init SET file = {} WHERE date  = \'{}\' '.format(init_data, date)
        db.engine.connect().excute(sql)
    except Exception as e:
        print('save_init_state|Exception:', e)


def get_init_state(db, date):
    try:
        sql = 'select file from tbl_hec_init WHERE date  = \'{}\' '.format(date)
        result = db.engine.connect().excute(sql)
        for init_data in result:
            return init_data
    except Exception as e:
        print('get_init_state|Exception:', e)
        return None


def is_init_state(db, date, init_state_path):
    state_data = get_init_state(db, date)
    if state_data is not None:
        write_file(state_data, init_state_path)
        return False
    else:
        return True


def save_init_state(db, date, init_state_path):
    if os.path.exists(init_state_path):
        state_data = read_file(init_state_path)
        save_init_state(db, date, state_data)


def copy_model_files(run_name, folder_date):
    print("copy_model_files")
    model_path = os.path.join(folder_date, run_name, '2008_2_Events')
    base_model_path = os.path.join('2008_2_Events_Hack')
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    print(model_path)
    copy_tree(base_model_path, model_path)


def copy_distributed_model_files(run_name, folder_date):
    print("copy_model_files")
    model_path = os.path.join(folder_date, run_name, '2008_2_Events')
    base_model_path = os.path.join('2008_2_Events_Distributed')
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    print(model_path)
    copy_tree(base_model_path, model_path)


def generate_rainfall(run_name, run_date, backward=2, forward=3):
    input_path = os.path.join(run_date.strftime("%Y-%m-%d"), run_name, 'input')
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    date = run_date.strftime("%Y-%m-%d")
    time = run_date.strftime("%H:%M:%S")
    get_rain_fall_util.generate_rf_file(input_path, date, time, backward, forward)


def update_model_files(run_name, folder_date, init_state):
    control_file = os.path.join(folder_date, run_name, '2008_2_Events/Control_1.control')
    run_file = os.path.join(folder_date, run_name, '2008_2_Events/2008_2_Events.run')
    gage_file = os.path.join(folder_date, run_name, '2008_2_Events/2008_2_Events.gage')
    rainfall_file = os.path.join(folder_date, run_name, 'input/DailyRain.csv')
    model_update_util.update_model_configs(control_file, run_file, gage_file, rainfall_file, init_state)


def update_model(run_name, folder_date):
    model_path = os.path.join(folder_date, run_name, '2008_2_Events')
    if not os.path.exists(model_path):
        os.makedirs(model_path)
        model_update_util.update_model_script(model_path, '2008_2_Events')


def csv_to_dss(run_name, folder_date):
    model_path = os.path.join(folder_date, run_name, '2008_2_Events')
    dssvue_cmd = 'dssvue/hec-dssvue.sh csv_to_dss_util.py --date {} --run_name {} --model_dir {}' \
        .format(folder_date, run_name, model_path)
    subprocess.call([dssvue_cmd], shell=True)


def validate_run_id(run_id):
    print(run_id)
    run_id_part_list = run_id.split(':')
    if len(run_id_part_list) == 4:
        return True
    else:
        return False


def dss_to_csv(run_name, run_date):
    date_str = run_date.strftime("%Y-%m-%d")
    model_path = os.path.join(date_str, run_name, '2008_2_Events')
    dssvue_cmd = 'dssvue/hec-dssvue.sh dss_to_csv_util.py --date {} --run_name {} --model_dir {}' \
        .format(date_str, run_name, model_path)
    subprocess.call([dssvue_cmd], shell=True)


def convert_dss_to_csv(run_name, run_date):
    model_path = os.path.join(run_date, run_name, '2008_2_Events')
    dssvue_cmd = 'dssvue/hec-dssvue.sh dss_to_csv_util.py --date {} --run_name {} --model_dir {}' \
        .format(run_date, run_name, model_path)
    subprocess.call([dssvue_cmd], shell=True)


def discharge_file_exists(run_name, run_date, output_path_prefix):
    date_str = run_date.strftime("%Y-%m-%d")
    discharge_file = os.path.join(output_path_prefix, date_str, run_name, 'output/DailyDischarge.csv')
    os.path.isfile(discharge_file)


def exists_discharge_file(run_name, run_date, output_path_prefix):
    discharge_file = os.path.join(output_path_prefix, run_date, run_name, 'output/DailyDischarge.csv')
    os.path.isfile(discharge_file)


def copy_input_file_to_output(source,destination):
    copy_tree(source, destination)


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def create_output_zip(zip_file_name, input_file_path, output_file_path):
    output_zip = zip_file_name + '.zip'
    output_zip_abs_path = os.path.join(output_file_path, output_zip)

    # Check whether output.zip is already created.
    if os.path.exists(output_zip_abs_path):
        return output_zip

    # Check whether the output is ready. If ready archive and return the .zip, otherwise return None.
    if os.path.exists(output_file_path):
        make_archive(input_file_path, 'zip', output_file_path)
        return output_zip


def run_model(run_name, run_date):
    model_path = os.path.join('/home/uwcc-admin/udp_150/hec-hms',run_date.strftime("%Y-%m-%d"), run_name, '2008_2_Events')
    # /home/uwcc-admin/udp_150/hec-hms/2018-07-12/hello/2008_2_Events/2008_2_Events.script
    script_file_path = os.path.join(model_path, '2008_2_Events.script')
    os.system('./run_hec.sh {}'.format(script_file_path))


def run_hec_model(run_name, run_date):
    model_path = os.path.join('/home/uwcc-admin/udp_150/hec-hms',run_date, run_name, '2008_2_Events')
    # /home/uwcc-admin/udp_150/hec-hms/2018-07-12/hello/2008_2_Events/2008_2_Events.script
    script_file_path = os.path.join(model_path, '2008_2_Events.script')
    os.system('./run_hec.sh {}'.format(script_file_path))