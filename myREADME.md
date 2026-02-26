Bug 1: InvestmentTool and RiskTool Methods Missing self
Description

The methods inside InvestmentTool and RiskTool were defined without the self parameter while being placed inside a class.

class InvestmentTool:
    async def analyze_investment_tool(financial_document_data):

When instantiated, this causes:

TypeError: analyze_investment_tool() takes 1 positional argument but 2 were given
Root Cause

Instance methods inside Python classes must include self as the first parameter.
Without it, Python automatically passes the instance as an argument, causing a mismatch.

**Fix Applied**
class InvestmentTool:
    async def analyze_investment_tool(self, financial_document_data):

Same fix applied to:

class RiskTool:
    async def create_risk_assessment_tool(self, financial_document_data):
Impact

Prevents runtime crashes when tools are instantiated and executed by CrewAI.

Bug 2: Inefficient and Unsafe Double-Space Cleanup Logic
Description

The original implementation removed double spaces using manual string slicing:

i = 0
while i < len(processed_data):
    if processed_data[i:i+2] == "  ":
        processed_data = processed_data[:i] + processed_data[i+1:]
Root Cause

This approach:

Has O(n²) time complexity

Mutates string repeatedly (strings are immutable in Python)

Risk of skipping characters

Hard to maintain

**Fix Applied**

Replaced with efficient built-in method:

processed_data = " ".join(financial_document_data.split())
Impact

Improves performance

Makes code readable

Prevents subtle string manipulation bugs

Bug 3: Missing PyPDFLoader Import in FinancialDocumentTool
Description

Pdf was used but never imported or defined:

docs = Pdf(file_path=path).load()

This causes:

NameError: name 'Pdf' is not defined
Root Cause

Incorrect class reference and missing dependency.

**Fix Applied**
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader(path)
docs = loader.load()
Impact

Enables proper PDF loading functionality.

Bug 4: Missing langchain Dependency
Description

PyPDFLoader requires langchain, but requirements.txt only included:

langchain-core==0.1.52

This causes:

ModuleNotFoundError: No module named 'langchain'
Root Cause

langchain-core does not include document loaders.

**Fix Applied**

Added:

langchain==0.1.16
Impact

Prevents module import failure.

Bug 5: Missing uvicorn Dependency
Description

main.py runs:

uvicorn.run(app)

But uvicorn was not listed in requirements.txt.

Error
ModuleNotFoundError: No module named 'uvicorn'
**Fix Applied**

Added:

uvicorn==0.34.0
Impact

Allows FastAPI app to start successfully.

Bug 6: Pydantic Version Conflict
Description

requirements.txt included:

pydantic==1.10.13
pydantic_core==2.8.0
Root Cause

pydantic_core v2 is intended for Pydantic v2, not v1.

This can cause schema validation runtime errors.

**Fix Applied**

Removed:

pydantic_core==2.8.0

Allowed pip to resolve compatible internal dependency.

Impact

Prevents runtime schema validation failures.

Bug 7: Unnecessary Google Cloud Dependency Bloat
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

Fix Applied

Removed unused packages to create a lean dependency graph.

Impact

Faster installation

Lower conflict risk

Cleaner production-grade environment

Bug 8: Environment Variable Dependency Not Documented
Description

SerperDevTool() requires:

SERPER_API_KEY

LLM requires:

GOOGLE_API_KEY=your_key_here

If missing, application fails silently or crashes.

Fix Applied

Documented required environment variables in README.

Impact

Improves deployment reliability and clarity.