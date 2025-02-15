import os
from dotenv import load_dotenv
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
import requests
# from airquality import get_data
from weather import main as get_weather 
from . import db
from.models import Myhealth, RiskAssessment 


views = Blueprint('views', __name__)

load_dotenv()
api_key = os.getenv('AIR_QUALITY_API_KEY')


@views.route('/')
def home():
    return render_template("home.html")

@views.route('/weather', methods = ['GET','POST'])
def weather():
    current_weather = None
    weekly_forecast = None
    if request.method == 'POST':
        city = request.form['cityName']
        country = request.form['countryName']
        current_weather, weekly_forecast = get_weather(city, country)
    return render_template("weather.html", current_weather=current_weather, weekly_forecast=weekly_forecast)


@views.route('/riskassessment', methods=['GET', 'POST'])
@login_required
def riskassessment():
    if request.method == 'POST':
        smoke_alarms = request.form.get('smoke_alarms')
        electrical_cords = request.form.get('electrical_cords')
        furniture_secured = request.form.get('furniture_secured')
        emergency_plan = request.form.get('emergency_plan')
        security_measures = request.form.get('security_measures')

        new_risk_assessment = RiskAssessment(
            user_id=current_user.id,
            smoke_alarms=(smoke_alarms == 'yes'),
            electrical_cords=(electrical_cords == 'yes'),
            furniture_secured=(furniture_secured == 'yes'),
            emergency_plan=(emergency_plan == 'yes'),
            security_measures=(security_measures == 'yes')
        )
        db.session.add(new_risk_assessment)
        db.session.commit()

        # Generate feedback messages based on responses
        if smoke_alarms == 'yes':
            flash('Great! Ensure you test your smoke alarms monthly and replace batteries at least once a year.', 'success')
        else:
            flash('It\'s crucial to have working smoke alarms on every level and near sleeping areas. Please install them as soon as possible for your safety.', 'danger')

        if electrical_cords == 'yes':
            flash('Excellent! Continue to regularly inspect your electrical cords and appliances for any signs of wear and tear.', 'success')
        else:
            flash('Replace or repair any frayed or damaged cords and ensure your appliances are in good condition to prevent electrical hazards.', 'danger')

        if furniture_secured == 'yes':
            flash('Well done! Periodically check the stability of heavy furniture and appliances to ensure they remain secure.', 'success')
        else:
            flash('Secure heavy furniture and appliances to prevent them from tipping over. This is especially important if you have children in your home.', 'danger')

        if emergency_plan == 'yes':
            flash('Great! Make sure to review and practice your emergency plan regularly with all household members.', 'success')
        else:
            flash('Create an emergency plan, designate meeting spots, and compile a list of emergency contacts. This will help you and your family be prepared for any emergencies.', 'danger')

        if security_measures == 'yes':
            flash('Good job! Keep doors and windows locked and maintain functional deadbolts and security systems.', 'success')
        else:
            flash('Ensure all doors and windows are properly locked and consider installing deadbolts and security systems to enhance your home\'s security.', 'danger')

        return redirect(url_for('views.riskassessment'))

    return render_template('riskassessment.html')


@views.route('/airquality')
@login_required
def airquality():
    return render_template("airquality.html")

@views.route('/healthtracker')
@login_required
def healthtracker():
    user = current_user
    first_name = user.first_name
    last_name = user.last_name

    health_data = Myhealth.query.filter_by(user_id=user.id).all()
    return render_template("healthtracker.html", first_name=first_name, last_name=last_name, health_data=health_data)

@views.route('/submit_health_data', methods=['POST'])
@login_required
def submit_health_data():
    # Get the form data
    steps = request.form.get('steps')
    sleep_hours = request.form.get('sleep')
    calories = request.form.get('calories')

    # Print the variables to ensure they are being accessed
    print(f'Steps: {steps}, Sleep Hours: {sleep_hours}, Calories: {calories}')

    # Save the data to the database
    new_health_data = Myhealth(
        user_id=current_user.id,
        step_count=steps,
        sleep_count=sleep_hours,
        calories_burned=calories
    )
    db.session.add(new_health_data)
    db.session.commit()

    flash('Health data submitted successfully!', 'success')
    return redirect(url_for('views.healthtracker'))  # Redirect to the health tracking page or another page