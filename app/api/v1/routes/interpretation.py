from fastapi import APIRouter, HTTPException
from app.modules.interpretation.schemas import InterpretationContext, InterpretationResult
from app.modules.interpretation.service import InterpretationService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Single instance of service (loads models once)
service = InterpretationService()

@router.post("/interpret", response_model=InterpretationResult)
async def interpret_prompt(context: InterpretationContext):
    logger.info(f"Received prompt: {context.prompt}")
    try:
        result = service.interpret(context)
        return result
    except Exception as e:
        logger.error(f"Error interpreting prompt: {e}")
        raise HTTPException(status_code=500, detail=str(e))
