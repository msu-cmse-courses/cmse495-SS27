#!/usr/bin/env python3
"""Migrate FS26 Schedule files to SS27 with new naming convention.

This script:
1. Reads all FS26 Schedule files (MMDD naming)
2. Sorts chronologically
3. Assigns sequential numbers (01-59)
4. Maps MMDD dates to SS27 MWF dates
5. Identifies milestones and maps to next-sun pattern
6. Updates frontmatter (removes order/mode, sets date)
7. Updates internal links
8. Copies to SS27/Schedule/

Usage:
    python3 scripts/migrate_fs26_to_ss27.py \
        --fs26-dir /path/to/cmse495-FS26/Schedule \
        --ss27-dir /path/to/cmse495-SS27/Schedule \
        --config config/spring_calendar.yml
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> Any:
    """Load YAML file."""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown file."""
    lines = content.splitlines(keepends=True)
    
    if not lines or lines[0].strip() != "---":
        return {}, content
    
    fm_lines = []
    body_start = 1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            body_start = i + 1
            break
        fm_lines.append(line)
    
    fm_text = "".join(fm_lines)
    body = "".join(lines[body_start:])
    
    try:
        frontmatter = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        frontmatter = {}
    
    return frontmatter if isinstance(frontmatter, dict) else {}, body


def generate_new_frontmatter(date: str) -> str:
    """Generate new minimal frontmatter with date only."""
    return f"---\nlayout: schedule\ndate: '{date}'\n---\n"


def is_milestone(filename: str) -> bool:
    """Check if file is a milestone based on name."""
    return "MILESTONE" in filename or "next-sun" in filename.lower()


def get_fs26_mmdd(filename: str) -> str:
    """Extract MMDD from FS26 filename."""
    return filename[:4]


def mmdd_to_date(mmdd: str, year: int = 2025) -> datetime:
    """Convert MMDD to date object for FS26 (fall 2025)."""
    return datetime.strptime(f"{year}-{mmdd}", "%Y-%m%d")


