from flask import Flask, jsonify, make_response, request, render_template, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)




