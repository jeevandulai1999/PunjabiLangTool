#!/usr/bin/env python3
"""
Punjabi Language Learning Tool - Startup Script

This script starts the FastAPI backend server.
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Check for .env file
env_file = project_root / ".env"
if not env_file.exists():
    print("⚠️  Warning: .env file not found!")
    print("Please create a .env file with your OPENAI_API_KEY")
    print(f"You can copy env.example to .env and edit it.")
    response = input("\nContinue anyway? (y/n): ")
    if response.lower() != 'y':
        sys.exit(1)

# Check for OpenAI API key
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openai_api_key_here":
    print("⚠️  Error: OPENAI_API_KEY not set properly!")
    print("Please set your OpenAI API key in the .env file")
    sys.exit(1)

print("✓ Environment configured")
print("✓ Starting Punjabi Language Learning Tool...")
print(f"\n🌐 Open your browser to: http://localhost:8000")
print("\nPress Ctrl+C to stop the server\n")

# Start the server
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",  # Use import string instead of app object
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "true").lower() == "true"
    )

