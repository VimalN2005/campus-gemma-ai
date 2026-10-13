"""CampusGemma AI: The Zero-Cost Student Side-Hustle & Technical Coaching Studio.

Built for Hacktoberfest 2026 Week 2 ('Side Hustle') using Google Gemma 2 Open Weights
and OpenTelemetry GenAI Observability.
"""

import streamlit as st
from core.engine import CampusGemmaEngine
from core.telemetry import get_recent_spans, init_telemetry

init_telemetry()

st.set_page_config(
    page_title="CampusGemma AI | Side Hustle Studio",
    page_icon="💼",
    layout="wide",
)

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
    .profit-badge {
        background-color: #ECFDF5;
        color: #065F46;
        padding: 10px 14px;
        border-radius: 8px;
        border-left: 4px solid #10B981;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=500&auto=format&fit=crop&q=60", caption="IIIT Bhopal Student Side-Hustle Hub")
    st.title("⚙️ Gemma 2 Settings")
    api_key = st.text_input("Groq API Key (Optional)", type="password", help="Leave blank to run in zero-config offline mode")
    mode = st.radio("Inference Provider", ["Groq Cloud (gemma2-9b-it)", "Local Ollama (localhost:11434)", "Built-in Offline Demo"])

    use_ollama = "Ollama" in mode
    engine = CampusGemmaEngine(api_key=api_key, use_local_ollama=use_ollama)

    st.markdown("---")
    st.markdown("### 🏆 Hacktoberfest Week 2")
    st.markdown("- **Theme:** Side Hustle 💼")
    st.markdown("- **Featured Track:** Best Use of Gemma")
    st.markdown("- **Observability:** OpenTelemetry GenAI")
    st.markdown("- **Builder:** Vimal Sahani (IIIT Bhopal)")

st.markdown('<div class="main-header">💼 CampusGemma AI: Student Side-Hustle Studio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Turn messy client messages into high-converting freelance proposals, scope-of-work contracts, and paid technical coaching — with $0.00 API overhead via Google Gemma 2.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="profit-badge">💡 <strong>Why Open Weights Make This Side-Hustle Profitable:</strong> Running Google Gemma 2 locally or on open endpoints keeps client NDA briefs 100% private on your laptop and eliminates $20+/month proprietary API subscriptions—meaning 100% of every student freelance gig stays in your pocket.</div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs([
    "💼 Freelance SOW & Quote Generator",
    "🎯 Paid Mock-Interview Coaching",
    "🔬 Client Code & Security Auditor",
    "📊 OpenTelemetry & Unit Economics",
])

# ----------------- TAB 1: FREELANCE PROPOSAL & SOW GENERATOR -----------------
with tab1:
    st.subheader("Turn Messy WhatsApp / Upwork Client Briefs into Ready-to-Sign Proposals")
    col1, col2 = st.columns([3, 1])
    with col1:
        default_brief = (
            "Hi! I run a local bakery and book cafe in Bhopal. Right now we take custom cake orders over WhatsApp "
            "and track everything in a messy Excel sheet. Half the time we miss delivery slots or forget advance payments. "
            "Can you build us a fast order booking backend with invoice PDFs and an admin dashboard?"
        )
        client_brief = st.text_area("Paste Raw Client Requirement / Message:", value=default_brief, height=130)
    with col2:
        hourly_rate = st.number_input("Your Hourly Rate ($ USD)", min_value=10.0, max_value=150.0, value=25.0, step=5.0)
        st.caption("Automatically calculates milestone quotes & anti-scope-creep clauses.")

    if st.button("⚡ Generate Statement of Work (SOW) & Pricing Quote", use_container_width=True):
        with st.spinner("Google Gemma 2 structuring SOW, milestones, and recording OpenTelemetry trace..."):
            st.session_state["proposal"] = engine.generate_freelance_proposal(
                client_brief=client_brief, hourly_rate_usd=hourly_rate
            )

    if "proposal" in st.session_state:
        prop = st.session_state["proposal"]
        st.success(f"💰 **Estimated Project Quote:** {prop.get('total_estimated_cost')}")
        st.markdown(f"### 📋 Executive Pitch\n{prop.get('executive_summary')}")

        st.markdown("### 🗓️ Engineering Milestones & Deliverable Schedule")
        for m in prop.get("milestones", []):
            st.markdown(f"- ✅ {m}")

        col_a, col_b = st.columns(2)
        with col_a:
            st.info(f"**🛡️ Anti-Scope-Creep Clause:**\n\n{prop.get('scope_boundaries')}")
        with col_b:
            st.warning(f"**🏗️ Recommended Tech Stack:**\n\n{prop.get('tech_stack_recommendation')}")

