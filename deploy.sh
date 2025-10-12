#!/bin/bash
# deploy.sh - Deployment script for ExamNetShield

set -e  # Exit on error

echo "=== ExamNetShield Deployment Script ==="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it and set your SECRET_KEY!"
    echo ""
    read -p "Press enter to continue after editing .env file..."
fi

# Check if running with Docker or manual deployment
echo "Choose deployment method:"
echo "1) Docker (recommended)"
echo "2) Manual (Python virtual environment)"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "=== Docker Deployment ==="
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed!"
        echo "Please install Docker first: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Check if docker-compose is installed
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ docker-compose is not installed!"
        echo "Please install docker-compose first: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    # Build and start containers
    echo "Building Docker image..."
    docker-compose build
    
    echo "Starting containers..."
    docker-compose up -d
    
    echo ""
    echo "✅ ExamNetShield is now running!"
    echo ""
    echo "Creating admin user..."
    docker-compose exec web python create_user.py
    
    echo ""
    echo "🌐 Access the application at: http://localhost:5000"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "=== Manual Deployment ==="
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed!"
        echo "Please install Python 3.8 or higher."
        exit 1
    fi
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create admin user
    echo ""
    echo "Creating admin user..."
    python create_user.py
    
    # Start application
    echo ""
    echo "Starting application..."
    echo "✅ ExamNetShield is now running!"
    echo "🌐 Access the application at: http://localhost:5000"
    echo ""
    echo "Press Ctrl+C to stop the application"
    python app.py
    
else
    echo "Invalid choice!"
    exit 1
fi
