# Moving This Course Website to a New Semester

Use this guide when preparing a new offering of CMSE 495. Start by forking this
repository so the existing semester remains available as a record. 

The schedule is generated from two sources:

- [`config/`](./config/) defines the semester calendar and meeting dates.
- [`Schedule/`](./Schedule/) contains the class pages and dated milestones.

Do not edit [`_data/schedule.yml`](./_data/schedule.yml),
[`_data/schedule_warnings.yml`](./_data/schedule_warnings.yml), or
[`course_calendar.ics`](./course_calendar.ics) by hand. They are regenerated
from the calendar and schedule pages.

## 1. Fork and rename the site

1. Fork this repository into the organization or account that will publish the
   new course site.
2. Rename the repository for the new term, such as `cmse495-FS28` or
   `cmse495-SS28`.
3. Configure GitHub Pages for the fork using the repository's normal publishing workflow.

## 2. Update site metadata

Edit [`_config.yml`](./_config.yml):

1. Set `title` and `description` for the course and semester.
2. Change `baseurl` to the new repository name, for example
   `/cmse495-FS28`.
3. Set `schedule_make_target` to `schedule-fall` or `schedule-spring` for the
   upcoming term. The pre-push check uses this target to verify generated
   schedule files.


Also update the semester heading and any prior-semester references on
[`index.md`](./index.md).

## 3. Gather the official calendar dates

Use the [MSU Academic Calendar](https://reg.msu.edu/ROInfo/Calendar/academic.aspx)
as the authoritative source for the following dates:

- the first and last day of classes;
- university holidays and break periods;
- final-exam dates; and
- commencement dates, if they are shown on the site.

Confirm the course's actual meeting days and times separately. They may differ
from the university-wide calendar.

## 4. Update the semester calendar configuration

Choose the file for the upcoming term:

- [`config/fall_calendar.yml`](./config/fall_calendar.yml) for a fall course;
- [`config/spring_calendar.yml`](./config/spring_calendar.yml) for a spring
  course.

Update the following fields in that file:

1. Set `semester_info.name`, `first_day`, and `last_day`.
2. Set `class_days` to the weekday names on which the course meets.
3. Replace each entry in `breaks` with the official holiday and break dates.
   A one-day closure uses `date`; a multi-day break uses `start` and `end`.
4. Update `important_dates`, including the final-exam range and commencement
   when applicable.
5. Add known cancellations or moved meetings under `schedule_adjustments`.
   Leave the empty lists and maps in place when there are no adjustments.

Use ISO dates (`YYYY-MM-DD`) throughout. The schedule generator excludes dates
listed in `breaks` when it assigns class-meeting numbers.

## 5. Update class and milestone pages

Review the pages in [`Schedule/`](./Schedule/). Update their content, remove
pages that no longer apply, and add pages for new activities.

The filename determines the scheduled date. `NN` is the **class-meeting
number**, not the count of all schedule files. Class pages must be numbered
continuously, beginning with `01`, for every scheduled class meeting:

```text
01-class-course-welcome.md
02-class-project-first-contact.md
03-class-project-review.md
```

Use these patterns for work related to a class meeting:

```text
NN-same-description.md       # on the same day as class NN
NN-plus-D-description.md     # D days after class NN
NN-next-mon-description.md   # next Monday after class NN
NN-next-tue-description.md   # next Tuesday after class NN
NN-next-wed-description.md   # next Wednesday after class NN
NN-next-thu-description.md   # next Thursday after class NN
NN-next-fri-description.md   # next Friday after class NN
NN-next-sat-description.md   # next Saturday after class NN
NN-next-sun-description.md   # next Sunday after class NN
```

For example, `11-next-sun-plan-video-storyboard.md` is scheduled for the
Sunday after class meeting 11. Keep an existing page's `layout: schedule`
front matter. The generator updates its `date` value.

If a page should remain in the repository but should not yet be a clickable
schedule item, set `publish: false` in its front matter. Do not leave a class
meeting without an `NN-class-*` page unless `TBD` is intentional.

## 6. Update stable course materials

Review [`Guide/`](./Guide/), instructor information, policies, assignment
links, forms, and external resources. Update dated language and verify
cross-links after renaming any guide pages.

Use relative links that match the actual current filename. For example, the
Project Video Guide is linked as:

```md
[Project Video Guide](../Guide/34-project-videos)
```

## 7. Regenerate the schedule

Set up the local environment if needed:

```bash
make envs
make bundle-install
```

Generate data for the selected term:

```bash
make schedule-fall
# or
make schedule-spring
```

This refreshes:

- [`_data/schedule.yml`](./_data/schedule.yml);
- [`_data/schedule_warnings.yml`](./_data/schedule_warnings.yml); and
- [`course_calendar.ics`](./course_calendar.ics).

Open `schedule_warnings.yml` immediately. Resolve every warning unless it
represents an intentional exception. In particular, a missing `NN-class-*`
page produces a `TBD` item on the published schedule.

Install the pre-push check once in each local clone:

```bash
make install-hooks
```

The check regenerates the outputs before every push and blocks the push if the
generated files differ from the committed versions. After it blocks a push, add
the regenerated files to the commit and push again.

## 8. Preview, review, and publish

1. Start the correct local preview:

   ```bash
   make serve-fall
   # or
   make serve-spring
   ```

2. Review the full schedule in date order. Confirm that every class page,
   milestone, break, and final-period event appears on its intended date.
3. Check schedule navigation and guide links from several schedule pages.
4. Download or subscribe to `course_calendar.ics` and confirm the calendar
   event dates.
5. Commit the calendar configuration, schedule pages, and regenerated files
   together. Publish only after the warnings file is understood and the
   schedule view is complete.

## 9. Add standalone menu pages

To add a standalone page to the primary menu, create a Markdown file at the
repository root with this front matter:

```yaml
---
layout: basic
title: "Seeking Community Partners"
---
```

For example, `Seeking-Community_Partners.md` is automatically listed in the
menu. Add its filename stem to `section_visibility` in `_config.yml` to hide
the page from both the menu and site search while keeping its URL available:

```yaml
section_visibility:
  Seeking-Community_Partners: unlisted
```

For a top-level folder section, use `layout: guide` in the folder's `index.md`.
It is listed automatically unless the folder name is `unlisted` in
`section_visibility`.
