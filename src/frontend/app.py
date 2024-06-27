from flask import Flask, render_template, request, jsonify
import os
from src.ai_modules.visual.visual_analysis import analyze_image
from src.ai_modules.text.text_generation import generate_text
from src.ai_modules.blockchain.blockchain import secure_data
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

import logging
from logging.handlers import RotatingFileHandler
from flasgger import Swagger
from celery import Celery
from flask_caching import Cache
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from prometheus_flask_exporter import PrometheusMetrics
from flask_swagger import swag_from


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Add other configuration variables as needed commit

app = Flask(__name__)
app.config.from_object(Config)

# Load LLM inference endpoints from an env variable or a file
config_list = config_list_from_json(os.environ.get("OAI_CONFIG_LIST"))

# Create AutoGen agents
assistant = AssistantAgent(name="assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent(name="user_proxy")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        image_bytes = file.read()
        prediction = predict(image_bytes)
        return jsonify({'prediction': prediction})

@app.route('/generate-text', methods=['POST'])
def generate_text_route():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'})
    text = generate_text(prompt)
    return jsonify({'text': text})

@app.route('/adios-task', methods=['POST'])
def adios_task():
    data = request.get_json()
    task_description = data.get('task')
    if not task_description:
        return jsonify({'error': 'No task description provided'})

    # Secure the task description using blockchain
    receipt = secure_data(task_description)
    task_id = receipt['logs'][0]['data']

    # Start a multi-agent conversation to solve the secured task
    user_proxy.initiate_chat(assistant, message=task_description)
    response = user_proxy.get_latest_message()
    
    return jsonify({'response': response, 'task_id': task_id})

if __name__ == '__main__':
    app.run(debug=True)

    # Initialize logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/adios.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('A.D.I.O.S startup')

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}, route: {request.url}')
    return jsonify({'error': 'Server Error'}), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error(f'Unhandled Exception: {e}, route: {request.url}')
    return jsonify({'error': 'Unhandled Exception'}), 500

swagger = Swagger(app)

@app.route('/analyze-image', methods=['POST'])
@swag_from('docs/analyze_image.yml')
def analyze_image_swagger():
    # Implementation here

    @app.route('/generate-text', methods=['POST'])
    @swag_from('docs/generate_text.yml')
    def generate_text_route_swagger():
        # Implementation here

        @app.route('/adios-task', methods=['POST'])
        @swag_from('docs/adios_task.yml')
        def adios_task_swagger():
            # Implementation here

            app.config.from_object(config)

celery = Celery(app.name, broker='redis://localhost:6379/0')
celery.conf.update(app.config)

@celery.task
def async_analyze_image(image_bytes):
    return predict(image_bytes)

@app.route('/analyze-image', methods=['POST'])
def analyze_image_async():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        image_bytes = file.read()
        task = async_analyze_image.delay(image_bytes)
        return jsonify({'task_id': task.id})

@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = async_analyze_image.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.result
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)

app.config['CACHE_TYPE'] = 'redis'
cache = Cache(app)

@cache.cached(timeout=60, key_prefix='analyze_image')
def cached_analyze_image(image_bytes):
    return predict(image_bytes)

@app.route('/analyze-image', methods=['POST'])
def analyze_image_cache():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        image_bytes = file.read()
        prediction = cached_analyze_image(image_bytes)
        return jsonify({'prediction': prediction})

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

metrics = PrometheusMetrics(app)

@metrics.summary('request_processing_seconds', 'Time spent processing request')
@app.route('/')
def index():
    return render_template('index.html')

# Add more metrics as needed

