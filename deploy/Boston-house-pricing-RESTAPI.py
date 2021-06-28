###################################################################################################
# Do not modify this code block #
# Import monitoring packages
import logging
import traceback
from Accuinsight.Monitoring.deploy.monitoring_deploy import AddDeployLog
# Import flask packages
from flask import Flask, make_response, request
from flask_restplus import Api, Resource
from werkzeug.datastructures import FileStorage
###################################################################################################

# Custom packages
import pandas as pd
from tensorflow.keras.models import model_from_json
# Flask app
app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API', doc='/__swagger__', description='A sample API')
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
ns_conf = api.namespace('conferences', description='Conference operations')

upload_parser = ns_conf.parser()
upload_parser.add_argument('test_data', location='files',
                           type=FileStorage, required=True)
upload_parser.add_argument('test_label', location='files',
                           type=FileStorage, required=True)

# Custom API class
@ns_conf.route("/")
class ConferenceList(Resource):
    @staticmethod
    @ns_conf.expect(upload_parser)
    def post():
        # load model from json
        # print(os.getcwd())
        dir_fd = os.open('runs/best-model/', os.O_RDONLY)
        
        def opener(path, flags):
            return os.open(path, flags, dir_fd=dir_fd)
        
        json_file = open('json_file_name', 'r', opener=opener)  # json_file_name modify
        
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        
        #load weights into new model
        loaded_model.load_weights('runs/best-model/h5_file_name')  # h5_file_name modify
        if upload_parser.parse_args():
            data = upload_parser.parse_args().pop('test_data')
            label = upload_parser.parse_args().pop('test_label')
            test_data = pd.read_csv(data)
            label = pd.read_csv(label)
            
            target = label.loc[0, 'MEDV'].tolist()
            output  = loaded_model.predict(test_data).tolist()[0].pop()
            
            return 'target: ' + str(target) + " predicted value: " + str(output)
        else:
            raise FileNotFoundError


# Custom alarm function
def custom_alarm():
    """
        Function for custom alarm

        provided data:
            log_info: deploy log summary (dictionary format)
                variables = total_call, total_success_call, latest_log {}
                sample =
                {'total_call': 43, 'total_success_call': 41, 'latest_log':
                    {'start_time': datetime.datetime(2020, 6, 12, 16, 20, 43, 743427),
                    'end_time': datetime.datetime(2020, 6, 12, 16, 20, 43, 744315)
                    'duration': 0.001,
                    'url': 'http://localhost:5000/conferences/1211',
                    'request_method': 'GET'
                    'status_code': 200,
                    'response_data': '"input_data = [1211] result = [92.00]"\n'}
                }

        adding notifiers: set_{notifier} function is provided. web push is default notifier
            provided notifier = slack, mail
            sample
                deploy_monitor.set_slack({hook_url})
                deploy_monitor.set_mail({address})

        required return value:
            message: list of message
                add message by appending string data to the list
                sample
                    if {status}: message.append("{message}")
    """

    ####################################################################################################
    # Do not modify this code block #
    # Custom alarm variable initialization
    log_info = deploy_monitor.get_log_info()
    message = list()
    ####################################################################################################

    # Custom alarm sample
    # if log_info['latest_log']['end_time'].hour >= 16: message.append("api called after 16:00")
    # if log_info['latest_log']['duration'] >= 0.01: message.append("api call has long duration time")
    # if log_info['latest_log']['status_code'] != 200: message.append("api call failed")

    # Set notifiers
    # deploy_monitor.set_slack('https://hooks.slack.com/services/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')
    # deploy_monitor.set_mail('hyunjoong@sk.com')

    ####################################################################################################
    # Do not modify this code block #
    # Return message
    return message
    ####################################################################################################


####################################################################################################
# Do not modify this code block #
# Deploy logging object
deploy_monitor = AddDeployLog()


# Request setting for logging
@app.before_request
def before():
    deploy_monitor.set_request(request)


# Logging
@app.after_request
def after(response):
    deploy_monitor.set_response(response)

    try:
        messages = custom_alarm()
    except Exception:
        logging.error("Error raised on custom_alarm function\n" + traceback.format_exc())
        messages = None

    deploy_monitor.add_log(messages)

    return response


# Error handling
@app.errorhandler(404)
def not_found(message): return make_response(message, 404)


@app.errorhandler(400)
def bad_request(message): return make_response(message, 400)


@app.errorhandler(Exception)
def internal_error(arg):
    return make_response(traceback.format_exc(), 500)


# Run api (main)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

####################################################################################################