def generate_ss27_date(fs26_mmdd: str, sequence_number: int, is_milestone: bool, class_days: list[str]) -> tuple[str, str]:
    """
    Map FS26 MMDD date to SS27 MWF date.
    
    Strategy:
    - FS26 runs Aug 31 - Dec 10, 2025 (~17 weeks)
    - SS27 runs Jan 19 - May 2, 2027 (~15 weeks)
    - Map by week offset within the semester
    
    Returns: (ISO date string, event_type)
    """
    # FS26 semester info
    fs26_start = datetime(2025, 8, 31)  # Saturday
    fs26_file_date = mmdd_to_date(fs26_mmdd, 2025)
    
    # Calculate week offset in FS26
    days_from_start = (fs26_file_date - fs26_start).days
    week_offset = days_from_start // 7
    day_of_week_fs26 = fs26_file_date.strftime("%A")
    
    # SS27 semester info
    ss27_start = datetime(2027, 1, 18)  # Monday, Jan 18 (MLK Day)
    ss27_first_class = datetime(2027, 1, 19)  # Tuesday, Jan 19
    
    # For milestones, calculate next Sunday from the sequence
    if is_milestone:
        # Milestones come after Fridays
        # Estimate which Friday based on sequence
        class_count = sequence_number // 2  # Rough estimate
        friday_date = ss27_start + timedelta(days=7 + (class_count * 3))  # Approximate
        
        # Find next Sunday
        days_until_sunday = (6 - friday_date.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        milestone_date = friday_date + timedelta(days=days_until_sunday)
        
        return milestone_date.strftime("%Y-%m-%d"), "next"
    
    # For regular classes, use week offset
    # Map weeks: FS26 week N -> SS27 week N
    estimated_date = ss27_start + timedelta(weeks=week_offset)
    
    # Find nearest class day (Mon, Wed, Fri)
    # Map based on day of week in FS26
    if day_of_week_fs26 in ["Monday", "Tuesday"]:
        # Assign to Monday of SS27
        target_weekday = 0  # Monday
    elif day_of_week_fs26 == "Wednesday":
        # Assign to Wednesday of SS27
        target_weekday = 2  # Wednesday
    elif day_of_week_fs26 in ["Thursday", "Friday", "Saturday"]:
        # Assign to Friday of SS27
        target_weekday = 4  # Friday
    else:
        # Sunday -> Friday
        target_weekday = 4
    
    # Find the target weekday in this week
    current_weekday = estimated_date.weekday()
    days_ahead = target_weekday - current_weekday
    if days_ahead < 0:
        days_ahead += 7
    
    class_date = estimated_date + timedelta(days=days_ahead)
    
    return class_date.strftime("%Y-%m-%d"), "class"


def update_internal_links(content: str, link_mapping: dict[str, str]) -> str:
    """Update internal links from FS26 filenames to SS27 filenames."""
    updated = content
    
    for fs26_file, ss27_file in link_mapping.items():
        # Handle various link formats
        # ../Schedule/0904-Title -> ../Schedule/02-title
        # Simple string replacement to avoid regex issues
        patterns = [
            f"../Schedule/{fs26_file}",
        ]
        
        ss27_name = ss27_file.replace(".md", "")
        replacement = f"../Schedule/{ss27_name}"
        
        for pattern in patterns:
            updated = updated.replace(pattern, replacement)
    
    return updated


def main():
    parser = argparse.ArgumentParser(description="Migrate FS26 Schedule files to SS27")
    parser.add_argument("--fs26-dir", required=True, help="Path to FS26 Schedule directory")
    parser.add_argument("--ss27-dir", required=True, help="Path to SS27 Schedule directory")
    parser.add_argument("--config", required=True, help="Path to SS27 spring_calendar.yml")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without writing")
    
    args = parser.parse_args()
    
    fs26_dir = Path(args.fs26_dir)
    ss27_dir = Path(args.ss27_dir)
    
    if not fs26_dir.exists():
        print(f"Error: FS26 directory not found: {fs26_dir}")
        return 1
    
    if not ss27_dir.exists():
        print(f"Error: SS27 directory not found: {ss27_dir}")
        return 1
    
    # Get all FS26 Schedule files
    fs26_files = sorted(fs26_dir.glob("*.md"))
    
    if not fs26_files:
        print(f"No markdown files found in {fs26_dir}")
        return 1
    
    print(f"Found {len(fs26_files)} FS26 Schedule files")
    print()
    
    # Build mapping
    link_mapping = {}
    migration_log = []
    
    for seq_num, fs26_file in enumerate(fs26_files, 1):
        mmdd = get_fs26_mmdd(fs26_file.name)
        is_mile = is_milestone(fs26_file.name)
        
        # Generate SS27 filename
        # Extract title from filename
        title_part = fs26_file.name[5:-3]  # Remove MMDD- and .md
        
        # Slugify title
        slug = title_part.lower().replace("_", "-")
        
        # Determine prefix
        if is_mile:
            if "next-sun" not in slug:
                slug = f"next-sun-{slug.replace('milestone-', '')}"
            prefix = ""
        else:
            prefix = "class-"
        
        ss27_filename = f"{seq_num:02d}-{prefix}{slug}.md"
        
        # Generate SS27 date
        ss27_date, event_type = generate_ss27_date(mmdd, seq_num, is_mile, ["Monday", "Wednesday", "Friday"])
        
        # Record mapping
        link_mapping[fs26_file.name] = ss27_filename
        
        # Read FS26 file
        fs26_content = fs26_file.read_text(encoding="utf-8")
        old_fm, body = extract_frontmatter(fs26_content)
        
        # Generate new frontmatter
        new_fm = generate_new_frontmatter(ss27_date)
        
        # Update links in body
        updated_body = update_internal_links(body, {fs26_file.name.replace(".md", ""): ss27_filename.replace(".md", "")})
        
        # Combine
        new_content = new_fm + updated_body
        
        # Log
        migration_log.append({
            "seq": seq_num,
            "fs26_file": fs26_file.name,
            "fs26_mmdd": mmdd,
            "fs26_date": mmdd_to_date(mmdd, 2025).strftime("%Y-%m-%d"),
            "is_milestone": is_mile,
            "ss27_file": ss27_filename,
            "ss27_date": ss27_date,
            "event_type": event_type,
        })
        
        # Write to SS27 (or dry-run)
        ss27_file = ss27_dir / ss27_filename
        if not args.dry_run:
            ss27_file.write_text(new_content, encoding="utf-8")
            print(f"✓ {seq_num:02d}: {fs26_file.name:50} → {ss27_filename}")
        else:
            print(f"  {seq_num:02d}: {fs26_file.name:50} → {ss27_filename}")
    
    print()
    print("="*80)
    print("Migration Summary")
    print("="*80)
    print(f"Total files processed: {len(migration_log)}")
    print(f"Milestones: {sum(1 for log in migration_log if log['is_milestone'])}")
    print(f"Classes/Activities: {sum(1 for log in migration_log if not log['is_milestone'])}")
    
    # Write mapping file for reference
    mapping_file = ss27_dir.parent / "MIGRATION_MAPPING.yml"
    if not args.dry_run:
        with mapping_file.open("w") as f:
            yaml.dump(migration_log, f, default_flow_style=False)
        print(f"\nMapping file written to: {mapping_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())
