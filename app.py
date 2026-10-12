"""CampusGemma AI: Open-Source College & Hostel Tech Interview Companion.

Built for IIIT Bhopal students using Google Gemma 2 and OpenTelemetry GenAI Observability.
"""

import os
import streamlit as st
from core.engine import CampusGemmaEngine
from core.telemetry import get_recent_spans, init_telemetry

# Initialize OpenTelemetry instrumentation
init_telemetry()

st.set_page_config(
    page_title="CampusGemma AI | IIIT Bhopal",
    page_icon="🎓",
    layout="wide",
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        border-left: 4px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=500&auto=format&fit=crop&q=60", caption="IIIT Bhopal Hostel Labs")
    st.title("⚙️ Engine Settings")
    api_key = st.text_input("Groq API Key (Optional)", type="password", help="Leave blank to run in zero-config offline mode")
    mode = st.radio("Inference Provider", ["Groq Cloud (gemma2-9b-it)", "Local Ollama (localhost:11434)", "Built-in Offline Demo"])
    
    use_ollama = "Ollama" in mode
    engine = CampusGemmaEngine(api_key=api_key, use_local_ollama=use_ollama)

    st.markdown("---")
    st.markdown("### 🏆 Hacktoberfest 2026")
    st.markdown("- **Theme Track:** Featured Partner (Google Gemma)")
    st.markdown("- **Observability:** OpenTelemetry GenAI Spans")
    st.markdown("- **Author:** Vimal Sahani (IIIT Bhopal)")

# Header
st.markdown('<div class="main-header">🎓 CampusGemma AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">The Open-Source Technical Interview & Systems Lab Companion for Engineering Students</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "🎯 Technical Interview Drills", 
    "💻 Systems Lab Code Explainer", 
    "📊 OpenTelemetry GenAI Traces"
])

# ----------------- TAB 1: INTERVIEW DRILLS -----------------
with tab1:
    st.subheader("Simulate Real Tech Placements with Google Gemma 2")
    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.selectbox("Interview Domain", [
            "Distributed Systems (Consensus, Raft, CAP Theorem)",
            "Operating Systems & Concurrency (Mutex, Deadlocks, Virtual Memory)",
            "Database Internals (B+ Trees, WAL, Isolation Levels)",
            "High-Throughput Networking (TCP/IP, Epoll, Socket Multiplexing)",
            "Advanced Data Structures (Segment Trees, Disjoint Set Union)"
        ])
    with col2:
        difficulty = st.select_slider("Target Level", options=["Intern", "Junior SDE", "Systems / Senior SDE"], value="Junior SDE")

    if st.button("🚀 Generate Interview Problem", use_container_width=True):
        with st.spinner("Google Gemma 2 generating scenario & tracing OpenTelemetry span..."):
            st.session_state["current_q"] = engine.generate_interview_question(topic=topic, difficulty=difficulty)

    if "current_q" in st.session_state:
        q = st.session_state["current_q"]
        st.info(f"**Scenario:** {q.get('problem')}")
        
        with st.expander("🔍 Key Concepts Evaluated"):
            for c in q.get("concepts", []):
                st.markdown(f"- {c}")

        with st.expander("💡 Stuck? View Hint"):
            st.write(q.get("hint"))

        candidate_ans = st.text_area("Your Solution / Architecture Explanation:", height=150, placeholder="Explain your design, data structures, and edge cases here...")
        
        if st.button("📝 Evaluate My Answer"):
            if not candidate_ans.strip():
                st.warning("Please write an answer before submitting for evaluation.")
            else:
                with st.spinner("Gemma 2 reviewing answer and recording telemetry..."):
                    eval_res = engine.evaluate_candidate_answer(question=q.get("problem", ""), candidate_answer=candidate_ans)
                    st.success(f"**Evaluation Score: {eval_res.get('score', 'N/A')} / 10**")
                    st.markdown(f"**Strengths:** {eval_res.get('strengths')}")
                    st.markdown(f"**Areas to Improve:** {eval_res.get('critique')}")
                    st.info(f"**Exemplar Industry Response:** {eval_res.get('exemplar')}")

# ----------------- TAB 2: LAB CODE EXPLAINER -----------------
with tab2:
    st.subheader("Dissect Complex Lab Assignments & Concurrency Code")
    lang = st.selectbox("Language", ["cpp", "python", "go", "c"])
    sample_code = """// Example: Lock-free ring buffer snippet
#include <atomic>
#include <vector>

template <typename T, size_t Cap>
class RingBuffer {
    std::atomic<size_t> head_{0};
    std::atomic<size_t> tail_{0};
    T buffer_[Cap];
public:
    bool push(const T& val) {
        size_t current_tail = tail_.load(std::memory_order_relaxed);
        if ((current_tail + 1) % Cap == head_.load(std::memory_order_acquire))
            return false;
        buffer_[current_tail] = val;
        tail_.store((current_tail + 1) % Cap, std::memory_order_release);
        return true;
    }
};"""
    code_input = st.text_area("Paste Lab Code Below:", value=sample_code, height=220)

    if st.button("🔬 Analyze Memory & Concurrency Model", use_container_width=True):
        with st.spinner("Analyzing code with Google Gemma 2..."):
            res = engine.explain_lab_code(code=code_input, language=lang)
            st.markdown(f"### 📋 Summary\n{res.get('summary')}")
            st.markdown(f"### 🧠 Memory & Threading State\n{res.get('memory_breakdown')}")
            st.markdown(f"### ⏱️ Complexity\n{res.get('complexity')}")
            st.warning(f"### ⚠️ Potential Deadlocks & Pitfalls\n{res.get('pitfalls')}")

# ----------------- TAB 3: OPENTELEMETRY TRACES -----------------
with tab3:
    st.subheader("Real-Time OpenTelemetry GenAI Observability")
    st.caption("Live trace spans generated by Google Gemma 2 inference requests conforming to OpenTelemetry semantic conventions.")

    spans = get_recent_spans()
    if not spans:
        st.info("No inference spans recorded yet. Generate an interview question or analyze code to inspect live traces.")
    else:
        st.metric("Total Recorded GenAI Spans", len(spans))
        for s in reversed(spans):
            with st.container():
                st.markdown(f"""
                <div class="metric-card">
                    <strong>Span Name:</strong> <code>{s['name']}</code> | 
                    <strong>Duration:</strong> {s['duration_ms']} ms | 
                    <strong>Status:</strong> {s['status']} <br>
                    <small>Trace ID: <code>{s['trace_id']}</code> | Span ID: <code>{s['span_id']}</code></small>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Inspect Span Attributes"):
                    st.json(s["attributes"])
