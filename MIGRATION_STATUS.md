# CMSE 495 Course Migration: FS26 → SS27

## Current Status: PHASE 1 COMPLETE ✅

### What's Been Accomplished

#### ✅ Calendar System Ready (Phase 0)
- Spring 2027 calendar configured (Jan 19 - May 2)
- MWF class meeting pattern established
- ~41 class days across 15 weeks
- Milestones due on Sundays (first Sunday after Friday class)
- Key dates: MLK Day (Jan 18), Spring Break (Mar 8-14), Finals (May 3-7)
- Calendar export ready for students (course_calendar.ics)

#### ✅ Schedule Files Migrated (Phase 1)
- **58 FS26 files** converted to SS27 format
  - 43 class/activity files → `NN-class-slug.md`
  - 15 milestone files → `NN-next-sun-slug.md`
- **Sequential numbering** applied (01-58)
- **Frontmatter updated** to template format (minimal: just date field)
- **Internal links** updated to reference new filenames
- **Mapping document** created for reference (MIGRATION_MAPPING.yml)

#### 📋 Documentation Created
- [updateplan.md](updateplan.md) - Comprehensive 4-phase migration strategy
- [CALENDAR_SETUP_COMPLETE.md](CALENDAR_SETUP_COMPLETE.md) - Calendar reference
- [PHASE1_MIGRATION_COMPLETE.md](PHASE1_MIGRATION_COMPLETE.md) - Migration details
- [MIGRATION_MAPPING.yml](MIGRATION_MAPPING.yml) - FS26→SS27 file mapping
- [scripts/migrate_fs26_to_ss27.py](scripts/migrate_fs26_to_ss27.py) - Reusable script

---

## What's Next

### Phase 2: Manual Content Review (Your Domain)
**Timeline:** Parallel with course development

Manual tasks you'll handle:
1. **Remove semester-specific content**
   - Replace "by end of September" with "Week X"
   - Remove FS26 course references
   - Update timeline descriptions to be generic

2. **Verify Activity Placement**
   - CyberAmbassadors should run on Wednesdays
   - SCHOLARS should run on Fridays
   - Adjust spacing as needed

3. **Check Milestone Alignment**
   - Verify each milestone due date makes sense
   - Move dates if spring context requires adjustment
   - Ensure no milestones due the Sunday after spring break

4. **Test and Refine**
   - Review generated schedule (`_data/schedule.yml`)
   - Preview site locally
   - Make final adjustments

### Phase 3: Guide Content (Later)
- Decide which FS26 Guide files to include in SS27
- Identify reusable content for cmse_course_template
- Organize Guide files with sequential numbering

### Phase 4: Template Enhancements (Optional)
- Document naming conventions in template Guide
- Share migration script with template repository
- Add SS27 learnings to template documentation

---

## Quick Reference

### File Structure
```
cmse495-SS27/
├── config/spring_calendar.yml          ✅ Spring 2027 dates
├── _data/schedule.yml                  (will regenerate when ready)
├── Schedule/
│   ├── 01-class-welcome.md
│   ├── 02-class-cyberambassadors-*.md
│   ├── 04-next-sun-project-*.md
│   └── ... (58 total files)
├── Guide/                              (from template, ready to customize)
├── scripts/
│   ├── migrate_fs26_to_ss27.py         ✅ Migration script
│   └── update_schedule.py              (regenerate schedule)
├── updateplan.md                       ✅ Full strategy doc
├── CALENDAR_SETUP_COMPLETE.md          ✅ Calendar guide
├── PHASE1_MIGRATION_COMPLETE.md        ✅ Migration summary
└── MIGRATION_MAPPING.yml               ✅ File mapping reference
```

### Useful Commands

**Regenerate schedule after file adjustments:**
```bash
cd /Users/colbrydi/REPOS/cmse495-SS27
make schedule-spring
```

**Check for any schedule warnings:**
```bash
cat _data/schedule_warnings.yml
```

**Preview site locally:**
```bash
make serve-spring
# Open http://localhost:4000 in browser
```

**Check git status:**
```bash
git status
git log --oneline
```

---

## Key Facts to Remember

### Naming Conventions (from cmse_course_template)
- **Classes:** `NN-class-descriptive-slug.md`
  - Example: `05-class-project-planning.md`
  
- **Milestones:** `NN-next-sun-milestone-name.md`
  - The `next-sun` tells the generator to place on first Sunday after class
  - Example: `07-next-sun-project-proposal.md`
  
- **Same-day activities:** `NN-same-activity.md`
  - Appears same day as class
  
- **Plus-N activities:** `NN-plus-2-checkpoint.md`
  - Appears N days after class

### Frontmatter Format
All Schedule files need only:
```yaml
---
layout: schedule
date: 'YYYY-MM-DD'
---
```

That's it! No `order`, `mode`, `title`, or other fields needed.

### How Dates Work
1. You provide the date in frontmatter
2. The generator looks at filename pattern to determine event type
3. Calendar generates the display date for the website
4. ICS file exports for student calendars

---

## Decisions Made

✅ **Accepted your answers to Phase 1 questions:**
1. Keep milestone order and weeks from FS26 (adjust in review)
2. Use pure sequential numbering (01-59)
3. CyberAmbassadors on Wednesdays, SCHOLARS on Fridays
4. Manual content cleanup (removing semester-specific references)
5. Naming conventions documented in template

---

## Known Issues / Caveats

- **File numbering vs. class dates:** The current 01-58 numbering may not perfectly align with Spring 2027's ~41 class days. You'll need to manually verify and adjust as you review.
  
- **FS26 milestones:** Some FS26 milestones fall on different dates relative to the start of semester in FS26 vs. SS27. You may want to adjust a few milestone dates for spring context.

- **Content references:** The FS26 content still references fall-specific items (e.g., "before Thanksgiving"). These need manual cleanup during Phase 2.

---

## Success Criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| Calendar configured | ✅ | Spring 2027 MWF schedule ready |
| Files migrated | ✅ | 58 files converted to new naming |
| Naming conventions applied | ✅ | NN-class-* and NN-next-sun-* patterns |
| Frontmatter converted | ✅ | Old fields removed, new minimal format |
| Mapping document | ✅ | MIGRATION_MAPPING.yml for reference |
| Content reviewed | ⏳ | Pending Phase 2 (manual) |
| Schedule regenerated | ⏳ | Pending Phase 2 completion |
| Site tested locally | ⏳ | After Phase 2 content review |
| Guide content decided | ⏳ | Phase 3 |
| Template docs updated | ⏳ | Phase 4 (optional) |

---

## Questions?

Refer to:
- [updateplan.md](updateplan.md) for detailed strategy
- [PHASE1_MIGRATION_COMPLETE.md](PHASE1_MIGRATION_COMPLETE.md) for migration specifics
- [MIGRATION_MAPPING.yml](MIGRATION_MAPPING.yml) to trace FS26→SS27 mappings
- [cmse_course_template Guide](https://github.com/msu-cmse-courses/cmse_course_template/tree/main/Guide) for template documentation

