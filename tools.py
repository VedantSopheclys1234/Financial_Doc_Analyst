## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools.tools.serper_dev_tool import SerperDevTool
from langchain.document_loaders import PyPDFLoader

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool():
    @staticmethod
    def read_data_tool(path=str) -> str:
        
        # Reads and cleans text from a financial PDF document.

        # Args:
        #     path (str): Path to the uploaded PDF file

        # Returns:
        #      str: Cleaned full document text
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found at path: {path}")
        
        try:
            docs = PyPDFLoader(path).load()

            full_report = []

            for page in docs:
                content = page.page_content

                #Clean formatting issues commonly found in financial documents
                cleaned_content = "\n".join(
                    line.strip() for line in content.splitlines() if line.strip()
                )
                full_report.append(cleaned_content)

            return "\n\n".join(full_report)
        
        except Exception as e:
            raise RuntimeError(f"Error processing PDF document: {str(e)}")
       
       
## Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data):
        """
        Performs basic deterministic investment insight extraction
        from financial document text.
        """
        if not financial_document_data:
            return "No financial document data provided for analysis."
        
        #Clean text efficiently
        processed_data = " ".join(financial_document_data.split())

        insight = []
        
        #Simple deterministic rules to extract keywords-based analysis
        if "revenue" in processed_data.lower():
            insight.append("Revenue data detected. Review revenue growth trends.")
        if "profit" in processed_data.lower():
            insight.append("Profit figures found. Analyze profitability ratios.")    
        if "debt" in processed_data.lower():
            insight.append("Debt information present. Assess leverage and solvency.")
        if "cash flow" in processed_data.lower():
            insight.append("Cash flow statements available. Evaluate liquidity position.")
        
        if not insight:
            insight.append("No clear financial metrics detected. Consider manual review.")
        
        return "Investment Insights:\n-" + "\n-".join(insight) 

## Creating Risk Assessment Tool
class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data):        
        """
        Performs simple deterministic risk classification
        based on document content.
        """
        if not financial_document_data:
            return "No financial document data provided for risk assessment."
        
        text = financial_document_data.lower()

        risks = []

        if "decline" in text or "loss" in text:
            risks.append("Financial performance decline detected. Potential risk of continued losses.")
        if "high debt" in text or "liabilities exceed assets" in text:
            risks.append("High debt levels identified. Risk of insolvency.")
        if "volatile" in text or "uncertain" in text:
            risks.append("Volatility mentioned. Market risk may be elevated.")
        if not risks:
            risks.append("No explicit risk indicators found. However, absence of evidence is not evidence of absence.")

        return "Risk assessment:n-" + "\n-".join(risks)