#!/usr/bin/env python3
"""AI-powered course generator using OpenRouter."""
import argparse
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import prompts
from parser import parse_course_outline

load_dotenv()

APP_API_KEY = os.getenv("OPENROUTER_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-4o")

if not APP_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=APP_API_KEY,
)

def call_ai(prompt: str) -> str:
    """Call OpenRouter AI with the given prompt."""
    print(f"Calling AI...")
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return response.choices[0].message.content

def slugify(text: str) -> str:
    """Convert text to slug format."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def generate_outline(title: str, description: str, weeks: int, language: str) -> str:
    """Generate course outline."""
    print(f"Generating {weeks}-week course outline...")
    prompt = prompts.get_outline_prompt(title, description, weeks, language)
    return call_ai(prompt)

def generate_module_content(title: str, desc: str, outline: str, mod_num: int, mod_title: str, lang: str) -> str:
    """Generate content for a module."""
    print(f"Generating module {mod_num} content...")
    prompt = prompts.get_module_prompt(title, desc, outline, mod_num, mod_title, lang)
    return call_ai(prompt)

def generate_unit_content(title: str, desc: str, outline: str, mod_content: str, mod_num: int, mod_title: str, unit_num: int, unit_title: str, lang: str) -> str:
    """Generate content for a unit."""
    print(f"Generating module {mod_num}, unit {unit_num} content...")
    prompt = prompts.get_unit_prompt(title, desc, outline, mod_content, mod_num, mod_title, unit_num, unit_title, lang)
    return call_ai(prompt)

def save_files(output_dir: Path, course_data: dict, structure: dict, module_contents: dict, unit_contents: dict) -> None:
    """Save all generated content to files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    modules_dir = output_dir / "modules"
    units_dir = output_dir / "units"
    modules_dir.mkdir(exist_ok=True)
    units_dir.mkdir(exist_ok=True)
    
    (output_dir / "outline.md").write_text(course_data["outline"])
    (output_dir / "structure.json").write_text(json.dumps(structure, indent=2))
    
    for mod_num, content in module_contents.items():
        (modules_dir / f"module_{mod_num:02d}.md").write_text(content)
    
    for key, content in unit_contents.items():
        (units_dir / f"{key}.md").write_text(content)
    
    print(f"Files saved to {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Generate AI-powered courses")
    parser.add_argument("--title", required=True, help="Course title")
    parser.add_argument("--description", required=True, help="Course description")
    parser.add_argument("--language", default="English", help="Course language")
    parser.add_argument("--depth", default="medium", choices=["short", "medium", "long"], help="Course depth")
    
    args = parser.parse_args()
    weeks = prompts.DEPTH_WEEKS[args.depth]
    slug = slugify(args.title)
    output_dir = Path("outputs") / slug
    
    print(f"Generating course: {args.title}")
    print(f"Output directory: {output_dir}")
    
    outline = generate_outline(args.title, args.description, weeks, args.language)
    structure = parse_course_outline(outline)
    
    module_contents = {}
    for module in structure.get("modules", []):
        mod_num = module["week"]
        mod_title = module["title"]
        content = generate_module_content(args.title, args.description, outline, mod_num, mod_title, args.language)
        module_contents[mod_num] = content
    
    unit_contents = {}
    for module in structure.get("modules", []):
        mod_num = module["week"]
        mod_title = module["title"]
        mod_content = module_contents.get(mod_num, "")
        for unit in module.get("units", []):
            unit_num = unit["number"]
            unit_title = unit["title"]
            key = f"module_{mod_num:02d}_unit_{unit_num:02d}"
            content = generate_unit_content(args.title, args.description, outline, mod_content, mod_num, mod_title, unit_num, unit_title, args.language)
            unit_contents[key] = content
    
    course_data = {"outline": outline}
    save_files(output_dir, course_data, structure, module_contents, unit_contents)
    print("Course generation complete!")

if __name__ == "__main__":
    main()
