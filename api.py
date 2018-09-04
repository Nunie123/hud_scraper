import json
from flask import Flask, jsonify
from flask_cors import CORS
from configparser import ConfigParser



# import config file to global object
config = ConfigParser()
config_file = 'config.ini'
config.read(config_file)

# instantiate flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = config.get('flask', 'secret_key')



@app.route('/api/hud_properties', methods=['GET'])
def get_hud_properties():
    with open('listings_data.json') as json_data:
        properties = json.load(json_data)
    return jsonify(properties)

if __name__ == '__main__':
    debug_mode = config.get('flask', 'debug_mode')
    app.run(debug=debug_mode)