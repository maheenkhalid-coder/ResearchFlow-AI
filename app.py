import sys
from pathlib import Path
from datetime import datetime

import streamlit as st

sys.path.append(str(Path(__file__).parent))

from backend.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

MAX_RUNS = 2

STATIONS = [
    {"key": "search", "label": "Search Agent", "icon": "&#128269;"},   # magnifying glass
    {"key": "read",   "label": "Reader Agent",  "icon": "&#128196;"},  # page
    {"key": "write",  "label": "Writer",        "icon": "&#9999;"},    # pencil
    {"key": "critic", "label": "Critic",        "icon": "&#128300;"},  # microscope
]

st.set_page_config(page_title="ResearchFlow AI", page_icon="\U0001F9ED", layout="wide")

# --------------------------------------------------------------------------
# Style
# --------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --ink: #0E1416;
    --panel: #141C1F;
    --panel-2: #182226;
    --line: #24333A;
    --text: #E7EEEF;
    --muted: #82989E;
    --amber: #D7A345;
    --amber-soft: rgba(215, 163, 69, 0.16);
    --teal: #4FB6A6;
    --teal-soft: rgba(79, 182, 166, 0.14);
}

html, body, [class*="css"]  { color: var(--text); }
.stApp { background: var(--ink); }

section[data-testid="stSidebar"] {
    background: var(--panel);
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel);
    border: 1px solid var(--line) !important;
    border-radius: 8px;
    padding: 0.4rem 0.6rem;
}

.rf-brand {
    font-family: 'Source Serif 4', serif;
    font-size: 1.35rem;
    color: var(--text);
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
    margin-bottom: 0.15rem;
}
.rf-brand span { color: var(--amber); }
.rf-tagline { color: var(--muted); font-size: 0.8rem; margin-bottom: 1.4rem; }

.rf-tries { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.6rem; }
.rf-pip { width: 9px; height: 9px; border-radius: 50%; border: 1px solid var(--amber); }
.rf-pip.filled { background: var(--amber); }
.rf-pip.empty { background: transparent; }
.rf-tries-label { color: var(--muted); font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }

.rf-log-heading {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    color: var(--muted);
    margin: 0.4rem 0 0.6rem 0;
    border-top: 1px solid var(--line);
    padding-top: 1rem;
}
.rf-log-empty { color: var(--muted); font-size: 0.82rem; line-height: 1.5; }

section[data-testid="stSidebar"] div[data-testid="stButton"] button {
    background: var(--panel-2);
    border: 1px solid var(--line);
    color: var(--text);
    text-align: left;
    border-radius: 6px;
    padding: 0.55rem 0.7rem;
    font-size: 0.82rem;
    width: 100%;
    transition: border-color 0.15s ease, background 0.15s ease;
}
section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
    border-color: var(--amber);
    background: var(--amber-soft);
    color: var(--text);
}

.rf-hero h1 {
    font-family: 'Source Serif 4', serif;
    font-weight: 600;
    font-size: 2.3rem;
    letter-spacing: -0.01em;
    margin-bottom: 0.2rem;
}
.rf-hero p { color: var(--muted); font-size: 0.98rem; max-width: 620px; }

