# Install Python using Winget
winget install Python -e

# Check if Python is installed successfully
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "Python installed successfully."
} else {
    Write-Error "Failed to install Python."
    exit 1
}

# Install required Python packages using pip
pip install selenium pandas beautifulsoup4 streamlit

# Install Git and Node using Winget
winget install Git -e
winget install Node.js -e

# Clone the GitHub repository
git clone https://github.com/siyal343/AmazonCouponExtractor-Streamlit-App

# Change directory to the cloned folder
cd AmazonCouponExtractor-Streamlit-App

# Unzip edgedriver_win64.zip
Expand-Archive edgedriver_win64.zip

cd edgedriver_win64
# Add msedgedriver.exe to the PATH
$edgedriverPath = (Get-Location).Path + "\edgedriver_win64\msedgedriver.exe"
$env:PATH += ";$edgedriverPath"

# Run the Streamlit app
streamlit run main.py
