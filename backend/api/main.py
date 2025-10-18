"""FastAPI main application"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import Optional
import tempfile
import os

from backend.models.scenario import CustomScenario
from backend.models.session import HelpRequest
from backend.services.scenario_service import get_scenario_service
from backend.services.session_manager import create_session, get_session, end_session
from backend.services.orchestrator import get_orchestrator

# Initialize FastAPI app
app = FastAPI(
    title="Punjabi Language Learning Tool",
    description="AI-powered Punjabi conversation practice",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directories exist
Path("frontend/static/audio").mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Initialize services
scenario_service = get_scenario_service()
orchestrator = get_orchestrator()


@app.get("/")
async def root():
    """Serve the main frontend page"""
    return FileResponse("frontend/index.html")


@app.get("/api/scenarios")
async def list_scenarios():
    """List all curated scenarios"""
    scenarios = scenario_service.list_scenarios()
    return {"scenarios": [s.model_dump() for s in scenarios]}


@app.get("/api/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    """Get a specific scenario by ID"""
    scenario = scenario_service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario.model_dump()


@app.post("/api/scenarios/custom")
async def create_custom_scenario(custom_scenario: CustomScenario):
    """Generate a custom scenario from user prompt"""
    try:
        scenario = scenario_service.generate_custom_scenario(custom_scenario)
        return scenario.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate scenario: {str(e)}")


@app.post("/api/sessions/start")
async def start_session(scenario_id: str = Form(...)):
    """
    Start a new conversation session.
    
    Args:
        scenario_id: ID of the scenario to use
    
    Returns:
        Session info with initial greeting
    """
    # Get scenario
    if scenario_id == "custom":
        raise HTTPException(
            status_code=400,
            detail="Use /api/scenarios/custom first to create custom scenario"
        )
    
    scenario = scenario_service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    # Create session
    session = create_session(scenario)
    
    # Generate initial greeting
    greeting = orchestrator.start_scenario_greeting(
        session,
        audio_output_path=f"frontend/static/audio/{session.session_id}_greeting.mp3"
    )
    
    return {
        "session_id": session.session_id,
        "scenario": scenario.model_dump(),
        "greeting": {
            "transcript": greeting["transcript"].model_dump(),
            "audio_url": f"/static/audio/{Path(greeting['audio_path']).name}"
        }
    }


@app.post("/api/sessions/{session_id}/turn")
async def process_turn(
    session_id: str,
    audio: UploadFile = File(...)
):
    """
    Process a conversation turn: user audio -> AI response.
    
    Args:
        session_id: Session identifier
        audio: User audio file
    
    Returns:
        User transcript and AI response with audio
    """
    # Get session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save uploaded audio to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        content = await audio.read()
        temp_audio.write(content)
        temp_audio_path = temp_audio.name
    
    try:
        # Process turn
        with open(temp_audio_path, "rb") as audio_file:
            result = orchestrator.process_conversation_turn(
                audio_file,
                session,
                audio_output_dir="frontend/static/audio"
            )
        
        # Clean up temp file
        os.unlink(temp_audio_path)
        
        return {
            "user": {
                "transcript": result["user_transcript"].model_dump(),
            },
            "ai": {
                "transcript": result["ai_transcript"].model_dump(),
                "audio_url": f"/static/audio/{Path(result['ai_audio_path']).name}"
            },
            "metrics": session.metrics.model_dump()
        }
    
    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path)
        # Log the full error for debugging
        import traceback
        print(f"ERROR in process_turn: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to process turn: {str(e)}")


@app.post("/api/sessions/{session_id}/help")
async def get_help(
    session_id: str,
    help_request: HelpRequest
):
    """
    Get help response for user query.
    
    Args:
        session_id: Session identifier
        help_request: Help request with query and optional topic
    
    Returns:
        Help response text
    """
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        help_response = orchestrator.get_help_response(
            query=help_request.query,
            session=session,
            topic=help_request.topic
        )
        
        return {
            "response": help_response,
            "context": help_request.context or session.get_recent_context()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get help: {str(e)}")


@app.post("/api/sessions/{session_id}/complete")
async def complete_session(
    session_id: str,
    confidence_rating: Optional[int] = Form(None)
):
    """
    Complete a session and get summary.
    
    Args:
        session_id: Session identifier
        confidence_rating: Optional user confidence rating (1-5)
    
    Returns:
        Session summary with metrics
    """
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        summary = session.complete(confidence_rating=confidence_rating)
        end_session(session_id)
        
        return summary.model_dump()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete session: {str(e)}")


@app.get("/api/sessions/{session_id}/metrics")
async def get_session_metrics(session_id: str):
    """Get current session metrics"""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "metrics": session.metrics.model_dump(),
        "turn_count": len(session.turns),
        "state": session.state.value
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "punjabi-lang-tool"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

