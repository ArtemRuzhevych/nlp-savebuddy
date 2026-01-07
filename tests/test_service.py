import pytest
from unittest.mock import MagicMock, patch
from app.modules.interpretation.service import InterpretationService
from app.modules.interpretation.schemas import InterpretationContext

@pytest.fixture
def mock_service():
    with patch("app.modules.interpretation.service.pipeline") as mock_pipeline, \
         patch("app.modules.interpretation.service.SentenceTransformer") as mock_embedder:
        
        # Mock QA Pipeline behavior
        mock_qa = MagicMock()
        mock_qa.return_value = {"answer": "mock answer", "score": 0.9}
        mock_pipeline.return_value = mock_qa
        
        # Mock Embeddings
        mock_emb = MagicMock()
        mock_emb.encode.return_value = [[0.1, 0.2]] # Mock tensor
        mock_embedder.return_value = mock_emb
        
        service = InterpretationService()
        return service

def test_intent_parsing(mock_service):
    # Setup specific mock responses for QA
    def qa_side_effect(question, context):
        if "What is the money for?" in question:
            return {"answer": "Travel Buddies", "score": 0.9}
        if "What is the monetary amount to save?" in question:
            return {"answer": "100", "score": 0.9}
        return {"answer": "something", "score": 0.5}

    mock_service.qa_pipeline.side_effect = qa_side_effect

    context = InterpretationContext(
        prompt="Save $100 for Travel Buddies",
        user_groups={"1": "Travel Buddies"}
    )
    
    # Mock matching
    with patch("app.modules.interpretation.service.util.semantic_search") as mock_search:
        # Return a high score match
        mock_search.return_value = [[{"corpus_id": 0, "score": 0.9}]]
        
        result = mock_service.interpret(context)
        
        assert result.intent == "group_saving"
        assert result.data.is_existing_group == True
        assert result.data.group_id == "1"
        assert result.data.group_name == "Travel Buddies"

def test_personal_saving(mock_service):
    # Setup specific mock responses for QA
    def qa_side_effect(question, context):
        if "What is the name of the savings group?" in question:
            return {"answer": "", "score": 0.0}
        if "What is the specific goal for this money?" in question:
            return {"answer": "New Bike", "score": 0.9}
        if "What is the monetary amount to save?" in question:
            return {"answer": "100", "score": 0.9}
        if "What is the currency of the saving?" in question:
             return {"answer": "150 zl", "score": 0.9}
        if "How often should the deposit be made?" in question:
            # The prompt implies "Monday", but QA might extract "every Monday" if it was there.
            # Here we test the extraction logic for implicit ONCE
            return {"answer": "Monday", "score": 0.9}
        if "On which day of the week?" in question:
            return {"answer": "Monday", "score": 0.9}
        return {"answer": "something", "score": 0.5}

    mock_service.qa_pipeline.side_effect = qa_side_effect

    context = InterpretationContext(
        prompt="Save $100 on Monday"
    )
    
    result = mock_service.interpret(context)
    
    assert result.intent == "personal_saving"
    assert result.data.amount == 100.0
    assert result.data.currency == "PLN"
    # "Monday" without "every" should be ONCE
    assert result.data.frequency == "ONCE" 
    assert result.data.day_of_week == "Monday"

def test_recurring_saving(mock_service):
    # Test explicitly recurring
    def qa_side_effect(question, context):
        if "How often should the deposit be made?" in question:
            return {"answer": "every Monday", "score": 0.9}
        if "On which day of the week?" in question:
            return {"answer": "Monday", "score": 0.9}
        return {"answer": "something", "score": 0.5}

    mock_service.qa_pipeline.side_effect = qa_side_effect

    context = InterpretationContext(
        prompt="Save $100 every Monday"
    )
    
    result = mock_service.interpret(context)
    
    assert result.data.frequency == "WEEKLY"
    assert result.data.day_of_week == "Monday"
