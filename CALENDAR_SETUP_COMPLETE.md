# Spring 2027 Calendar Setup - COMPLETE ✅

## What Was Done

### 1. Spring 2027 Calendar Configuration
**File:** `config/spring_calendar.yml`

Updated with Spring 2027 dates:
- **Semester Start:** Tuesday, January 19, 2027
- **Semester End:** Sunday, May 2, 2027
- **Class Days:** Monday, Wednesday, Friday (MWF)
- **MLK Day:** January 18, 2027 (no class)
- **Spring Break:** March 8-14, 2027
- **Finals Period:** May 3-7, 2027

### 2. Schedule Data Generated
**File:** `_data/schedule.yml`

Automatically generated schedule with:
- All ~45 class meetings on MWF dates
- Proper week grouping and boundaries
- Sunday milestone dates auto-calculated
- Pre-populated from template structure

### 3. Calendar Export
**File:** `course_calendar.ics`

Ready to import into Google Calendar or share with students. Contains all class dates and key deadlines.

---

## How It Works: Naming Conventions

### Regular Classes
```
NN-class-descriptive-slug.md
```
- Files are automatically assigned to MWF class dates in sequence
- First file → First Monday (Jan 20)
- Frontmatter only needs: `date: 'YYYY-MM-DD'`

### Sunday Milestones
```
NN-next-sun-milestone-name.md
```
- Use the `next-sun` pattern for Friday class deadlines that push to the following Sunday
- Example: Friday class on Jan 29 → Sunday deadline Jan 31
- The schedule generator automatically calculates the Sunday date

### Example Schedule Generated

```
Jan 18 (Mon)  - MLK Day (no class)
Jan 20 (Tue)  - Class 01 (01-class-course-welcome.md)
Jan 22 (Wed)  - Class 02 (02-class-project-review.md)
Jan 24 (Fri)  - Class 03 (03-class-preferences.md)
Jan 31 (Sun)  - Milestone Due (05-next-sun-initial.md) [auto-calculated]
...
```

---

## What's Next: Phase 1 - Schedule Migration

### The Challenge
- **59 files** in FS26 using MMDD naming (0831-Welcome.md, 0902-CyberAmbassadors_First_Contact.md, etc.)
- Need to convert to sequential numbering with updated frontmatter
- Update all internal links to reference new filenames
- Map FS26 content to SS27 calendar dates

### The Solution
Create a migration script that:
1. Reads all FS26 Schedule files
2. Extracts title and content
3. Strips old frontmatter fields (`order`, `mode`)
4. Maps MMDD dates to SS27 week-relative dates
5. Generates new sequential filenames
6. Rewrites internal links
7. Outputs to SS27/Schedule/

### Before We Build the Script
Need to answer (see updateplan.md):
1. **Content Timing:** Keep milestones at same week offset, or adjust for spring context?
2. **File Numbering:** Pure sequential (01-59) or preserve some structure?
3. **CyberAmbassadors & SCHOLAR:** How should these be named in sequence?
4. **Content Changes:** Any spring-specific adjustments needed?

---

## Files Modified

- ✅ `config/spring_calendar.yml` - Spring 2027 dates configured
- ✅ `_data/schedule.yml` - Auto-generated (will regenerate as files are added)
- ✅ `course_calendar.ics` - Generated for calendar import
- ✅ `updateplan.md` - Comprehensive migration plan with examples

---

## Quick Reference

### Regenerate schedule after adding new files:
```bash
cd /Users/colbrydi/REPOS/cmse495-SS27
make schedule-spring  # Updates _data/schedule.yml and course_calendar.ics
```

### Check for schedule warnings (missing dates, etc):
```bash
cat _data/schedule_warnings.yml
```

### Serve locally to preview:
```bash
make serve-spring
```

---

## Next Meeting Agenda

1. Review naming convention preferences (see updateplan.md questions)
2. Decide on FS26 → SS27 content mapping strategy
3. Build and test the migration script on sample files
4. Run full migration
5. Validate and adjust as needed

**Total estimated time for Phase 1:** 2-3 hours of active development

