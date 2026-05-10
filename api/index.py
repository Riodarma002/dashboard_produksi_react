import sys
import os

# Add the root directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_main import app

# Vercel needs a variable called 'app' or 'handler'
# Since api_main already has 'app', we just expose it.
