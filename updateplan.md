# Migration Plan: cmse495-FS26 → cmse495-SS27 (Template-Based)

## Overview
Migrate course content from the legacy cmse495-FS26 repository (ipynb-based, dual-repo workflow) to the new cmse495-SS27 repository, adopting the cmse_course_template structure and conventions.

**Key Principle:** Features that benefit the template → cmse_course_template. Content-specific customizations → cmse495-SS27.

---

## Current State Analysis

### FS26 Structure
- **Naming Convention:** MMDD (Month/Day) - e.g., `0831-Welcome.md`, `0902-CyberAmbassadors_First_Contact.md`
- **Files to Migrate:** 59 Schedule files
- **Frontmatter Format:** Legacy with `order: MMDD` field
  ```yaml
  ---
  layout: schedule
  title: "Welcome"
  order: 831
  mode: "schedule"
  ---
  ```
- **Guide:** 24 course guide files (content-heavy, course-specific)

### SS27/Template Structure
- **Naming Convention:** Sequential numbering - e.g., `01-class-course-welcome.md`, `02-class-project-first-contact.md`
- **Frontmatter Format:** Simplified with `date` field
  ```yaml
  ---
  layout: schedule
  date: '2026-09-01'
  ---
  ```
- **Guide:** Minimal template files (5 files)

---

## Migration Strategy

### Phase 1: Schedule File Conversion (Priority 1)
**Objective:** Convert 59 FS26 Schedule files to sequential numbering with updated frontmatter.

#### Tasks:
1. **Create conversion utility script** (`scripts/migrate_schedule.py` or similar)
   - Read all files from `/Users/colbrydi/REPOS/cmse495-FS26/Schedule/`
   - Extract MMDD prefix and content
   - Generate sequential numbers (01-59)
   - Build mapping: `MMDD → NN` for reference purposes
   - Parse existing frontmatter
   - Generate new frontmatter with `date` field (requires calendar mapping)
   - Write converted files to `/Users/colbrydi/REPOS/cmse495-SS27/Schedule/`

2. **Create date mapping**
   - Map each MMDD date to actual 2027 Spring semester dates
   - Reference: FS26 started Aug 31, 2025
   - Determine SS27 start date (likely early January 2027)
   - Generate `date` field in ISO format (YYYY-MM-DD)

3. **Update internal links in content**
   - Search for relative links like `../Schedule/0904-*` in FS26 files
   - Convert to new sequential naming in SS27 files
   - Links like `../Guide/Syllabus` remain unchanged (Guide structure is compatible)

4. **Validate conversion**
   - Verify all 59 files transferred
   - Check that all frontmatter is valid YAML
   - Confirm no broken internal links
   - Test site build locally

#### Deliverables:
- Migration script (reusable for future semesters)
- Mapping document: `Migration_Mapping.md` (MMDD → NN → Date)
- All 59 Schedule files in SS27 with correct naming and frontmatter
- Updated internal links

---

### Phase 2: Guide Content Review (Priority 2)
**Objective:** Determine which FS26 Guide files should be migrated vs. kept in template.

#### Current FS26 Guide Files (24 total):
- AI_Policy.md
- Communication.md
- Community_Partner_Communication.md
- Daily_Check_In.md
- Friday_SCHOLARS.md
- Git_Repository_Organization.md
- Glossary.md
- Honors_Option.md
- Knowledge_Stewardship.md
- Meeting_Agenda_and_Notes.md
- Milestone_Roadmap.md
- Monday_Peer_Review_and_Planning.md
- (and more...)

#### Current Template Guide Files (5 total):
- 01-Quick_Start.md
- 02-Glossary.md
- 10-Recommended_Workflow.md
- 11-Maintenance_and_Publishing.md
- index.md

#### Decision Criteria:
- **→ Template (reusable):** Files describing template features, general course mechanics that apply across courses
  - Examples: Git_Repository_Organization (if generic), Glossary (if general terms)
- **→ SS27 (content-specific):** Course-specific policies, CMSE495-specific content, custom workflows
  - Examples: AI_Policy (likely CMSE-specific), Friday_SCHOLARS (custom milestone), Daily_Check_In (customized format)