# ----------------- TAB 2: PAID MOCK INTERVIEW COACHING -----------------
with tab2:
    st.subheader("Campus Placement Coaching Side-Hustle Studio")
    st.caption("Host structured 1-on-1 mock technical interviews for juniors and generate instant grading rubrics.")
    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.selectbox("Interview Domain", [
            "Distributed Systems (Consensus, Raft, CAP Theorem)",
            "Operating Systems & Concurrency (Mutex, Deadlocks, Virtual Memory)",
            "Database Internals (B+ Trees, WAL, Isolation Levels)",
            "High-Throughput Networking (TCP/IP, Epoll, Socket Multiplexing)",
            "Advanced Data Structures (Segment Trees, Disjoint Set Union)",
        ])
    with col2:
        difficulty = st.select_slider("Target Role Level", options=["Intern", "Junior SDE", "Systems / Senior SDE"], value="Junior SDE")

    if st.button("🚀 Generate Interview Problem", use_container_width=True):
        with st.spinner("Google Gemma 2 generating scenario & tracing OpenTelemetry span..."):
            st.session_state["current_q"] = engine.generate_interview_question(topic=topic, difficulty=difficulty)

    if "current_q" in st.session_state:
        q = st.session_state["current_q"]
        st.info(f"**Scenario:** {q.get('problem')}")

        with st.expander("🔍 Key Concepts Evaluated"):
            for c in q.get("concepts", []):
                st.markdown(f"- {c}")

        with st.expander("💡 View Coaching Hint"):
            st.write(q.get("hint"))

        candidate_ans = st.text_area("Candidate Answer / Notes:", height=130, placeholder="Type the student's response to generate a structured grading report...")

        if st.button("📝 Generate Paid Session Scorecard"):
            if not candidate_ans.strip():
                st.warning("Please enter candidate notes before grading.")
            else:
                with st.spinner("Gemma 2 grading response..."):
                    eval_res = engine.evaluate_candidate_answer(question=q.get("problem", ""), candidate_answer=candidate_ans)
                    st.success(f"**Session Score: {eval_res.get('score', 'N/A')} / 10**")
                    st.markdown(f"**Strengths:** {eval_res.get('strengths')}")
                    st.markdown(f"**Actionable Gaps:** {eval_res.get('critique')}")
                    st.info(f"**Reference Solution:** {eval_res.get('exemplar')}")

# ----------------- TAB 3: CLIENT CODE AUDITOR -----------------
with tab3:
    st.subheader("Rapid Code Audit & Bottleneck Report Generator")
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
    code_input = st.text_area("Paste Client or Lab Code:", value=sample_code, height=200)

    if st.button("🔬 Generate Technical Audit Report", use_container_width=True):
        with st.spinner("Auditing code with Google Gemma 2..."):
            res = engine.explain_lab_code(code=code_input, language=lang)
            st.markdown(f"### 📋 Executive Summary\n{res.get('summary')}")
            st.markdown(f"### 🧠 Memory & Concurrency Analysis\n{res.get('memory_breakdown')}")
            st.markdown(f"### ⏱️ Algorithmic Complexity\n{res.get('complexity')}")
            st.warning(f"### ⚠️ Risk & Deadlock Audit\n{res.get('pitfalls')}")

# ----------------- TAB 4: OPENTELEMETRY & UNIT ECONOMICS -----------------
with tab4:
    st.subheader("OpenTelemetry GenAI Observability & Side-Hustle Unit Economics")
    st.caption("Live trace spans proving why open-weight models (Google Gemma 2) keep side-hustle profit margins at 100%.")

    spans = get_recent_spans()
    c1, c2, c3 = st.columns(3)
    c1.metric("Recorded GenAI Spans", len(spans))
    c2.metric("Gemma 2 Inference Cost", "$0.00 USD", delta="100% Profit Margin")
    c3.metric("Proprietary API Cost Saved", f"${round(len(spans) * 0.045, 3)} USD", delta="Saved via Open Weights")

    if not spans:
        st.info("No inference spans recorded yet. Generate a Freelance Proposal or Interview Scenario to inspect live OpenTelemetry traces.")
    else:
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
                with st.expander("Inspect OpenTelemetry GenAI Attributes"):
                    st.json(s["attributes"])
