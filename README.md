# Financial Document Analyzer - Debug Assignment

## Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## Getting Started

### Install Required Libraries
```sh
pip install -r requirements.txt
```

### Sample Document
The system analyzes financial documents like Tesla's Q2 2025 financial update.

**To add Tesla's financial document:**
1. Download the Tesla Q2 2025 update from: https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
2. Save it as `data/sample.pdf` in the project directory
3. Or upload any financial PDF through the API endpoint

**Note:** Current `data/sample.pdf` is a placeholder - replace with actual Tesla financial document for proper testing.

# You're All Not Set!
🐛 **Debug Mode Activated!** The project has bugs waiting to be squashed - your mission is to fix them and bring it to life.

## Debugging Instructions

1. **Identify the Bug**: Carefully read the code in each file and understand the expected behavior. There is a bug in each line of code. So be careful.
2. **Fix the Bug**: Implement the necessary changes to fix the bug.
3. **Test the Fix**: Run the project and verify that the bug is resolved.
4. **Repeat**: Continue this process until all bugs are fixed.

## Expected Features
- Upload financial documents (PDF format)
- AI-powered financial analysis
- Investment recommendations
- Risk assessment
- Market insights

# Code Fixed 

## Bug 1: InvestmentTool and RiskTool Methods Missing self
Description

The methods inside InvestmentTool and RiskTool were defined without the self parameter while being placed inside a class.
```sh
class InvestmentTool:
    async def analyze_investment_tool(financial_document_data):
```
When instantiated, this causes:

TypeError: analyze_investment_tool() takes 1 positional argument but 2 were given
Root Cause

Instance methods inside Python classes must include self as the first parameter.
Without it, Python automatically passes the instance as an argument, causing a mismatch.

**Fix Applied**
class InvestmentTool:
    async def analyze_investment_tool(self, financial_document_data):

Same fix applied to:
```sh
class RiskTool:
    async def create_risk_assessment_tool(self, financial_document_data):
```
Impact

Prevents runtime crashes when tools are instantiated and executed by CrewAI.

# Bug 2: Inefficient and Unsafe Double-Space Cleanup Logic
Description

The original implementation removed double spaces using manual string slicing:
```sh
i = 0
while i < len(processed_data):
    if processed_data[i:i+2] == "  ":
        processed_data = processed_data[:i] + processed_data[i+1:]
```
Root Cause

This approach:

Has O(n²) time complexity

Mutates string repeatedly (strings are immutable in Python)

Risk of skipping characters

Hard to maintain

**Fix Applied**

Replaced with efficient built-in method:
```sh
processed_data = " ".join(financial_document_data.split())
```
Impact

Improves performance

Makes code readable

Prevents subtle string manipulation bugs


# Bug 3: Missing PyPDFLoader Import in FinancialDocumentTool
Description
```sh
Pdf was used but never imported or defined:

docs = Pdf(file_path=path).load()
```
This causes:
```sh
NameError: name 'Pdf' is not defined
```
Root Cause

Incorrect class reference and missing dependency.

**Fix Applied**
```sh
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader(path)
docs = loader.load()
Impact
```
Enables proper PDF loading functionality.

# Bug 4: Missing langchain Dependency
Description

PyPDFLoader requires langchain, but requirements.txt only included:
```sh
langchain-core==0.1.52
```
This causes:

ModuleNotFoundError: No module named 'langchain'
Root Cause

langchain-core does not include document loaders.

**Fix Applied**

Added:
```sh
langchain==0.1.16
```
Impact

Prevents module import failure.

# Bug 5: Missing uvicorn Dependency
Description
```sh
main.py runs:
uvicorn.run(app)
```
But uvicorn was not listed in requirements.txt.

Error
ModuleNotFoundError: No module named 'uvicorn'
**Fix Applied**

Added:
```sh
uvicorn==0.34.0
```
Impact

Allows FastAPI app to start successfully.

# Bug 6: Pydantic Version Conflict
Description

requirements.txt included:
```sh
pydantic==1.10.13
pydantic_core==2.8.0
```
Root Cause

pydantic_core v2 is intended for Pydantic v2, not v1.

This can cause schema validation runtime errors.

**Fix Applied**

Removed:
```sh
pydantic_core==2.8.0
```
Allowed pip to resolve compatible internal dependency.

Impact

Prevents runtime schema validation failures.

# Bug 7: Unnecessary Google Cloud Dependency Bloat
Description

Multiple unused Google Cloud packages were included:

google-cloud-bigquery

google-cloud-aiplatform

google-cloud-storage

onnxruntime

telemetry packages

Root Cause

Overextended dependency footprint increases:

Install time

Dependency conflicts

Security surface area

**Fix Applied**

Removed unused packages to create a lean dependency graph.

Impact

Faster installation

Lower conflict risk

Cleaner production-grade environment

# Bug 8: Environment Variable Dependency Not Documented
Description

SerperDevTool() requires:
```sh
SERPER_API_KEY
```
LLM requires:
```sh
GOOGLE_API_KEY=your_key_here
```
If missing, application fails silently or crashes.

**Fix Applied**

Documented required environment variables in README.



## Setup Instructions
```sh
git clone <repo>
cd project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Create .env:
```sh
GOOGLE_API_KEY=your_key
SERPER_API_KEY=your_key
```
Run:
```sh
uvicorn main:app --reload
```
🔹 API Example
```sh
POST /analyze
{
  "pdf_path": "data/sample.pdf"
}
```
