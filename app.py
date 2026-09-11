import streamlit as st

from src.github_loader import (
    get_repository,
    get_all_files,
    read_files
)

from src.document_processor import (
    create_documents,
    split_documents
)

from src.vector_store import (
    create_vector_store,
    create_retriever
)

from src.rag_chain import (
    create_rag_chain,
    create_context
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GitHub Repository Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM UI
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #08090c;
    --panel: #101116;
    --panel-2: #14151b;
    --border: #242631;
    --muted: #8b8f9b;
    --text: #f5f7fb;
    --accent: #7c5cff;
    --accent-2: #5b8cff;
}

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            800px 400px at 50% -120px,
            rgba(124, 92, 255, 0.20),
            transparent 65%
        ),
        radial-gradient(
            700px 350px at 10% 30%,
            rgba(91, 140, 255, 0.07),
            transparent 65%
        ),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 980px;
    padding-top: 1.8rem;
    padding-bottom: 7rem;
}

[data-testid="stSidebar"] {
    display: none;
}

#MainMenu,
footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;
    padding: 26px 0 30px;
}

.hero-icon {
    width: 58px;
    height: 58px;
    margin: 0 auto 18px;
    border-radius: 18px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 27px;
    font-weight: 700;

    background:
        linear-gradient(145deg, #171923, #0f1015);

    border: 1px solid #30333f;

    box-shadow:
        0 0 0 5px rgba(124, 92, 255, 0.05),
        0 18px 45px rgba(0, 0, 0, 0.45);
}

.hero-title {
    margin: 0;
    font-size: 36px;
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -1.5px;

    background:
        linear-gradient(
            90deg,
            #ffffff 20%,
            #b9b4ff 55%,
            #8eb7ff 85%
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    margin-top: 10px;
    color: #969aa7;
    font-size: 14px;
}


/* ============================================================
   REPOSITORY CARD
   ============================================================ */

.repo-card {
    position: relative;
    overflow: hidden;

    padding: 22px;
    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(20, 21, 28, 0.96),
            rgba(13, 14, 19, 0.96)
        );

    border: 1px solid var(--border);

    box-shadow:
        0 20px 60px rgba(0, 0, 0, 0.28);
}

.repo-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 8%;
    right: 8%;
    height: 1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(124, 92, 255, 0.7),
            transparent
        );
}

.repo-label {
    color: #d8dae1;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 9px;
}

.repo-hint {
    color: #737784;
    font-size: 12px;
    margin-top: 9px;
}


/* ============================================================
   INPUT
   ============================================================ */

.stTextInput > div > div > input {
    height: 48px !important;

    background: #0b0c10 !important;
    color: #f4f5f8 !important;

    border: 1px solid #30333e !important;
    border-radius: 13px !important;

    padding: 0 15px !important;

    transition: all 0.2s ease;
}

.stTextInput > div > div > input:hover {
    border-color: #444856 !important;
}

.stTextInput > div > div > input:focus {
    border-color: #7761ff !important;

    box-shadow:
        0 0 0 1px #7761ff,
        0 0 25px rgba(124, 92, 255, 0.12) !important;
}


/* ============================================================
   ANALYZE BUTTON
   ============================================================ */

.stButton > button {
    height: 48px !important;

    border-radius: 13px !important;

    border: 1px solid rgba(146, 127, 255, 0.7) !important;

    background:
        linear-gradient(
            135deg,
            #775cff,
            #5c7dff
        ) !important;

    color: white !important;

    font-weight: 700 !important;

    box-shadow:
        0 8px 25px rgba(91, 92, 255, 0.18);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);

    box-shadow:
        0 12px 30px rgba(91, 92, 255, 0.28);
}


/* ============================================================
   REPOSITORY READY
   ============================================================ */

.repo-status {
    margin-top: 18px;
    margin-bottom: 26px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 14px 17px;

    border-radius: 15px;

    background: rgba(16, 17, 22, 0.86);
    border: 1px solid #272a35;
}

.repo-status-left {
    min-width: 0;
}

.repo-name {
    color: #f3f4f7;
    font-size: 14px;
    font-weight: 700;
}

.repo-url {
    color: #6f7380;
    font-size: 11px;

    margin-top: 4px;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.ready-pill {
    display: flex;
    align-items: center;
    gap: 7px;

    padding: 6px 10px;

    border-radius: 999px;

    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.18);

    color: #8ee6a8;

    font-size: 11px;
    font-weight: 700;

    flex-shrink: 0;
}

.ready-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 10px rgba(74, 222, 128, .65);
}


/* ============================================================
   EMPTY STATE
   ============================================================ */

.empty-state {
    text-align: center;
    padding: 76px 20px 40px;
}

