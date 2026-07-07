#!/usr/bin/env python
"""Runner script for Flask app"""
import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Now import and run the app
from main import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
