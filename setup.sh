#!/bin/sh
echo "Cloning vuln-regex-detector..."
git clone https://github.com/davisjam/vuln-regex-detector.git || { echo "Clone failed"; exit 1; }

echo "Changing directory..."
cd vuln-regex-detector

echo "Setting environment variable..."
export VULN_REGEX_DETECTOR_ROOT=$(pwd)

echo "Environment variable is set to ${VULN_REGEX_DETECTOR_ROOT}"

echo "Running configuration script..."
./configure