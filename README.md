# Risky Regex Retriever
Risky Regex Retriever is a tool for extracting hard-coded regexes from web-related GitHub repositories and checking them for potential **Regular Expression Denial of Service (ReDoS)** attacks. It is written by [William Hedenskog](https://github.com/pilsnerfrajz) and [Joakim Sundman](https://github.com/JoakimSundman) as the final project in DD2525 Language Based Security at KTH. We utilize [vuln-regex-detector](https://github.com/davisjam/vuln-regex-detector) for evil regex validation.

## Requirements
- Ubuntu (tested with 24.04), due to the limitations of `vuln-regex-detector`
- Python (tested with 3.12.3)
- NodeJS (tested with version 18), which will be installed by `setup.sh`
- GitHub account

## Getting Started

### Setup

**1. Clone the repository:**
   
   ```
   git clone https://github.com/pilsnerfrajz/risky-regex-retriever.git
   ```
   
**2. Run the setup script:**

   ```
   ./setup.sh
   ```
   
**3. Create a virtual environment for Python and install all dependencies:**

   ```
   python3 -m venv env/rrr
   ```
   ```
   source env/rrr/bin/activate
   ```
   ```
   pip3 install -r requirements.txt
   ```

**4. Create a GitHub access token:**

   - Go to [New personal access token (classic)](https://github.com/settings/tokens/new)
   - Add a name in the `Note` field, set the expiration date, and press `Generate token`
   - Copy the token which should have the format `ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
   - Append it to _GITHUB_TOKEN=_ in `token.env` at the root of the repo

## Running the Program

Running the program is simple. Just run `python3 src/main.py`. It will now find web-related repositories and look for files containing regex-related functions, e.g., `test()`. It will then extract the regexes and check if they are vulnerable to ReDoS attacks. This will take a couple of hours.

## Output Files

Any potentially vulnerable regexes are placed in `outputs/output_of_validate.txt`. `vuln-regex-detector` produces false positives and the flagged regexes should be double checked. During our run we extracted 13484 regexes across 270 repositories, of which 28 were marked as unsafe. Out of the 28, we found only 7 patterns to be 100% vulnerable. 

`outputs/regex_results.txt` contains the regex function used to filter files in the repositories, along with the names of the matching files. For each match, there is a list of regexes found in that specific file. Searching `outputs/regex_results.txt` for an interesting regex will show you the repositories containing it.