#### Tasks:
1. Review each FS26 Guide file for reusability
2. Flag files for template inclusion vs. SS27-only
3. Normalize naming convention to match template (sequential numbering with descriptive slugs)
4. Update frontmatter in Guide files to match template format (if different)
5. Copy to appropriate destination

#### Deliverables:
- Updated Guide files in SS27 with normalized naming
- Identified reusable files for cmse_course_template (if any)

---

### Phase 3: Root-Level Content & Config (Priority 3)
**Objective:** Update configuration and ensure SS27 is self-contained and production-ready.

#### Files to Review:
- `_config.yml` - Ensure course title, URLs, course-specific config
- `index.md` - Homepage, course description
- `.github/` - CI/CD workflows (should be generic from template)
- `scripts/` - Check for course-specific vs. generic scripts

#### Tasks:
1. Verify `_config.yml` has correct course title and metadata for SS27
2. Update `index.md` with SS27 course description (if different from FS26)
3. Ensure calendar generation tools work with new naming scheme
4. Test full site build and verify all links work

#### Deliverables:
- SS27 ready for local preview and deployment
- Verified build with no broken links or warnings

---

### Phase 4: Feature Enhancements to Template (Optional, Per-Need)
**Objective:** If SS27 requires new features, evaluate for template inclusion.

#### Decision Framework:
- **Worth adding to template?**
  - Is it reusable across multiple courses?
  - Does it improve the template's usability?
  - Does it follow the template's design principles?
  
- **Keep in SS27 only?**
  - Is it specific to this course/semester?
  - Is it experimental or under evaluation?
  - Would it add complexity without broad benefit?

#### Possible Enhancements (if identified):
- Custom schedule metadata fields (e.g., milestone tracking)
- Automated schedule visualization
- Enhanced frontmatter generators
- Course-specific layout improvements

---

## Naming Convention Reference

### Old Format (FS26)
```
MMDD-Descriptive_Title.md
0831-Welcome.md
0902-CyberAmbassadors_First_Contact.md
0920-MILESTONE_Exploration_and_Plan.md
```

### New Format (SS27)
```
NN-descriptive-slug.md
01-class-course-welcome.md
02-class-project-first-contact.md
05-class-project-preferences.md
```

### Conversion Example
| FS26 Filename | NN | Date | SS27 Filename |
|---|---|---|---|
| 0831-Welcome.md | 01 | 2027-01-12 | 01-class-course-welcome.md |
| 0902-CyberAmbassadors_First_Contact.md | 02 | 2027-01-14 | 02-class-project-first-contact.md |
| 0920-MILESTONE_Exploration_and_Plan.md | 05 | 2027-01-28 | 05-class-project-preferences.md |

---

## Frontmatter Updates

### FS26 Format
```yaml
---
layout: schedule
title: "Welcome"
order: 831
mode: "schedule"
---
```

### SS27/Template Format
```yaml
---
layout: schedule
date: '2027-01-12'
---
```

### Conversion Logic:
1. **Keep:** `layout: schedule` (unchanged)
2. **Remove:** `order`, `mode`, explicit `title` (derived from filename/content)
3. **Add:** `date: 'YYYY-MM-DD'` (mapped from MMDD)
4. **First heading becomes title:** The first H1 in the file serves as the page title

---

## Timeline & Dependencies

### Prerequisite
- [ ] Confirm SS27 spring semester start date
- [ ] Obtain calendar mapping (which dates correspond to which class meetings)

### Phase 1: Schedule Migration
- [ ] Create and test migration script
- [ ] Run migration on all 59 files
- [ ] Validate outputs
- [ ] Create mapping document
- **Est. Time:** 2-3 hours

### Phase 2: Guide Review & Migration
- [ ] Audit all 24 FS26 Guide files
- [ ] Create reusability matrix
- [ ] Copy/convert files to SS27
- [ ] Identify template candidates (if any)
- **Est. Time:** 1-2 hours

### Phase 3: Config & Build Verification
- [ ] Update SS27 configs
- [ ] Run full site build
- [ ] Verify links and layout
- **Est. Time:** 30 min - 1 hour

### Phase 4: (Optional) Template Enhancements
- [ ] Implement any identified improvements
- [ ] Test across template and SS27
- [ ] Commit to cmse_course_template
- **Est. Time:** Variable

