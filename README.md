# Course Generator

AI-powered Python course generator using OpenRouter. Generates complete, well-structured courses from simple descriptions.

## Features

- Two-Stage Generation: Generate outline first, then detailed content
- Configurable Depth: short (2 weeks), medium (6 weeks), or long (13 weeks)
- Multi-Language Support: Generate courses in any language
- Structured Output: Clean JSON with modules, units, and reading lists
- OpenRouter Integration: Use any model via .env

## Installation

```bash
git clone https://github.com/yourusername/course-generator.git
cd course-generator
pip install -r requirements.txt
```

## Configuration

1. Create a .env file:

```env
OPENROUTER_API_KEY=your_key_here
AI_MODEL=openai/gpt-4o
```

## Usage

```bash
python generate.py --title "Web Development" --description "Learn HTML, CSS, JS" --language "English" --depth "long"
```

## License

MIT
