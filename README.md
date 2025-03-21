PubMed CLI Tool
📖 A command-line interface (CLI) tool that fetches research papers from PubMed, filters non-academic authors, and exports the results to a CSV file.

📌 Features
✅ Fetch research papers using the PubMed API
✅ Supports full query syntax for flexible searches
✅ Filters non-academic authors and company affiliations
✅ Saves results to a CSV file with:

• PubMed ID
• Title
• Publication Date
• Non-Academic Authors
• Company Affiliations
• Corresponding Author Email
✅ Supports command-line options:
• -h or --help: Show usage instructions
• -d or --debug: Print debug information
• -f or --file: Specify the output CSV file

🛠 Installation & Setup
1️⃣ Install Python & Poetry
Make sure you have Python 3.12+ installed. Then, install Poetry:

sh
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

2️⃣ Clone the Repository
sh
git clone https://github.com/YOUR_GITHUB_USERNAME/pubmed-cli.git
cd pubmed-cli

3️⃣ Install Dependencies
sh
poetry install

🚀 Usage
Run the CLI
sh
poetry run get-papers-list "cancer research" -f results.csv

Command-line Options
sh
poetry run get-papers-list -h   # Show help
poetry run get-papers-list "machine learning" -f output.csv  # Save results
poetry run get-papers-list "diabetes treatment" -d  # Debug mode

🧰 Tools & Libraries Used
• PubMed API → Fetches research papers
• Python 3.12+ → Programming language
• Poetry → Dependency management
• Requests → Handles API calls
• Pandas → Processes and exports data
• Argparse → Handles command-line arguments

🗂️ Code Orgsnisation
pubmed_cli/
│── pubmed_cli/
│   ├── cli.py         # Main CLI logic
│   ├── pubmed.py      # Functions for API calls and processing
│── pyproject.toml     # Poetry configuration
│── README.md          # Documentation


🔗 References
PubMed API Docs: https://www.ncbi.nlm.nih.gov/home/develop/api/
Poetry Docs: https://python-poetry.org/docs/

📜 License
This project is open-source under the MIT License.

📌 Acknowledgment
This project was developed with guidance from ChatGPT (GPT-4) for structuring the CLI tool, debugging, and ensuring best practices in Python development.