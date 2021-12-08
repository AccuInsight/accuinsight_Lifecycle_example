####################################################################################################
# Do not modify this code block #
# Import monitoring packages
import traceback
from Accuinsight.Monitoring.deploy.monitoring_deploy import AddDeployLog

# Import flask packages
from flask import Flask, make_response, request
from flask_restplus import Api, Resource, reqparse
from flask_cors import CORS
####################################################################################################

# Custom packages
import joblib
import numpy as np

# Flask app
app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Sample API', doc='/__swagger__', description='A sample API')
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
ns = api.namespace('cancer', description='Breast Cancer classification model')

input_parser = ns.parser()
input_parser.add_argument('input_data', type=str, help='input data', location='form')

req_parser = reqparse.RequestParser()
req_parser.add_argument('input_data', type=str, help='input_data')


# Custom API class
@ns.route("/")
class Cancer(Resource):
    @staticmethod
    @ns.expect(input_parser)
    def post():
        # custom variables and function
        json_arr = request.get_json()

        if not json_arr:
            input_data = input_parser.parse_args().pop('input_data')

            try:
                json_arr = eval(input_data)
            except SyntaxError:
                raise ValueError("Invalid input data: " + input_data)

        # load model from file
        loaded_model = joblib.load("./runs/best-model/joblib_file_name")  # edit joblib_file_name

        # label dictionary
        class_dic = {0: "Ber", 1: "Mal"}

        # make predictions for test data
        y_pred = loaded_model.predict(np.array(json_arr['input_data']))

        result = ["input_data[" + str(i + 1) + "] = '" + str(json_arr['input_data'][i]) + "', result = " + str(class_dic[y_pred[i]])
                  for i in range(len(y_pred))]

        return "\n".join(result)


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
    if log_info['latest_log']['status_code'] != 200: message.append("Breast cancer classification api call failed")

    # Set notifiers
    # deploy_monitor.set_slack('')
    # deploy_monitor.set_mail('')

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
        app.logger.error("Error raised on custom_alarm function\n" + traceback.format_exc())
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
