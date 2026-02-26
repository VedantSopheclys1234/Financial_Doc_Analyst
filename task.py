## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import FinancialDocumentTool

## Verification of Document Task
verification = Task(
    description=(
        "Verify whether the document located at {file_path} is a valid financial document.\n"
        "Check for presence of structured financial statements such as:\n"
        "- Income Statement\n"
        "- Balance Sheet\n"
        "- Cash Flow Statement\n"
        "- Financial ratios or tabular numeric data\n\n"
        "If the document lacks financial characteristics, clearly state why."
    ),
    expected_output=(
        "Provide a structured verification report:\n"
        "1. Is this a financial document? (Yes/No)\n"
        "2. Evidence found in the document\n"
        "3. Confidence level (Low/Medium/High)\n"
    ),
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)
## Creating a task to help solve user's query
analyze_financial_document = Task(
    description=(
        "Analyze the financial document located at {file_path} "
        "and answer the user's query: {query}.\n\n"
        "Instructions:\n"
        "- Base conclusions strictly on document data.\n"
        "- Do NOT fabricate numbers or URLs.\n"
        "- If information is missing, clearly state assumptions.\n"
        "- Extract relevant financial metrics before analysis.\n"
    ),
    expected_output=(
        "Provide structured financial analysis:\n"
        "1. Summary of Key Financial Metrics\n"
        "2. Revenue, Profitability, and Cash Flow Insights\n"
        "3. Strengths Identified\n"
        "4. Weaknesses Identified\n"
        "5. Direct Answer to User Query\n"
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description=(
        "Based strictly on verified financial data from {file_path}, "
        "generate balanced investment insights addressing: {query}.\n\n"
        "Instructions:\n"
        "- Provide evidence-based recommendations.\n"
        "- Discuss both upside and downside scenarios.\n"
        "- Avoid speculative or unsupported claims.\n"
    ),
    expected_output=(
        "Provide investment analysis in the following format:\n"
        "1. Investment Outlook (Positive/Neutral/Negative)\n"
        "2. Supporting Financial Evidence\n"
        "3. Key Growth Drivers\n"
        "4. Potential Risks\n"
        "5. Recommendation (Buy/Hold/Sell with reasoning)\n"
    ),
    agent=investment_advisor,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)


## Creating a risk assessment task
risk_assessment = Task(
    description=(
        "Assess financial and operational risks using data from {file_path}.\n\n"
        "Instructions:\n"
        "- Identify measurable risk factors.\n"
        "- Classify risks as Low, Medium, or High.\n"
        "- Provide reasoning based on financial indicators.\n"
        "- Avoid exaggeration or speculation.\n"
    ),
    expected_output=(
        "Provide structured risk assessment:\n"
        "1. Identified Risks\n"
        "2. Risk Classification (Low/Medium/High)\n"
        "3. Financial Indicators Supporting Classification\n"
        "4. Suggested Mitigation Strategies\n"
    ),
    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

    