.empty-orbit {
    width: 76px;
    height: 76px;

    margin: 0 auto 24px;

    border-radius: 24px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            145deg,
            rgba(124, 92, 255, 0.12),
            rgba(91, 140, 255, 0.06)
        );

    border: 1px solid rgba(124, 92, 255, 0.2);

    font-size: 30px;

    box-shadow:
        0 0 55px rgba(124, 92, 255, 0.08);
}

.empty-title {
    color: #f0f1f5;
    font-size: 20px;
    font-weight: 700;
}

.empty-text {
    max-width: 490px;
    margin: 8px auto 0;

    color: #777b87;
    font-size: 13px;
    line-height: 1.7;
}


/* ============================================================
   CHAT
   ============================================================ */

[data-testid="stChatMessage"] {
    padding: 8px 0 !important;
    background: transparent !important;
}

[data-testid="stChatMessageContent"] {
    max-width: 100%;
    border-radius: 17px !important;
    padding: 15px 18px !important;
    line-height: 1.65;
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"] {
    background: #15161c;
    border: 1px solid #282b36;
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stChatMessageContent"] {
    background:
        linear-gradient(
            145deg,
            rgba(18, 19, 25, 0.95),
            rgba(13, 14, 18, 0.95)
        );

    border: 1px solid #252832;
}


/* ============================================================
   SOURCES
   ============================================================ */

.source-wrapper {
    margin-top: 14px;
    padding-top: 12px;

    border-top: 1px solid #252832;
}

.source-title {
    color: #777b87;
    font-size: 10px;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 0.7px;

    margin-bottom: 7px;
}

.source-file {
    display: inline-block;

    padding: 5px 9px;
    margin: 2px 4px 2px 0;

    border-radius: 8px;

    background: #15161c;
    border: 1px solid #2a2d38;

    color: #aeb2bd;

    font-size: 11px;
}


/* ============================================================
   CHAT INPUT
   ============================================================ */

[data-testid="stChatInput"] {
    padding-top: 14px;
}

[data-testid="stChatInput"] > div {
    border-radius: 16px !important;

    background: #101116 !important;

    border: 1px solid #30333e !important;

    box-shadow:
        0 10px 35px rgba(0, 0, 0, .24);
}

[data-testid="stChatInput"] textarea {
    color: #f4f5f8 !important;
    background: transparent !important;
}

[data-testid="stChatInput"] > div:focus-within {
    border-color: #7560ff !important;

    box-shadow:
        0 0 0 1px #7560ff,
        0 10px 40px rgba(124, 92, 255, .12) !important;
}


/* ============================================================
   SUGGESTIONS
   ============================================================ */

.suggestion-label {
    color: #686c78;
    font-size: 11px;
    font-weight: 600;

    text-align: center;

    margin: 24px 0 10px;
}

.suggestion-row .stButton > button {
    height: 42px !important;

    background: #111217 !important;

    border: 1px solid #292c36 !important;

    color: #aeb2bc !important;

    font-size: 11px !important;
    font-weight: 500 !important;

    box-shadow: none !important;
}

.suggestion-row .stButton > button:hover {
    background: #171820 !important;
    border-color: #454857 !important;
    color: #e1e3e8 !important;
}


/* ============================================================
   STATUS / ALERT
   ============================================================ */

[data-testid="stStatusWidget"] {
    border-radius: 15px !important;
    border: 1px solid #292c36 !important;
    background: #101116 !important;
}

