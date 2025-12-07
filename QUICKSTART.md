# 🚀 Quick Start - Course Generator UI

This guide will get you up and running with the Streamlit web UI in minutes!

## Prerequisites

- Python 3.8+
- OpenRouter API key (get one free at https://openrouter.ai)

## Installation

### 1. Clone & Setup

```bash
git clone https://github.com/mouradamri21/course-generator.git
cd course-generator
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=sk_YOUR_ACTUAL_KEY_HERE
AI_MODEL=openai/gpt-4o  # or any model from OpenRouter
```

## Running the App

### Web UI (Streamlit) - Recommended!

```bash
streamlit run app.py
```

This opens a beautiful web interface at `http://localhost:8501`

**UI Features:**
- Easy course input form
- Real-time generation progress
- Download outline and structure JSON
- Mobile-responsive design

### CLI (Command Line)

```bash
python generate.py \
  --title "Web Development Fundamentals" \
  --description "Learn HTML, CSS, and JavaScript" \
  --language "English" \
  --depth "long"
```

## What Happens Next

1. **Type course details** in the form
2. **Click Generate** - watch the progress bar
3. **Review the outline** - see the markdown structure
4. **Download files** - get markdown outline and JSON structure
5. **Generate another** - repeat as many times as you want!

## Generated Files

Output gets saved to `outputs/[course-slug]/`:

```
outputs/web-development-fundamentals/
├── outline.md          # Full course outline
└── structure.json      # Structured data
```

## Tips & Tricks

💡 **Depths explained:**
- `short` = 2 weeks (quick overview)
- `medium` = 6 weeks (standard course)
- `long` = 13 weeks (comprehensive course)

🌍 **Language support:**
Generate courses in any language - Spanish, French, German, Chinese, etc.

⚡ **Performance:**
- Course generation takes 1-3 minutes depending on depth
- Uses OpenRouter for optimal AI model routing
- Temperature set to 0.1 for consistency

## Troubleshooting

**Q: API key not working?**
A: Make sure your `.env` file exists and has the correct format.

**Q: Streamlit not found?**
A: Run `pip install streamlit==1.52.0`

**Q: Generation taking too long?**
A: Try a `short` or `medium` course first, or switch to a faster model.

## Next Steps

- Check `README.md` for full documentation
- See `generate.py` for CLI usage
- View `prompts.py` to customize AI prompts
- Modify `parser.py` to change outline parsing logic

---

**Happy course generating! 🎓**
