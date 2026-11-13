# Phase 1: Schedule File Migration - COMPLETE ✅

## What Was Done

### Migration Script
Created `scripts/migrate_fs26_to_ss27.py` that:
- Reads all 58 FS26 Schedule files (MMDD naming convention)
- Sorts chronologically by date
- Assigns sequential numbers 01-58
- Identifies milestones (files containing "MILESTONE")
- Generates SS27 filenames following template convention:
  - Classes: `NN-class-descriptive-slug.md`
  - Milestones: `NN-next-sun-descriptive-slug.md`
- Strips old frontmatter (removed `order`, `mode` fields)
- Sets new minimal frontmatter with `date` field only
- Updates internal links from old filenames to new ones
- Copies all files to SS27/Schedule/

### Migration Results
- ✅ **58 files migrated** from FS26 to SS27
  - 43 class/activity files
  - 15 milestone files
- ✅ **Sequential numbering applied** (01-58)
- ✅ **Frontmatter converted** to new template format
- ✅ **Mapping document created** (`MIGRATION_MAPPING.yml`)

### Files Copied
All FS26 Schedule files are now in SS27/Schedule/ with new names:

**Examples of conversion:**
```
0831-Welcome.md                          → 01-class-welcome.md
0902-CyberAmbassadors_First_Contact.md   → 02-class-cyberambassadors-first-contact.md
0906-MILESTONE_Project_Preferences.md    → 04-next-sun-project-preferences.md
1214-MILESTONE_Personal_Reflection.md    → 58-next-sun-personal-reflection.md
```

---

## What Needs Manual Adjustment

### 1. File Numbering
The current sequential numbering (01-58) doesn't yet align with the actual Spring 2027 class schedule. 

**Next step:** You'll need to manually review and renumber files to match the MWF schedule pattern. The migration script provides a logical starting point, but the calendar alignment needs your domain knowledge.

**Why:** The FS26 course has 43 class days spread over ~17 weeks. SS27 has ~41 class days over ~15 weeks. The mapping isn't perfect, so manual review is needed.

### 2. Activity Types
CyberAmbassadors and SCHOLARS appear as regular classes but need to be flagged/scheduled appropriately:

Current:
- `02-class-cyberambassadors-first-contact.md` (Wed activity)
- `10-class-scholar-review.md` (Fri activity)

You can:
- Keep them as-is (they'll show in the schedule as regular class days)
- Rename them with content clues so you remember which day they belong on
- Add notes in the content about which day they should run

### 3. Content Review
The frontmatter has been stripped, but **content still contains FS26-specific references** that you wanted to remove:

- Semester-specific dates ("by end of September", "before Thanksgiving")
- FS26-specific instructions or examples
- Links to FS26 courses or previous semesters

**Action:** Review each file and remove semester-specific language. This will make future migrations easier.

### 4. Milestone Timing
Some milestones may not align perfectly with the Spring 2027 calendar:

- FS26 milestones fall on specific Sundays based on the fall schedule
- SS27 Sundays occur on different dates due to different semester dates
- Manually verify that each milestone is scheduled for an appropriate date

---

## Reference Documents

### Mapping File
`MIGRATION_MAPPING.yml` contains the full mapping:
```yaml
- seq: 1
  fs26_file: 0831-Welcome.md
  fs26_mmdd: '0831'
  fs26_date: '2025-08-31'
  is_milestone: false
  ss27_file: 01-class-welcome.md
  ss27_date: '2027-01-22'
  event_type: class
```

Use this to trace back to original FS26 files if needed.

### File Listing
- `64 Schedule/*.md` files (after removing one template placeholder)
- Ready to regenerate `_data/schedule.yml` once files are in final positions

---

## Next Steps

### For You (Manual Review Phase)
1. [ ] Review each file's content and remove semester-specific language
2. [ ] Verify CyberAmbassadors are scheduled for Wednesdays
3. [ ] Verify SCHOLARS are scheduled for Fridays
4. [ ] Check that milestones fall on appropriate Sundays
5. [ ] Renumber files as needed to match your MWF schedule

### When Ready to Test
```bash
cd /Users/colbrydi/REPOS/cmse495-SS27

# Regenerate schedule (once files are finalized)
make schedule-spring

# Preview locally
make serve-spring

# Commit your changes
git add -A
git commit -m "Complete Phase 1: Schedule file migration from FS26"
```

---

## Success Metrics

✅ **Complete (Phase 1):**
- All 58 FS26 files converted and copied to SS27
- Naming convention applied (NN-class-/NN-next-sun-)
- Frontmatter updated to template format
- Mapping document created for reference

⏳ **Pending Manual Review (Next):**
- Content cleanup (remove semester-specific references)
- Schedule alignment (verify MWF dates match your calendar)
- CyberAmbassadors/SCHOLARS placement
- Final numbering and ordering

---

## Questions & Notes

**If you need to:**
- Renumber files: Just rename them (e.g., `01-` → `05-`). The numbers drive the positioning.
- Change milestone dates: Update the `date:` field in frontmatter
- Change event types: The `next-sun` pattern is auto-detected; you can verify in regenerated `_data/schedule.yml`

**Migration script reusability:**
The `migrate_fs26_to_ss27.py` script can be used for future semesters with the same pattern. Just update the source and destination paths.

