127
128
#!/usr/bin/env python3
"""Streamlit web UI for AI-powered course generator."""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import prompts
from parser import parse_course_outline
import json
import re

load_dotenv()

# Page config
st.set_page_config(
    page_title="Course Generator AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main {
    padding: 2rem;
}
.stTitle {
    color: #FF6B35;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "course_outline" not in st.session_state:
    st.session_state.course_outline = None
if "course_structure" not in st.session_state:
    st.session_state.course_structure = None
if "generation_step" not in st.session_state:
    st.session_state.generation_step = "input"

API_KEY = os.getenv("OPENROUTER_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-4o")

def init_client():
    """Initialize OpenRouter client."""
    if not API_KEY:
        st.error("OPENROUTER_API_KEY not found in .env file")
        st.stop()
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)

def call_ai(prompt: str) -> str:
    """Call OpenRouter AI."""
    client = init_client()
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return response.choices[0].message.content

def slugify(text: str) -> str:
    """Convert text to slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def save_files(output_dir: Path, outline: str, structure: dict) -> None:
    """Save generated files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "outline.md").write_text(outline)
    (output_dir / "structure.json").write_text(json.dumps(structure, indent=2))

# Header
st.markdown("# 🎓 AI Course Generator")
st.markdown("Generate complete, AI-powered courses in minutes using OpenRouter")
st.divider()

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    api_status = "✅ Connected" if API_KEY else "❌ Not Configured"
    st.markdown(f"**API Status**: {api_status}")
    st.markdown(f"**Model**: {AI_MODEL}")
    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("""
    1. Fill in course details
    2. Click 'Generate Outline'
    3. Review and generate content
    4. Download your course
    """)

# Main content
if st.session_state.generation_step == "input":
    st.markdown("## 📝 Course Details")
    
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Course Title", placeholder="e.g., Python for Data Science")
    with col2:
        language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Chinese"])
    
    description = st.text_area(
        "Course Description",
        placeholder="Describe what this course will teach...",
        height=120
    )
    
    col1, col2 = st.columns(2)
    with col1:
        depth = st.radio("Course Duration", ["short", "medium", "long"], horizontal=True)
        depth_info = {"short": "2 weeks", "medium": "6 weeks", "long": "13 weeks"}
        st.caption(f"📅 {depth_info[depth]}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("")
    with col2:
        if st.button("🚀 Generate Outline", key="gen_outline", type="primary"):
            if not title or not description:
                st.error("Please fill in all fields")
            elif not API_KEY:
                st.error("Please configure your OpenRouter API key in .env")
            else:
                                st.session_state.title = title
                st.session_state.description = description
                st.session_state.language = language
                st.session_state.depth = depth
                st.session_state.generation_step = "generating"
                st.rerun()

elif st.session_state.generation_step == "generating":
    st.markdown("## 🔄 Generating Your Course")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Generate outline
        status_text.text("📚 Generating course outline...")
        progress_bar.progress(25)
        
        weeks = prompts.DEPTH_WEEKS[st.session_state.depth]
        prompt = prompts.get_outline_prompt(st.session_state.title, st.session_state.description, weeks, st.session_state.language)
        outline = call_ai(prompt)
        st.session_state.course_outline = outline
        
        progress_bar.progress(50)
        status_text.text("🔍 Parsing outline structure...")
        
        # Parse structure
        structure = parse_course_outline(outline)
        st.session_state.course_structure = structure
        
        progress_bar.progress(75)
        status_text.text("💾 Saving files...")
        
        # Save files
        slug = slugify(st.session_state.title)
        output_dir = Path("outputs") / slug
        save_files(output_dir, outline, structure)
        
        progress_bar.progress(100)
        status_text.text("✅ Course generated successfully!")
        
        st.session_state.generation_step = "review"
        st.rerun()
    except Exception as e:
        st.error(f"Error during generation: {str(e)}")
        st.session_state.generation_step = "input"

elif st.session_state.generation_step == "review":
    st.markdown("## ✅ Course Generated!")
    st.success("Your course outline has been generated successfully!")
    
    # Display structure
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Modules", st.session_state.course_structure['total_weeks'])
    with col2:
        st.metric("Total Units", st.session_state.course_structure['total_units'])
    with col3:
        st.metric("Course Language", st.session_state.language)
    
    st.divider()
    
    # Tabs for outline and structure
    tab1, tab2 = st.tabs(["📖 Outline", "📊 Structure JSON"])
    
    with tab1:
        st.markdown(st.session_state.course_outline)
    
    with tab2:
        st.json(st.session_state.course_structure)
    
    st.divider()
    
    # Download options
    st.markdown("## 📥 Download Your Course")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        outline_md = st.session_state.course_outline.encode()
        st.download_button(
            label="📄 Download Outline (MD)",
            data=outline_md,
            file_name=f"{slugify(st.session_state.title)}_outline.md",
            mime="text/markdown"
        )
    
    with col2:
        structure_json = json.dumps(st.session_state.course_structure, indent=2).encode()
        st.download_button(
            label="📋 Download Structure (JSON)",
            data=structure_json,
            file_name=f"{slugify(st.session_state.title)}_structure.json",
            mime="application/json"
        )
    
    with col3:
        if st.button("🔄 Generate Another Course", type="secondary"):
            st.session_state.generation_step = "input"
            st.session_state.course_outline = None
            st.session_state.course_structure = None
            st.rerun()

st.divider()
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.8rem; margin-top: 2rem;'>
🚀 Powered by OpenRouter | Built with Streamlit | AI-Generated Courses
</div>
""", unsafe_allow_html=True)