.rf-pipeline-wrap { position: relative; margin: 2.4rem 0 1.6rem 0; }
.rf-pipeline-track {
    position: absolute;
    top: 27px;
    left: 6%;
    right: 6%;
    height: 2px;
    background: var(--line);
    z-index: 0;
}
.rf-pipeline-fill {
    position: absolute;
    top: 0; left: 0; height: 100%;
    background: linear-gradient(90deg, var(--teal), var(--amber));
    transition: width 0.5s ease;
}
.rf-stations { position: relative; z-index: 1; display: flex; justify-content: space-between; }
.rf-station { display: flex; flex-direction: column; align-items: center; width: 25%; }
.rf-node {
    width: 54px; height: 54px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    background: var(--panel-2);
    border: 2px solid var(--line);
    transition: all 0.3s ease;
}
.rf-station.active .rf-node {
    border-color: var(--amber);
    background: var(--amber-soft);
    box-shadow: 0 0 0 6px rgba(215,163,69,0.08);
    animation: rf-pulse 1.4s ease-in-out infinite;
}
.rf-station.done .rf-node { border-color: var(--teal); background: var(--teal-soft); }
@keyframes rf-pulse {
    0%, 100% { box-shadow: 0 0 0 6px rgba(215,163,69,0.08); }
    50% { box-shadow: 0 0 0 10px rgba(215,163,69,0.03); }
}
.rf-station-label { margin-top: 0.55rem; font-size: 0.85rem; color: var(--text); font-family: 'Inter', sans-serif; }
.rf-station-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--muted);
    margin-top: 0.1rem;
}
.rf-station.active .rf-station-status { color: var(--amber); }
.rf-station.done .rf-station-status { color: var(--teal); }

.rf-panel {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
}
.rf-report-body { font-family: 'Inter', sans-serif; line-height: 1.65; font-size: 0.95rem; }

.rf-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    margin-bottom: 0.6rem;
}

