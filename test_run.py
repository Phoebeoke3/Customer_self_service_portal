#!/usr/bin/env python
"""Test script to run the Flask app and show output"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("=" * 50)
    print("Starting SwissAxa Portal...")
    print("=" * 50)
    
    # Import and run
    from app import app
    
    print("\nFlask app imported successfully!")
    print(f"App name: {app.name}")
    print(f"Debug mode: {app.debug}")
    print(f"Host: 127.0.0.1")
    print(f"Port: 5000")
    print("\n" + "=" * 50)
    print("Server starting...")
    print("Access the portal at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

