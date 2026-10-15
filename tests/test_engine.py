"""Unit test suite for CampusGemma AI core engine, Side Hustle proposal generator, and OpenTelemetry tracing."""

import pytest
from core.engine import CampusGemmaEngine
from core.telemetry import get_recent_spans, init_telemetry


@pytest.fixture(autouse=True)
def setup_telemetry():
    init_telemetry()


def test_engine_initialization():
    engine = CampusGemmaEngine()
    assert engine is not None
    assert engine.tracer is not None


def test_generate_freelance_proposal():
    engine = CampusGemmaEngine()
    result = engine.generate_freelance_proposal(
        client_brief="Need a FastAPI backend for a local bakery.", hourly_rate_usd=30.0
    )
    assert isinstance(result, dict)
    assert "executive_summary" in result
    assert "milestones" in result
    assert "total_estimated_cost" in result
    assert "scope_boundaries" in result
    assert len(result["milestones"]) >= 2


def test_generate_interview_question():
    engine = CampusGemmaEngine()
    result = engine.generate_interview_question(topic="Distributed Systems", difficulty="Medium")
    assert isinstance(result, dict)
    assert "problem" in result
    assert "concepts" in result
    assert "hint" in result
    assert "solution" in result
    assert len(result["concepts"]) > 0


def test_explain_lab_code():
    engine = CampusGemmaEngine()
    sample_code = "int* ptr = new int(10); delete ptr;"
    result = engine.explain_lab_code(code=sample_code, language="cpp")
    assert isinstance(result, dict)
    assert "summary" in result
    assert "memory_breakdown" in result
    assert "complexity" in result
    assert "pitfalls" in result


def test_evaluate_candidate_answer():
    engine = CampusGemmaEngine()
    result = engine.evaluate_candidate_answer(
        question="Explain CAP Theorem",
        candidate_answer="A distributed system can only guarantee 2 of Consistency, Availability, Partition Tolerance.",
    )
    assert isinstance(result, dict)
    assert "score" in result
    assert "strengths" in result
    assert "critique" in result
    assert "exemplar" in result


def test_opentelemetry_spans_recorded():
    engine = CampusGemmaEngine()
    initial_count = len(get_recent_spans())
    engine.generate_freelance_proposal(client_brief="Build an API")
    spans = get_recent_spans()
    assert len(spans) > initial_count
    last_span = spans[-1]
    assert last_span["name"] == "gemma2.freelance_proposal"
    assert last_span["attributes"]["gen_ai.system"] == "gemma"
    assert "trace_id" in last_span


def test_generate_client_invoice():
    engine = CampusGemmaEngine()
    result = engine.generate_client_invoice(
        client_name="Aman Verma",
        project_title="FastAPI E-Commerce Backend",
        milestone_name="Milestone 1: Database & Auth",
        amount_usd=120.0,
        payment_id="vimalsahani@upi",
    )
    assert isinstance(result, dict)
    assert "invoice_number" in result
    assert "client_name" in result
    assert "line_items" in result
    assert "total_amount_usd" in result
    assert "payment_instructions" in result
    assert "payment_terms" in result
    assert len(result["line_items"]) > 0


def test_invoice_opentelemetry_span():
    engine = CampusGemmaEngine()
    initial_count = len(get_recent_spans())
    engine.generate_client_invoice(
        client_name="Test Client",
        project_title="Test Project",
        milestone_name="Milestone 1",
        amount_usd=50.0,
    )
    spans = get_recent_spans()
    assert len(spans) > initial_count
    last_span = spans[-1]
    assert last_span["name"] == "gemma2.generate_invoice"
    assert last_span["attributes"]["gen_ai.system"] == "gemma"
    assert last_span["attributes"]["side_hustle.type"] == "client_invoice"

