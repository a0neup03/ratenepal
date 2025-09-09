#!/usr/bin/env python3
"""
Simple server runner for development
"""

import sys
import os
import subprocess

# Add app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def main():
    """Run the FastAPI server"""
    print("🇳🇵 Nepal Government Office Experience Tracker API")
    print("=" * 60)
    print("🚀 Starting development server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🔍 Interactive API: http://localhost:8000/api/redoc")
    print("=" * 60)
    
    try:
        # Change to app directory and run uvicorn
        os.chdir(os.path.join(os.path.dirname(__file__), 'app'))
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()