.stAlert {
    border-radius: 13px !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .block-container {
        padding-left: 18px;
        padding-right: 18px;
        padding-top: 1rem;
    }

    .hero-title {
        font-size: 29px;
    }

    .hero {
        padding-top: 18px;
    }

    .repo-card {
        padding: 17px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "repository" not in st.session_state:
    st.session_state.repository = None

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "repo_url" not in st.session_state:
    st.session_state.repo_url = ""

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# IMPORTANT: CASUAL CONVERSATION
# ============================================================

def is_casual_message(message):

    message = message.lower().strip()

    casual_messages = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "ok",
        "okay",
        "thanks",
        "thank you",
        "thankyou",
        "bye",
        "goodbye",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "what's up",
        "whats up"
    }

    return message in casual_messages


def generate_answer(question):

    rag_chain = st.session_state.rag_chain

    # Casual conversation does NOT need vector search.
    if is_casual_message(question):

        answer = rag_chain.invoke({
            "context": "",
            "query": question
        })

        return answer, []

    # Repository-related question.
    retriever = st.session_state.retriever

    docs = retriever.invoke(question)

    context = create_context(docs)

    answer = rag_chain.invoke({
        "context": context,
        "query": question
    })

    sources = list(
        dict.fromkeys(
            doc.metadata.get("source", "Unknown")
            for doc in docs
        )
    )

    return answer, sources


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-icon">◈</div>

    <h1 class="hero-title">
        GitHub Repository Assistant
    </h1>

    <div class="hero-subtitle">
        Understand your codebase with AI-powered repository search
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# REPOSITORY INPUT
# ============================================================

st.markdown("""
<div class="repo-card">

    <div class="repo-label">
        Connect repository
    </div>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5.5, 1.2], gap="small")

with col1:

    repo_url = st.text_input(
        "Repository URL",
        placeholder="https://github.com/username/repository",
        label_visibility="collapsed"
    )

with col2:

    analyze = st.button(
        "Analyze",
        use_container_width=True
    )

st.markdown(
    """
    <div class="repo-hint">
        Public GitHub repositories are supported.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ANALYZE REPOSITORY
# ============================================================

if analyze:

    if not repo_url.strip():

        st.error("Please enter a GitHub repository URL.")

    else:

        try:

            with st.status(
                "Preparing your repository...",
                expanded=True
            ) as status:

                st.write("Connecting to GitHub...")

                repo = get_repository(repo_url)

                st.write("Reading repository files...")

                repo_files = repo.get_contents("")

                all_files = get_all_files(
                    repo,
                    repo_files
                )

                st.write(
                    f"Found {len(all_files)} repository files."
                )

                st.write("Processing documents...")

                file_documents = read_files(
                    repo,
                    all_files
                )

                documents = create_documents(
                    file_documents
                )

                chunks = split_documents(
                    documents
                )

                st.write(
                    f"Created {len(chunks)} searchable chunks."
                )

                st.write("Building vector database...")

                vectorstore = create_vector_store(
                    chunks
                )

                retriever = create_retriever(
                    vectorstore
                )

                st.write("Starting AI assistant...")

                rag_chain = create_rag_chain()

                st.session_state.repository = repo
                st.session_state.vectorstore = vectorstore
                st.session_state.retriever = retriever
                st.session_state.rag_chain = rag_chain
                st.session_state.repo_url = repo_url
                st.session_state.messages = []

                status.update(
                    label="Repository is ready",
                    state="complete",
                    expanded=False
                )

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to analyze repository: {str(e)}"
            )


# ============================================================
# REPOSITORY STATUS
# ============================================================

if st.session_state.repository:

    repo = st.session_state.repository

    st.markdown(
        f"""
        <div class="repo-status">

            <div class="repo-status-left">

                <div class="repo-name">
                    {repo.full_name}
                </div>

                <div class="repo-url">
                    {st.session_state.repo_url}
                </div>

            </div>

            <div class="ready-pill">
                <span class="ready-dot"></span>
                Ready
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state.repository:

    st.markdown("""
    <div class="empty-state">

        <div class="empty-orbit">
            ⌘
        </div>

        <div class="empty-title">
            Start exploring your codebase
        </div>

        <div class="empty-text">
            Connect a GitHub repository above and ask questions
            about its structure, files, technologies, and implementation.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.markdown(
                '<div class="source-wrapper">'
                '<div class="source-title">Sources</div>',
                unsafe_allow_html=True
            )

            for source in message["sources"]:

                st.markdown(
                    f'<span class="source-file">📄 {source}</span>',
                    unsafe_allow_html=True
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

if (
    st.session_state.repository
    and not st.session_state.messages
):

    st.markdown(
        '<div class="suggestion-label">Suggested questions</div>',
        unsafe_allow_html=True
    )

    suggestions = [
        "Explain the project structure",
        "How does the main application work?",
        "What technologies are used?",
        "Where is the main logic implemented?"
    ]

    st.markdown(
        '<div class="suggestion-row">',
        unsafe_allow_html=True
    )

    cols = st.columns(4, gap="small")

    for i, question in enumerate(suggestions):

        with cols[i]:

            if st.button(
                question,
                key=f"suggestion_{i}",
                use_container_width=True
            ):

                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })

                try:

                    answer, sources = generate_answer(question)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as e:

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": (
                            "I couldn't process that request. "
                            f"Error: {str(e)}"
                        ),
                        "sources": []
                    })

                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# CHAT INPUT
# ============================================================

if st.session_state.repository:

    question = st.chat_input(
        "Ask anything about your repository..."
    )

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    answer, sources = generate_answer(question)

                    st.markdown(answer)

                    if sources:

                        st.markdown(
                            '<div class="source-wrapper">'
                            '<div class="source-title">Sources</div>',
                            unsafe_allow_html=True
                        )

                        for source in sources:

                            st.markdown(
                                f'<span class="source-file">📄 {source}</span>',
                                unsafe_allow_html=True
                            )

                        st.markdown(
                            "</div>",
                            unsafe_allow_html=True
                        )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as e:

                    error_message = (
                        "I couldn't process that request. "
                        f"Error: {str(e)}"
                    )

                    st.error(error_message)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    })
