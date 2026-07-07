#!/bin/bash
# Build and run the project locally

echo "Building Sherlock..."

# Create virtual environment
python -m venv venv

# Activate (this works on Unix-like systems)
source venv/bin/activate

# Install dependencies
pip install -q -r backend/requirements.txt

# Run tests
echo "Running tests..."
pytest test_api.py -v

echo "Setup complete! To start the backend:"
echo "  source venv/bin/activate  # Unix/Mac"
echo "  .\\venv\\Scripts\\activate  # Windows"
echo "  cd backend && python app/main.py"
