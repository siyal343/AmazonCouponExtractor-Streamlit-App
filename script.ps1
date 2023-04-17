# Install Python using Winget
Write-Host "Installing Python using Winget..."
winget install Python -e

# Check if Python is installed successfully
$pythonCheck = python --version
if ($pythonCheck) {
    Write-Host "Python installed successfully"
} else {
    Write-Host "Python installation failed"
    exit 1
}

# Install required Python packages using pip
Write-Host "Installing Selenium, Pandas, BeautifulSoup4, and Streamlit using pip..."
pip install selenium pandas beautifulsoup4 streamlit

# Install Git and Node using Winget
Write-Host "Installing Git and Node using Winget..."
winget install Git -e
winget install Node.js -e

# Clone the GitHub repository
Write-Host "Cloning the GitHub repository..."
git clone https://github.com/siyal343/AmazonCouponExtractor-Streamlit-App

# Change directory to the cloned folder
Write-Host "Changing directory to the cloned folder..."
cd AmazonCouponExtractor-Streamlit-App

# Run the Python script
Write-Host "Running the Python script..."
streamlit run main.py