div[data-testid="stTextInput"] input {
    background: var(--panel-2);
    border: 1px solid var(--line);
    color: var(--text);
    border-radius: 6px;
}
div.stButton > button[kind="primary"] {
    background: var(--amber);
    color: #17110A;
    border: none;
    font-weight: 600;
    border-radius: 6px;
}
div.stButton > button[kind="primary"]:hover { background: #c8963c; }
div.stButton > button[kind="primary"]:disabled { background: var(--line); color: var(--muted); }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "runs_used" not in st.session_state:
    st.session_state.runs_used = 0
if "viewing" not in st.session_state:
    st.session_state.viewing = None  # index into history, or None = fresh run screen


def render_pipeline(active_idx, done_set):
    """active_idx: index of the currently running station, or -1 if none.
    done_set: set of indices already completed."""
    n = len(STATIONS)
    completed = len(done_set)
    pct = int((completed / n) * 100) if n else 0
    stations_html = ""
    for i, s in enumerate(STATIONS):
        if i in done_set:
            cls, status = "done", "done"
        elif i == active_idx:
            cls, status = "active", "running"
        else:
            cls, status = "idle", "queued"
        stations_html += (
            f'<div class="rf-station {cls}">'
            f'<div class="rf-node">{s["icon"]}</div>'
            f'<div class="rf-station-label">{s["label"]}</div>'
            f'<div class="rf-station-status">{status}</div>'
            f'</div>'
        )
    return (
        '<div class="rf-pipeline-wrap">'
        f'<div class="rf-pipeline-track"><div class="rf-pipeline-fill" style="width:{pct}%"></div></div>'
        f'<div class="rf-stations">{stations_html}</div>'
        '</div>'
    )


def save_to_history(topic, report, feedback, search_results, scraped):
    st.session_state.history.append({
        "topic": topic,
        "timestamp": datetime.now().strftime("%b %d, %H:%M"),
        "report": report,
        "feedback": feedback,
        "search_results": search_results,
        "scraped": scraped,
    })


def render_result(entry):
    st.markdown(f"<div class='rf-meta'>{entry['timestamp']} &middot; {entry['topic']}</div>", unsafe_allow_html=True)
    tab_report, tab_critic, tab_raw = st.tabs(["Report", "Critique", "Raw research"])
    with tab_report:
        with st.container(border=True):
            st.markdown(entry['report'])
    with tab_critic:
        with st.container(border=True):
            st.markdown(entry['feedback'])
    with tab_raw:
        st.markdown("**Search agent output**")
        with st.container(border=True):
            st.markdown(entry['search_results'])
        st.markdown("**Reader agent output**")
        with st.container(border=True):
            st.markdown(entry['scraped'])

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='rf-brand'>ResearchFlow <span>AI</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='rf-tagline'>A four-agent research pipeline</div>", unsafe_allow_html=True)

    remaining = max(MAX_RUNS - st.session_state.runs_used, 0)
    pips = "".join(
    f"<div class='rf-pip {'filled' if i < remaining else 'empty'}'></div>"
    for i in range(MAX_RUNS)
    )
    st.markdown(
        f"<div class='rf-tries'>{pips}<span class='rf-tries-label'>{remaining} of {MAX_RUNS} runs left</span></div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='rf-log-heading'>Research log</div>", unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown("<div class='rf-log-empty'>Runs you complete will appear here.</div>", unsafe_allow_html=True)
    else:
        for idx in reversed(range(len(st.session_state.history))):
            entry = st.session_state.history[idx]
            label = entry["topic"] if len(entry["topic"]) <= 34 else entry["topic"][:31] + "..."
            if st.button(f"{label}\n{entry['timestamp']}", key=f"hist_{idx}"):
                st.session_state.viewing = idx
        if st.button("Clear log", key="clear_log"):
            st.session_state.history = []
            st.session_state.viewing = None
            st.rerun()

# --------------------------------------------------------------------------
# Main area
# --------------------------------------------------------------------------
if st.session_state.viewing is not None:
    entry = st.session_state.history[st.session_state.viewing]
    if st.button("&larr; New research", key="back"):
        st.session_state.viewing = None
        st.rerun()
    st.markdown("<div class='rf-hero'><h1>Past result</h1></div>", unsafe_allow_html=True)
    render_result(entry)

else:
    st.markdown(
        "<div class='rf-hero'><h1>ResearchFlow AI</h1>"
        "<p>Four agents split the work of researching a topic: one searches, one reads, "
        "one writes, one critiques. Give it a topic and watch it move through the pipeline.</p></div>",
        unsafe_allow_html=True,
    )

    runs_left = MAX_RUNS - st.session_state.runs_used
    topic = st.text_input("Research topic", placeholder="e.g. the state of small modular nuclear reactors")

    if runs_left <= 0:
        st.info("This portfolio demo is capped at two runs per session, to keep API usage in check. Refresh the page to reset it.")
        run_clicked = False
    else:
        run_clicked = st.button("Run research", type="primary", disabled=not topic.strip())

    pipeline_placeholder = st.empty()
    pipeline_placeholder.markdown(render_pipeline(-1, set()), unsafe_allow_html=True)

    status_placeholder = st.empty()
    result_placeholder = st.container()

    if run_clicked and topic.strip():
        st.session_state.runs_used += 1
        done = set()
        state = {}
        error = None

        try:
            status_placeholder.caption("Searching the web for relevant sources...")
            pipeline_placeholder.markdown(render_pipeline(0, done), unsafe_allow_html=True)
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}"
                                      f"In your final answer, list each source with its title and full URL.")]
            })
            state["search_results"] = search_result["messages"][-1].content
            done.add(0)

            status_placeholder.caption("Reading the most relevant source in depth...")
            pipeline_placeholder.markdown(render_pipeline(1, done), unsafe_allow_html=True)
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped"] = reader_result["messages"][-1].content
            done.add(1)

            status_placeholder.caption("Drafting the report...")
            pipeline_placeholder.markdown(render_pipeline(2, done), unsafe_allow_html=True)
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
            done.add(2)

            status_placeholder.caption("Critiquing the draft...")
            pipeline_placeholder.markdown(render_pipeline(3, done), unsafe_allow_html=True)
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            done.add(3)

            pipeline_placeholder.markdown(render_pipeline(-1, done), unsafe_allow_html=True)
            status_placeholder.caption("Done.")

        except Exception as e:
            error = str(e)
            pipeline_placeholder.markdown(render_pipeline(-1, done), unsafe_allow_html=True)
            status_placeholder.empty()

        if error:
            st.error(f"The pipeline hit an error partway through: {error}")
        else:
            save_to_history(topic, state["report"], state["feedback"], state["search_results"], state["scraped"])
            with result_placeholder:
                render_result(st.session_state.history[-1])
