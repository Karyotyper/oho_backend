from email.mime.text import MIMEText

import pyotp
from flask import Flask, request, json, Response, Blueprint, g, session, jsonify
from marshmallow import ValidationError

from models import db
from models.prompt import prompt_schema, prompt
from models.user_simpleton import user_simpleton, user_simpleton_schema

from flask_mail import Mail, Message

app = Flask(__name__)
user_api = Blueprint('user_api', __name__)
user_schema = user_simpleton_schema()

mail = Mail(app)


def send_email(otp, receiver):
    import smtplib

    try:
        # creates SMTP session
        s = smtplib.SMTP("smtp.gmail.com", 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login("ohopilot2020@gmail.com", "qpastxumemivtgib")

        # message to be sent
        msg = MIMEText('Here is your One Time Password: ' + str(otp))
        msg['Subject'] = 'Oho OTP Verification'
        msg['From'] = "ohopilot2020@gmail.com"
        msg['To'] = receiver
        receiver = receiver

        # sending the mail
        s.sendmail("ohopilot2020@gmail.com", receiver, msg.as_string())

        # terminating the session
        s.quit()
    except:
        return False

    return True


@user_api.route('/login', methods=['GET'])
def login():
    print("SDJS")
    req_data = request.get_json()
    user_in_db = user_simpleton.get_user_by_email(req_data['email'])
    if user_in_db != None:
        otp = pyotp.random_base32()
        session['response'] = otp
        receiver = req_data['email']
        if send_email(otp, receiver):
            return custom_response("OTP Sent", 201)
        else:
            return custom_response("Server Error", 500)
    else:
        return custom_response({'Error': "User not found"}, 500)


@user_api.route('/emailverifyonsignup', methods=['POST'])
def verify_email_on_signup():
    req_data = request.get_json()

    # check if user already exist in the db
    user_in_db = user_simpleton.get_user_by_email(req_data['email'])
    if user_in_db == None:
        otp = pyotp.random_base32()
        session['response'] = otp
        if send_email(otp, req_data['email']):
            return custom_response("OTP Generated", 201)
        else:
            return custom_response('Server Error', 500)
    else:
        return custom_response("User exists", 500)


@user_api.route('/register', methods=['POST'])
def create():
    """
    Create User Function
    """
    req_data = request.get_json()
    print(req_data)
    app.logger.info('even -------------- #' + json.dumps(req_data))

    try:
        data = user_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)

    # check if user already exist in the db
    user_in_db = user_simpleton.get_user_by_email(data.get('email'))

    if user_in_db is None:

        try:
            user = user_simpleton(data)
            user.save()
        except Exception as err:
            return custom_response(err, 500)

        return jsonify(user.to_json())
    else:
        return custom_response("User Already Exists", 500)


@user_api.route('/id', methods=['GET'])
def getUserbyId():
    try:
        user_id = request.get_json()["user_id"]

        user = user_simpleton.get_one_user(user_id)

        return jsonify(user.to_json())
    except Exception as err:
        custom_response(err, 500)


@user_api.route('/update', methods=['POST'])
def update():
    """
    Create User Function
    """
    req_data = request.get_json()
    app.logger.info('even -------------- #' + json.dumps(req_data))

    data = req_data
    print((data))

    # check if user already exist in the db
    user_in_db = user_simpleton.get_one_user(data.get('id'))
    updated_data = None
    if user_in_db is not None:

        try:
            user = user_simpleton(data)
            updated_data = user.update(req_data)

        except Exception as err:
            return custom_response(err, 500)

        return jsonify(user_in_db.to_json())

    else:
        return custom_response("Error while updating the user", 500)


@user_api.route('/prompt/update', methods=['POST'])
def prompt_update():
    try:
        rdata = request.get_json()
        user_id = rdata.get("user_id")

        if user_simpleton.get_one_user(user_id).prompts is not None:
            for item in range(0, len(rdata["prompts"])):
                prompt_id = rdata["prompts"][item].get("prompt_id")
                name = rdata["prompts"][item].get("name")
                user_id = rdata["prompts"][item].get("user_id")

                pm = prompt(name, user_id)
                updated_pm = pm.update(rdata, name, user_id, item, prompt_id)
    except Exception as err:
        custom_response(err, 500)

    return "Prompt updated successfully"


@user_api.route('/prompt/add', methods=['POST'])
def prompt_add():
    try:
        rdata = request.get_json()
        for item in range(0, len(rdata["prompts"])):
            name = rdata["prompts"][item].get("name")
            user_id = rdata["prompts"][item].get("user_id")

            pm = prompt(name, user_id)
            user = user_simpleton.get_one_user(rdata["prompts"][item].get("user_id"))
            user.prompts.append(pm)

            db.session.add(user)
            db.session.add(pm)
            db.session.commit()
    except Exception as err:
        return custom_response(err, 500)

    return "Prompt saved successfully"


@user_api.route('/prompts', methods=['GET'])
def get_prompts():
    try:
        user_id = request.get_json()["user_id"]
        all_prompts = prompt.get_prompts_by_user(user_id)
        return json.dumps([o.dump_prompt() for o in all_prompts])
    except Exception as err:
        custom_response(err, 500)

@user_api.route('/validateOTP', methods=['POST'])
def validateOTP():
    req_data = request.get_json()
    otp = (req_data['otp'])
    st = req_data['type']

    if 'response' in session:
        s = session['response']
        session.pop('response', None)

        if s == otp:
            if st == 'Login':
                return custom_response('Login Authorised Successfully', 200)
            elif st == 'EmailVerifyOnSignup':
                return custom_response('Valid Email for Signup', 200)
        else:
            if st == 'Login':
                return custom_response('Login not successful', 500)
            elif st == 'EmailVerifyOnSignup':
                return custom_response('Email is not valid', 500)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
