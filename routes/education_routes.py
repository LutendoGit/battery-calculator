# Routes file for battery education platform
# This file contains all the Flask routes (endpoints) for the educational content
# It handles requests and renders templates

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from functools import wraps

# This is a shared/public version - backend implementation details removed
# The routes reference educational content and API endpoints

education_bp = Blueprint('education', __name__, url_prefix='/learn')

# Route definitions available:
# GET  /learn/fundamentals - Introduction to cells and batteries
# GET  /learn/chemistry - Battery chemistry comparison
# GET  /learn/capacity-dod - Capacity and depth of discharge lesson
# GET  /learn/crate - C-rate explanation
# GET  /learn/cycles-aging - Battery aging and degradation
# GET  /learn/cell-simulator - Interactive cell discharge simulator
# GET  /learn/pack-simulator - Multi-cell pack simulator
# GET  /learn/calculators - Energy and C-rate calculators
# GET  /learn/quiz - Quiz selection page
# GET  /learn/glossary - Searchable battery terminology
# GET  /learn/reference/good-cell - Good cell characteristics
# GET  /learn/reference/bad-cell - Bad cell detection guide
# GET  /learn/reference/pack-issues - Pack imbalance solutions

# See routes/education_routes.py for actual endpoint implementations
