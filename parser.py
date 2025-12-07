"""Parse markdown course outlines into structured JSON."""
import re
from typing import Dict, Any, List

def parse_course_outline(markdown: str) -> Dict[str, Any]:
    """Parse markdown course outline into structured data."""
    lines = markdown.split('\n')
    modules = []
    current_module = None
    current_units = []
    
    for line in lines:
        if line.startswith('### Week '):
            if current_module:
                current_module['units'] = current_units
                modules.append(current_module)
            match = re.search(r'### Week (\d+):\s*(.*)', line)
            if match:
                week_num = int(match.group(1))
                title = match.group(2).strip()
                current_module = {'week': week_num, 'title': title}
                current_units = []
        elif line.startswith('- Unit ') and current_module:
            match = re.search(r'- Unit (\d+):\s*(.*)', line)
            if match:
                unit_num = int(match.group(1))
                unit_title = match.group(2).strip()
                current_units.append({'number': unit_num, 'title': unit_title})
    
    if current_module:
        current_module['units'] = current_units
        modules.append(current_module)
    
    return {
        'modules': modules,
        'total_weeks': len(modules),
        'total_units': sum(len(m.get('units', [])) for m in modules)
    }
