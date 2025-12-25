"""
Markdown parser for extracting hierarchical textbook structure.
Parses markdown files to identify modules, chapters, and sections.
"""
import re
from typing import List, Dict, Tuple
from pathlib import Path


class ParsedSection:
    """Represents a parsed section with its content"""

    def __init__(
        self,
        title: str,
        content: str,
        order: int,
        line_start: int,
        line_end: int
    ):
        self.title = title
        self.content = content
        self.order = order
        self.line_start = line_start
        self.line_end = line_end


class ParsedChapter:
    """Represents a parsed chapter with its sections"""

    def __init__(self, title: str, order: int, sections: List[ParsedSection]):
        self.title = title
        self.order = order
        self.sections = sections


class ParsedModule:
    """Represents a parsed module with its chapters"""

    def __init__(
        self,
        title: str,
        description: str | None,
        order: int,
        chapters: List[ParsedChapter]
    ):
        self.title = title
        self.description = description
        self.order = order
        self.chapters = chapters


def parse_markdown_file(file_path: str) -> Tuple[List[str], str]:
    """
    Read markdown file and return lines and full content.

    Args:
        file_path: Path to markdown file

    Returns:
        Tuple of (lines, full_content)

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    return lines, content


def extract_hierarchical_structure(
    lines: List[str],
    file_path: str
) -> Dict[str, List[Dict]]:
    """
    Extract hierarchical structure from markdown lines.

    Assumes markdown structure:
    - # Module Title
    - ## Chapter Title
    - ### Section Title

    Args:
        lines: List of markdown lines
        file_path: Original file path for reference

    Returns:
        Dictionary with chapters and sections structure
    """
    chapters = []
    current_chapter = None
    current_section = None
    section_content = []
    section_start_line = 0

    chapter_order = 0
    section_order = 0

    for line_num, line in enumerate(lines, start=1):
        # Check for chapter heading (## heading)
        chapter_match = re.match(r'^##\s+(.+)$', line)
        if chapter_match:
            # Save previous section if exists
            if current_section and current_chapter:
                current_section['content'] = '\n'.join(section_content).strip()
                current_section['line_end'] = line_num - 1
                current_chapter['sections'].append(current_section)

            # Save previous chapter if exists
            if current_chapter:
                chapters.append(current_chapter)

            # Start new chapter
            chapter_order += 1
            section_order = 0  # Reset section order for new chapter
            current_chapter = {
                'title': chapter_match.group(1).strip(),
                'order': chapter_order,
                'sections': []
            }
            current_section = None
            section_content = []
            continue

        # Check for section heading (### heading)
        section_match = re.match(r'^###\s+(.+)$', line)
        if section_match:
            # Save previous section if exists
            if current_section and current_chapter:
                current_section['content'] = '\n'.join(section_content).strip()
                current_section['line_end'] = line_num - 1
                current_chapter['sections'].append(current_section)

            # Start new section
            section_order += 1
            current_section = {
                'title': section_match.group(1).strip(),
                'order': section_order,
                'line_start': line_num,
                'line_end': line_num,  # Will be updated
                'content': ''
            }
            section_content = []
            section_start_line = line_num
            continue

        # Accumulate content for current section
        if current_section:
            section_content.append(line)

    # Save last section and chapter
    if current_section and current_chapter:
        current_section['content'] = '\n'.join(section_content).strip()
        current_section['line_end'] = len(lines)
        current_chapter['sections'].append(current_section)

    if current_chapter:
        chapters.append(current_chapter)

    return {'chapters': chapters}


def parse_textbook_markdown(
    file_path: str,
    module_title: str,
    module_description: str | None,
    module_order: int
) -> ParsedModule:
    """
    Parse a textbook markdown file into hierarchical structure.

    Args:
        file_path: Path to markdown file
        module_title: Title of the module
        module_description: Optional module description
        module_order: Order of module in textbook

    Returns:
        ParsedModule with chapters and sections

    Example markdown structure:
        ## Chapter 1: Introduction
        ### Section 1.1: Overview
        Content here...

        ### Section 1.2: Background
        More content...

        ## Chapter 2: Details
        ### Section 2.1: Technical Details
        Content...
    """
    lines, full_content = parse_markdown_file(file_path)
    structure = extract_hierarchical_structure(lines, file_path)

    # Convert to ParsedModule structure
    chapters = []
    for chapter_data in structure['chapters']:
        sections = []
        for section_data in chapter_data['sections']:
            section = ParsedSection(
                title=section_data['title'],
                content=section_data['content'],
                order=section_data['order'],
                line_start=section_data['line_start'],
                line_end=section_data['line_end']
            )
            sections.append(section)

        chapter = ParsedChapter(
            title=chapter_data['title'],
            order=chapter_data['order'],
            sections=sections
        )
        chapters.append(chapter)

    module = ParsedModule(
        title=module_title,
        description=module_description,
        order=module_order,
        chapters=chapters
    )

    return module
