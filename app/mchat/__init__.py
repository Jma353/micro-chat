from flask import Blueprint

# Define a Blueprint for this module (mchat)
mchat = Blueprint('mchat', __name__, url_prefix='/mchat')

# Import all controllers 
from controllers.users_controller import * 