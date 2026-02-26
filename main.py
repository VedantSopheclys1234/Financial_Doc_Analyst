from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document as analyze_financial_task

app = FastAPI(title="Financial Document Analyzer",
            description="AI-powered financial document analysis using CrewAI",  
            version="0.130.0")

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew"""
    try:
        financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_task],
        process=Process.sequential,
        )
    
        result = financial_crew.kickoff(inputs={
            'query': query, 
            'file_path': file_path
            })
        return result
    except Exception as crew_error:
        raise Exception(f"Error running financial crew: {str(crew_error)}")
    
    

@app.get("/", tags=["Health Check"])
async def root()-> dict[str,str]:
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze", tags=["Analysis"])
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
) -> dict[str, Any]:
    """Analyze financial document and provide comprehensive investment recommendations"""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True) # Ensure data directory exists
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        # if query=="" or query is None:
        #     query = "Analyze this financial document for investment insights"
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"    
        # Process the financial document with all analysts
        response = await asyncio.to_thread(
                    run_crew,
                    query=query.strip(),
                    file_path=file_path
                )
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    