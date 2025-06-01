#!/bin/sh

echo "Installing npm..."
sudo snap install node --channel=23/stable --classic || { echo "Install failed"; exit 1; }

echo "Cloning vuln-regex-detector..."
git clone https://github.com/davisjam/vuln-regex-detector.git

echo "Changing directory..."
cd vuln-regex-detector || { exit 1; }

echo "Replacing invalid directory 'src/cache/client' with 'src/cache/client/npm' in 'configure'..."
sed -i 's|src/cache/client/|src/cache/client/npm/|g' configure || { echo "Replacement failed"; exit 1; }

echo "Setting environment variable..."
export VULN_REGEX_DETECTOR_ROOT=$(pwd)
echo "Environment variable is set to ${VULN_REGEX_DETECTOR_ROOT}"

echo "Running configuration script..."
./configure

echo "Creating output directory..."
mkdir outputs

echo "\nCreate a virtual environment and install dependencies with:"
echo "    python3 -m venv env/rrr"
echo "    source env/rrr/bin/activate"
echo "    pip3 install -r requirements.txt"

echo "Run scanner with:"
echo "    python3 src/main.py"