---

## Conversion Reference Guide

### File Naming Patterns

#### Regular Classes (Wed, Fri after Mon start)
```
NN-class-descriptive-slug.md
```
**Examples:**
- `01-class-course-welcome.md` → Monday, Jan 19
- `02-class-project-review.md` → Wednesday, Jan 21
- `03-class-project-preferences.md` → Friday, Jan 23

#### Sunday Milestones (Due on first Sunday after class)
```
NN-next-sun-milestone-name.md
```
**Examples:**
- `05-next-sun-project-initial.md` → Due Sunday, Jan 31 (after Friday Jan 29)
- `09-next-sun-exploration-plan.md` → Due Sunday, Feb 28 (after Friday Feb 26)

**Event Type:** `next` in schedule YAML (auto-calculates Sunday)

#### Same-Day Check-ins (Activities on same day as class)
```
NN-same-check-in.md
```
**Event Type:** `same` in schedule YAML

#### Plus-N Activities (N days after class)
```
NN-plus-N-checkpoint.md
```
**Examples:**
- `03-plus-2-project-checkpoint.md` → Wed + 2 days = Friday
- `05-plus-3-review.md` → Monday + 3 days = Thursday

**Event Type:** `plus` in schedule YAML

---

## FS26 → SS27 Mapping Strategy

### Step 1: Identify FS26 File Categories
Run this to see the structure:
```bash
cd /Users/colbrydi/REPOS/cmse495-FS26/Schedule
ls | grep -c "MILESTONE" # Milestones
ls | grep -c "SCHOLAR"   # Scholar activities
ls | grep -c "CyberAmbassadors" # Ambassador activities
```

### Step 2: Map Date Ranges
**FS26 Dates:** Aug 31, 2025 - Dec 10, 2025 (~14 weeks)
**SS27 Dates:** Jan 19, 2027 - May 2, 2027 (~15 weeks)

**Mapping Approach:**
- FS26 starts: Aug 31 (Saturday) → Actually starts Sep 2 (Monday, class 02)
- SS27 starts: Jan 19 (Tuesday) → Actual first class
- Align milestones by week offset, not exact date

### Step 3: Create Conversion Script
The script will:
1. Read each FS26 file (`MMDD-Title.md`)
2. Extract title and MMDD date
3. Parse content and frontmatter
4. Determine event type (`class`, `next`, `same`, `plus`)
5. Calculate SS27 week-relative date
6. Generate SS27 filename with sequential number
7. Update internal links (e.g., `../Schedule/0904-*` → `../Schedule/02-*`)
8. Write converted file to SS27

### Step 4: Review and Manual Adjustments
After conversion:
- Verify frontmatter removed old fields (`order`, `mode`)
- Check that all links resolve
- Validate event types match schedule intent
- Update content for spring semester context

---

## Timeline & Dependencies (Revised)

### ✅ Completed
- [x] Confirm SS27 spring semester dates
- [x] Create Spring 2027 calendar config
- [x] Generate schedule data (`_data/schedule.yml`)
- [x] Generate ICS calendar (`course_calendar.ics`)
- [x] Document naming conventions

### Upcoming
**Phase 1: Schedule Migration** (Next)
- [ ] Create schedule conversion script (`scripts/migrate_schedule_fs26_ss27.py`)
- [ ] Test on sample files (3-5 files)
- [ ] Run full migration on all 59 files
- [ ] Validate outputs and fix link references
- **Est. Time:** 2-3 hours

**Phase 2: Guide Content Review** (Then)
- [ ] Audit FS26 Guide files for reusability
- [ ] Copy/organize to SS27/Guide
- [ ] Identify template candidates
- **Est. Time:** 1-2 hours

**Phase 3: Build & Validation** (Finally)
- [ ] Run Jekyll site build
- [ ] Verify no broken links
- [ ] Test site locally
- **Est. Time:** 30 min

---

## Risk & Mitigation (Updated)

| Risk | Mitigation |
|---|---|
| Broken links during migration | Create mapping doc, automated link validation after migration |
| Date mapping errors | Double-check calendar alignment; generate mapping with validation |
| Lost content | Preserve FS26 repo; review all files before deletion |
| Template drift | Document all SS27-specific features; clearly mark them |
| Incomplete frontmatter conversion | Test migration script on sample files first; manual review |

