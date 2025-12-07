"""LLM Prompts for course generation."""

DEPTH_WEEKS = {
    "short": 2,
    "medium": 6,
    "long": 13
}

def get_outline_prompt(title: str, description: str, weeks: int, language: str) -> str:
    """Generate prompt for course outline creation."""
    return f"""You are an expert course designer. Create a comprehensive {weeks}-week university-level course outline.

Course Title: {title}
Description: {description}
Language: {language}
Duration: {weeks} weeks

Provide the outline in the following Markdown format:

# {title}

## Course Overview
Brief description of the course.

## Learning Outcomes
- Learning outcome 1
- Learning outcome 2

## Course Structure

### Week 1: Module Title
- Unit 1: Unit title
- Unit 2: Unit title
- Unit 3: Unit title

### Week 2: Module Title
- Unit 1: Unit title
- Unit 2: Unit title

Continue for all {weeks} weeks.

## Recommended Reading
- Reference 1
- Reference 2

Create a detailed, well-structured outline with 3-4 units per week."""

def get_module_prompt(title: str, description: str, outline: str, module_num: int, module_title: str, language: str) -> str:
    """Generate prompt for module content creation."""
    return f"""You are an expert course instructor. Create detailed content for a course module.

Course: {title}
Description: {description}
Language: {language}
Module {module_num}: {module_title}

Course Outline:
{outline}

Write comprehensive module-level content that introduces the key concepts. Include:
- Overview of the module
- Key learning objectives
- Main concepts to be covered
- Real-world applications
- Connection to subsequent modules

Write in {language}. Make it engaging and educational."""

def get_unit_prompt(title: str, description: str, outline: str, module_content: str, module_num: int, module_title: str, unit_num: int, unit_title: str, language: str) -> str:
    """Generate prompt for unit content creation."""
    return f"""You are an expert course instructor. Create a detailed article for a course unit.

Course: {title}
Module {module_num}: {module_title}
Unit {unit_num}: {unit_title}
Language: {language}

Course Description: {description}

Course Outline:
{outline}

Module Content:
{module_content}

Write a comprehensive, engaging article about '{unit_title}' that:
- Provides detailed explanations
- Includes practical examples
- Builds on previous units
- Prepares for subsequent units
- Includes key takeaways

Write in {language}. Make it suitable for university-level learners."""