---

## Success Criteria

- ✅ All 59 Schedule files migrated to SS27 with correct numbering
- ✅ All frontmatter converted and valid
- ✅ All internal links functional
- ✅ Guide content organized (migrated or flagged for template)
- ✅ SS27 site builds and renders correctly
- ✅ FS26 content fully preserved in source repo
- ✅ Clear documentation of migration process for future semesters

---

## Next Steps

1. **Confirm this plan** with course needs and calendar dates
2. **Start Phase 1:** Create migration script and test on sample files
3. **Iterate:** Review outputs, adjust script logic if needed
4. **Document:** Keep detailed notes for future semester migrations

---

## Calendar System

### Key Discovery
The template uses a **YAML-based calendar system** (`config/spring_calendar.yml`) combined with **auto-generated schedule data** (`_data/schedule.yml`).

#### Calendar Config Structure
- **`config/spring_calendar.yml`**: Defines semester metadata (start/end dates, class days, breaks)
- **`_data/schedule.yml`**: Auto-generated from the calendar config + Schedule markdown files
- **`scripts/generate_course_calendar.py`**: Script that generates the ICS calendar file

#### Event Types Supported
The template recognizes these event types in `_data/schedule.yml`:
- `class`: Regular class meeting (MWF)
- `next`: Due on first Sunday after a class day (use for milestones)
- `same`: Same-day activity (e.g., check-in on same day as class)
- `plus`: Plus-N days from class (e.g., checkpoint 2 days after class)
- `non_class`: Breaks, holidays, university closures
- `general`: Unspecified event

#### Milestone Naming Convention
For **Sunday milestone deadlines**, use this pattern:
- **Filename:** `NN-next-sun-milestone-name.md`
- **Event Type in schedule:** `next`
- **Example:** 
  - File: `05-next-sun-initial.md`
  - Due date: First Sunday after class Day 05
  - Frontmatter: Only needs `date: 'YYYY-MM-DD'` (the Sunday date)

### Spring 2027 Calendar Setup

✅ **COMPLETED**
- Updated `config/spring_calendar.yml` with Spring 2027 dates:
  - First class day: Tuesday, January 19, 2027
  - Class days: Monday, Wednesday, Friday (MWF)
  - Last day: Sunday, May 2, 2027
  - MLK Day: January 18, 2027
  - Spring Break: March 8-14, 2027
  - Finals: May 3-7, 2027

- Generated `_data/schedule.yml` with all class meetings for Spring 2027
- Generated `course_calendar.ics` for Google Calendar import (ready for students)

### Calendar Notes
- **First class day:** Tuesday, Jan 19 (slightly offset from typical Monday start)
- **Class frequency:** MWF pattern generates proper week boundaries and milestone dates
- **Sunday milestone dates:** Auto-calculated as first Sunday after class day using `next` event type
- **Spring Break:** March 8-14 (week after 2 months of classes)
- **Total class meetings:** ~45 sessions (Mon/Wed/Fri for ~15 weeks)

---

## Questions to Resolve Before Phase 1

1. **Content Alignment:** Should milestones stay on the same relative week as FS26, or do you want to adjust timing for SS27?
   - Example: If "MILESTONE_Project_Preferences" was week 2 in FS26, keep it week 2 in SS27?
   - Or: Completely rethink milestone timing for spring semester?

2. **File Numbering:** With ~59 classes in SS27, do you want:
   - Sequential numbers (01-59) regardless of event type?
   - Separate numbering for classes vs. milestones?
   - Keep FS26 MMDD in a comment for reference?

3. **CyberAmbassadors & SCHOLAR Activities:** These appear frequently in FS26. Should they:
   - Keep their own sequence or mix with main classes?
   - Have distinct filename prefixes (e.g., `ambass-*`, `scholar-*`)?
   - Or integrate into the single sequence?

4. **Spring Semester Context:** Any content that needs spring-specific adjustments?
   - Timeline references (e.g., "by Thanksgiving" → "by finals")?
   - Seasonal references?
   - Different milestone deadlines?

5. **Template Feature Request:** Should the naming convention patterns be documented in the cmse_course_template for other instructors?
