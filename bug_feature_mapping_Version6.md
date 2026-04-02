# Bug Feature Mapping Reference
> Use this document to auto-assign bugs to feature tags based on keywords found in bug titles, descriptions, and stack traces.

---

## 1. TAG NAME: Clear
**Description:** Covers all operations that remove or reset content, formatting, notes, or hyperlinks from cells or ranges. Triggered when users want to wipe out cell data without deleting the cell itself.

**Primary Keywords:**
`clear`, `erase`, `reset`, `remove content`, `remove format`, `delete content`, `clear all`, `clear formats`, `clear notes`, `clear hyperlinks`, `wipe cell`, `empty cell`, `delete data`

---

## 2. TAG NAME: Images
**Description:** Handles insertion, display, and management of images within the spreadsheet — either anchored to a cell, floating over cells, or rendered via an IMAGE formula.

**Primary Keywords:**
`image`, `picture`, `photo`, `insert image`, `image in cell`, `over cell`, `floating image`, `IMAGE()`, `image formula`, `thumbnail`, `icon`, `img`, `embed image`, `image resize`, `image position`

---

## 3. TAG NAME: Style
**Description:** Covers all visual formatting of cells including text alignment, font properties, background fill colors, border styles, and number formatting (e.g., currency, percentage, date format, time format). Also covers cases where cell submission detects or misidentifies the format type (date, time, duration, custom format).

**Primary Keywords:**
`style`, `alignment`, `font`, `bold`, `italic`, `underline`, `fill`, `background color`, `border`, `number format`, `cell format`, `text wrap`, `horizontal align`, `vertical align`, `font size`, `font color`, `strikethrough`, `format cell`, `currency`, `percentage`, `date format`, `time format`, `duration format`, `custom format`, `custom date`, `date detection`, `time detection`, `format detection`, `detected as date`, `detected as time`, `stored as string`, `display text`, `format type`, `accounts format`, `prefix`, `suffix`

> ℹ️ **Style vs Evaluation:**
> If a bug is about a **date, time, or number format being misidentified, incorrectly displayed, or wrongly stored** during cell submission → assign **Style**.
> Assign **Evaluation** only when the bug is about **formula computation, recalculation, or formula result being wrong**.
>
> **Examples:**
> | Bug | Tag |
> |---|---|
> | "Oct 20 not considered as date" | ✅ **Style** (date format detection) |
> | "Oct 20 need to be detected as custom date while submitting" | ✅ **Style** (custom date format) |
> | "Wrong output of Time Submission - 36:45 returning 12:45" | ✅ **Style** (time format display issue) |
> | "Incorrect display text for duration format" | ✅ **Style** (duration format display) |
> | "Currency Detection on Language settings" | ✅ **Style** (currency format detection) |
> | "SUM formula returning wrong value" | ✅ **Evaluation** (formula computation) |
> | "Array formula not recalculating" | ✅ **Evaluation** (recalculation issue) |

---

## 4. TAG NAME: XLSX File I/O
**Description:** Handles reading (parsing) and writing (generating) of `.xlsx` Excel files. Includes import/export integrity, formula preservation, and compatibility with Excel format standards.

**Primary Keywords:**
`xlsx`, `excel`, `import`, `export`, `parse`, `writer`, `file import`, `file export`, `open file`, `save file`, `.xlsx`, `excel format`, `workbook`, `spreadsheet file`, `file upload`, `download`, `compatibility`, `corrupt file`, `file read`, `file write`, `save and reopen`, `save & reopen`, `reopen file`, `after save`, `post save`

> ⚠️ **FORCED Priority Rule:** If a bug contains the keywords `save`, `reopen`, `save and reopen`, or `save & reopen` — **XLSX File I/O is forced**, regardless of any other feature tag matched.
>
> **Examples:**
> - "Filter not applied after save and reopen" → **XLSX File I/O** (not Filter)
> - "Chart missing after reopen" → **XLSX File I/O** (not Charts)
> - "Formula lost after save" → **XLSX File I/O** (not Evaluation)

---

## 5. TAG NAME: DSV File I/O
**Description:** Handles reading and writing of delimiter-separated value files such as CSV, TSV, and TXT. Covers delimiter handling, encoding, and data integrity during import/export.

**Primary Keywords:**
`csv`, `tsv`, `txt`, `dsv`, `delimiter`, `comma separated`, `tab separated`, `import csv`, `export csv`, `parse csv`, `text file`, `flat file`, `separator`, `encoding`, `line break`, `carriage return`, `quoted fields`, `newline`, `file parser`

---

## 6. TAG NAME: Shifting
**Description:** Covers insertion and deletion of rows, columns, and individual cells, including the shifting behavior of adjacent content when cells are added or removed.

**Primary Keywords:**
`insert row`, `delete row`, `insert column`, `delete column`, `insert cell`, `delete cell`, `shift cells`, `shift down`, `shift right`, `shift up`, `shift left`, `add row`, `remove row`, `add column`, `remove column`, `row insertion`, `column deletion`

---

## 7. TAG NAME: API
**Description:** Relates to all programmatic interfaces, public APIs, configuration methods, and meta-information exposed by the spreadsheet engine for external integration.

**Primary Keywords:**
`api`, `meta`, `endpoint`, `config`, `options`, `callback`, `event`, `listener`, `integration`, `sdk`, `plugin`, `interface`, `instance`, `initialize`, `destroy`, `getCell`, `setCell`, `getData`, `loadData`, `updateData`, `trigger`, `parameter_list`, `schema`, `response object`, `request object`

> ⚠️ **API Priority Rules:**
>
> **Rule 1 — `meta` is always API (FORCED):**
> If a bug contains the keyword `meta` → **API is forced**, regardless of any other feature tag.
> - "Meta info missing in sort callback" → **API** (not Sort)
> - "Undo meta not returned correctly" → **API** (not Undo/Redo)
>
> **Rule 2 — `response` / `request` keywords need context:**
> `response` and `request` alone do NOT force API. They map to API **only when**:
> - There is no identifiable feature (Filter, Chart, Sort, etc.) involved, AND
> - The bug is explicitly about an API response/request **object** being wrong, incomplete, or missing fields (e.g., `UndoRedoInfo response`, `Manage DV response`, `parameter_list`)
>
> **Rule 3 — Feature always beats API:**
> If a specific feature (Filter, Chart, Sort, Hyperlink, etc.) is clearly the root cause, assign the **Feature tag** even if `response` or `request` appears in the description.
> - "Filter response not returning correct rows" → **Filter** (not API)
> - "Chart request data is wrong" → **Charts** (not API)
>
> **Rule 4 — API beats Undo/Redo:**
> If the bug matches both API and Undo/Redo → **API wins**.
> - "UndoRedoInfo response missing activesheetid" → **API** (not Undo/Redo)

---

## 8. TAG NAME: Filter
**Description:** Covers standard row filtering, named filters, and advanced filter configurations. Includes display of filtered results and interaction with the filter UI.

**Primary Keywords:**
`filter`, `autofilter`, `named filter`, `advanced filter`, `filter row`, `filter column`, `filter condition`, `filter criteria`, `hide rows`, `show rows`, `dropdown filter`, `filter menu`, `filter icon`, `clear filter`, `reapply filter`, `filter range`

---

## 9. TAG NAME: Sort
**Description:** Handles sorting of data within a range or table, including single/multi-column sort, custom sort orders, and sorting applied within filtered views.

**Primary Keywords:**
`sort`, `ascending`, `descending`, `custom sort`, `sort order`, `sort column`, `sort range`, `multi-column sort`, `sort key`, `sort in filter`, `order by`, `alphabetical sort`, `numeric sort`, `sort direction`

---

## 10. TAG NAME: Find and Replace
**Description:** Covers search functionality within the sheet including finding all matches, finding the next match, and replacing content (individual or all occurrences).

**Primary Keywords:**
`find`, `replace`, `search`, `find all`, `find next`, `replace all`, `replace next`, `match case`, `match cell`, `search string`, `find dialog`, `search result`, `highlight find`, `regex search`, `look in`

---

## 11. TAG NAME: Page Layout
**Description:** Manages print and page configuration settings such as page size, orientation, margins, headers/footers, print area, gridlines, and page breaks.

**Primary Keywords:**
`page layout`, `print`, `page size`, `orientation`, `portrait`, `landscape`, `margins`, `header`, `footer`, `print area`, `page break`, `fit to page`, `gridlines print`, `repeat rows`, `repeat columns`, `scale`, `print preview`, `paper size`

---

## 12. TAG NAME: Autofit
**Description:** Automatically adjusts row heights and column widths to fit their content. Also covers manual or custom sizing of rows and columns.

**Primary Keywords:**
`autofit`, `auto fit`, `fit content`, `column width`, `row height`, `resize column`, `resize row`, `auto width`, `auto height`, `custom width`, `custom height`, `best fit`, `adjust column`, `adjust row`

---

## 13. TAG NAME: Cut / Copy / Paste
**Description:** Covers cut, copy, and all forms of paste operations including clipboard paste, internal engine paste, and Paste Special (values only, formats only, transpose, etc.).

**Primary Keywords:**
`cut`, `copy`, `paste`, `clipboard`, `paste special`, `paste values`, `paste format`, `paste formula`, `transpose`, `engine paste`, `ctrl+c`, `ctrl+v`, `ctrl+x`, `copy range`, `paste range`, `duplicate`, `copy cell`

> ⚠️ **FORCED Priority Rule:** If a bug contains `cut`, `copy`, `paste`, or `transpose` as the **primary action** — **Cut/Copy/Paste is forced** over any feature side-effect.
>
> **Examples:**
> - "CF lost after paste" → **Cut/Copy/Paste** (not Conditional Formatting)
> - "Hyperlink missing after copy paste" → **Cut/Copy/Paste** (not Hyperlink)
> - "Style not retained after paste" → **Cut/Copy/Paste** (not Style)
>
> **Exception:** If the bug is explicitly about the feature's own behavior triggered independently (not via paste/copy), assign the feature tag.

---

## 14. TAG NAME: Fill
**Description:** Covers auto-fill series (numeric, date, text patterns), copy fill, and special fill options. Used when content is extended or propagated across a range.

**Primary Keywords:**
`fill`, `fill series`, `autofill`, `fill down`, `fill right`, `fill up`, `fill left`, `fill handle`, `series`, `copy fill`, `fill special`, `auto complete`, `drag fill`, `extend series`, `linear fill`, `growth fill`

---

## 15. TAG NAME: Sheet View
**Description:** Controls how the sheet is displayed, including frozen rows/columns, zoom level, and grid spacing/density.

**Primary Keywords:**
`freeze`, `freeze row`, `freeze column`, `freeze pane`, `unfreeze`, `zoom`, `zoom in`, `zoom out`, `grid spacing`, `sheet view`, `view settings`, `split`, `fixed row`, `fixed column`, `gridlines`

---

## 16. TAG NAME: Defined Name
**Description:** Handles creation and usage of named ranges and defined names that reference cell ranges or values, enabling more readable formulas.

**Primary Keywords:**
`defined name`, `named range`, `name manager`, `create name`, `name reference`, `scope`, `global name`, `local name`, `named cell`, `name formula`, `define name`, `range name`

---

## 17. TAG NAME: Grouping
**Description:** Covers grouping and ungrouping of rows and columns for collapsible outline views, typically used for hierarchical data organization.

**Primary Keywords:**
`group`, `ungroup`, `row group`, `column group`, `outline`, `collapse`, `expand`, `grouping level`, `hide group`, `show group`, `group rows`, `group columns`, `outline level`

---

## 18. TAG NAME: Sheet Operations
**Description:** Manages sheet-level operations such as renaming, inserting new sheets, deleting, duplicating, moving, hiding, and unhiding sheet tabs.

**Primary Keywords:**
`sheet`, `rename sheet`, `insert sheet`, `delete sheet`, `duplicate sheet`, `move sheet`, `hide sheet`, `unhide sheet`, `sheet tab`, `new sheet`, `copy sheet`, `sheet name`, `tab color`, `sheet order`, `add tab`

---

## 19. TAG NAME: Hyperlink
**Description:** Covers hyperlink insertion into cells, hyperlink formulas (HYPERLINK()), and hyperlink editing or removal.

**Primary Keywords:**
`hyperlink`, `link`, `url`, `insert link`, `HYPERLINK()`, `hyperlink formula`, `edit link`, `remove link`, `external link`, `internal link`, `cell link`, `navigate link`, `broken link`, `anchor`

---

## 20. TAG NAME: Tables
**Description:** Covers structured table creation, formatting, resizing, and behavior including header rows, total rows, banded rows, and table references in formulas.

**Primary Keywords:**
`table`, `insert table`, `structured reference`, `table header`, `total row`, `banded rows`, `table style`, `table name`, `resize table`, `table range`, `convert to table`, `table formula`, `list object`

---

## 21. TAG NAME: Formula Parser
**Description:** Covers the core formula **parsing and lexical analysis engine only** — tokenizing formula strings, identifying syntax errors, and building the parse tree. Does NOT cover formula result computation or recalculation (see Evaluation).

**Primary Keywords:**
`formula parser`, `lexer`, `lex`, `tokenize`, `parse formula`, `syntax error`, `formula engine`, `expression`, `operand`, `operator`, `function call`, `parse tree`, `formula string`, `token`, `#NAME?`, `#VALUE!` *(when caused by parse failure)*

> ℹ️ **Formula Parser vs Evaluation:**
> - Bug is about **parsing/tokenizing the formula string** → **Formula Parser**
> - Bug is about the **computed result being wrong** → **Evaluation**

---

## 22. TAG NAME: Solver
**Description:** Covers the Solver add-in functionality for optimization problems — finding optimal values for a target cell by adjusting variable cells subject to constraints.

**Primary Keywords:**
`solver`, `optimize`, `minimize`, `maximize`, `objective`, `constraint`, `variable cell`, `target cell`, `solution`, `iteration`, `convergence`, `linear programming`, `non-linear`, `solver result`, `solver model`

---

## 23. TAG NAME: Goalseek
**Description:** Covers the Goal Seek feature which back-solves a formula to find the input value required to reach a desired result in a target cell.

**Primary Keywords:**
`goal seek`, `goalseek`, `back solve`, `target value`, `set cell`, `by changing`, `what-if`, `reverse calculate`, `goal`, `iterate`, `goal seek result`, `goal seek dialog`

---

## 24. TAG NAME: Evaluation
**Description:** Covers **formula computation and recalculation only** — array formulas, formula result correctness, recalculation triggers, circular references, and status bar aggregate functions. Does NOT cover format detection, date/time display, or number formatting (see Style).

**Primary Keywords:**
`evaluate`, `formula result`, `recalculate`, `array formula`, `submit formula`, `status bar`, `calculate`, `SUM`, `COUNT`, `AVERAGE`, `MIN`, `MAX`, `formula bar`, `Ctrl+Shift+Enter`, `volatile`, `dependency`, `circular reference`, `formula computation`, `wrong formula result`, `resubmit`

> ℹ️ **Evaluation vs Style:**
> - Bug is about **formula computation giving a wrong result** → **Evaluation**
> - Bug is about **date/time/number format being misidentified or wrongly displayed** → **Style**

---

## 25. TAG NAME: Conditional Formatting
**Description:** Covers rules-based cell formatting where styles are applied automatically based on cell values or formulas (e.g., highlight cells, data bars, color scales, icon sets).

**Primary Keywords:**
`conditional formatting`, `CF`, `highlight`, `data bar`, `color scale`, `icon set`, `rule`, `condition`, `format rule`, `manage rules`, `new rule`, `greater than`, `less than`, `between`, `formula rule`, `duplicate values`, `top/bottom rules`

---

## 26. TAG NAME: Crash Recovery
**Description:** Covers auto-save, session recovery, and crash handling mechanisms that restore unsaved work after an unexpected shutdown or application error.

**Primary Keywords:**
`crash`, `recovery`, `auto save`, `autosave`, `restore`, `unsaved`, `session`, `backup`, `crash recovery`, `recover file`, `data loss`, `auto recover`, `save state`, `checkpoint`

---

## 27. TAG NAME: Themes
**Description:** Covers theme management including applying, switching, creating, and customizing visual themes that control color palettes, fonts, and effects across the spreadsheet.

**Primary Keywords:**
`theme`, `color theme`, `apply theme`, `theme font`, `theme color`, `switch theme`, `custom theme`, `dark mode`, `light mode`, `appearance`, `palette`, `theme management`

---

## 28. TAG NAME: Pivot Table
**Description:** Covers all aspects of PivotTable creation and interaction including field placement, aggregation, grouping, filtering, refreshing, and layout changes.

**Primary Keywords:**
`pivot`, `pivot table`, `pivot field`, `row field`, `column field`, `value field`, `filter field`, `aggregate`, `sum`, `count pivot`, `pivot layout`, `refresh pivot`, `pivot source`, `pivot group`, `pivot filter`, `grand total`, `subtotal`, `create pivot`

---

## 29. TAG NAME: Merge
**Description:** Covers merging of cells including standard merge, merge and center, merge across, and unmerging operations.

**Primary Keywords:**
`merge`, `merge cell`, `merge and center`, `merge across`, `unmerge`, `combine cells`, `split cell`, `merged area`, `merge row`, `merge column`, `center across`

---

## 30. TAG NAME: Navigation
**Description:** Covers keyboard and UI-based navigation within the spreadsheet including moving between cells, sheets, scrolling, and jump-to-cell functionality.

**Primary Keywords:**
`navigate`, `navigation`, `move`, `arrow key`, `tab key`, `enter key`, `go to`, `scroll`, `jump to cell`, `cell reference`, `name box`, `keyboard navigation`, `focus cell`, `active cell`, `page up`, `page down`, `Ctrl+Home`, `Ctrl+End`

---

## 31. TAG NAME: Notes
**Description:** Covers insertion, editing, display, and deletion of cell notes (comments/annotations) attached to cells.

**Primary Keywords:**
`note`, `comment`, `annotation`, `insert note`, `edit note`, `delete note`, `cell note`, `note indicator`, `show note`, `hide note`, `note text`, `review note`

---

## 32. TAG NAME: Hide/Unhide
**Description:** Covers hiding and unhiding rows and columns, making them invisible without deleting the data they contain.

**Primary Keywords:**
`hide`, `unhide`, `hide row`, `hide column`, `unhide row`, `unhide column`, `hidden row`, `hidden column`, `show row`, `show column`, `row visibility`, `column visibility`

---

## 33. TAG NAME: Text to Columns
**Description:** Covers splitting cell content into multiple columns based on a delimiter or fixed width, commonly used for data parsing tasks.

**Primary Keywords:**
`text to columns`, `split text`, `split column`, `delimiter split`, `fixed width`, `parse text`, `convert text`, `split cell`, `comma split`, `space split`, `text wizard`, `data split`

---

## 34. TAG NAME: Autosum
**Description:** Covers one-click sum insertion and other auto-aggregate formula insertion shortcuts (SUM, AVERAGE, COUNT, etc.) based on detected ranges.

**Primary Keywords:**
`autosum`, `auto sum`, `SUM`, `quick sum`, `insert sum`, `sum range`, `sum formula`, `aggregate formula`, `auto aggregate`, `Alt+=`, `sum shortcut`

---

## 35. TAG NAME: Rich Text
**Description:** Covers inline rich text formatting within a single cell, including mixed fonts, colors, sizes within one cell value, and hyperlinks embedded in text.

**Primary Keywords:**
`rich text`, `inline format`, `mixed format`, `partial bold`, `partial italic`, `cell rich text`, `text formatting`, `inline hyperlink`, `multi-style`, `character format`, `text style`

---

## 36. TAG NAME: Data Validation
**Description:** Covers rules that restrict cell input to specific types, ranges, or lists — including dropdown lists, numeric ranges, date constraints, and custom formula validations.

**Primary Keywords:**
`data validation`, `DV`, `validation rule`, `dropdown list`, `input restriction`, `valid input`, `invalid input`, `validation message`, `error alert`, `list validation`, `numeric validation`, `date validation`, `custom validation`, `validation formula`, `input message`

---

## 37. TAG NAME: Charts
**Description:** Covers creation, editing, and interaction with charts including bar, line, pie, scatter, and other chart types linked to spreadsheet data.

**Primary Keywords:**
`chart`, `graph`, `bar chart`, `line chart`, `pie chart`, `scatter plot`, `chart title`, `legend`, `axis`, `series`, `chart data`, `insert chart`, `chart type`, `chart style`, `data range`, `chart update`, `chart format`

---

## 38. TAG NAME: Checkbox
**Description:** Covers checkbox cell controls — inserting, toggling, and binding checkbox state (TRUE/FALSE) to cell values.

**Primary Keywords:**
`checkbox`, `check box`, `tick box`, `toggle`, `checked`, `unchecked`, `boolean cell`, `insert checkbox`, `checkbox value`, `TRUE`, `FALSE`, `form control`

---

## 39. TAG NAME: Undo/Redo
**Description:** Covers issues that are strictly within the undo/redo core mechanism — the undo stack, redo stack, stack size limitations, and the main undo/redo layer of the engine code.

**Primary Keywords:**
`undo stack`, `redo stack`, `undo limit`, `redo limit`, `stack size`, `stack overflow`, `undo layer`, `redo layer`, `undo count`, `redo count`, `cannot undo`, `cannot redo`, `undo history lost`, `redo history lost`, `undo main layer`, `undo engine`

> ⚠️ **Strict Assignment Rule — Undo/Redo is assigned ONLY when:**
> 1. The bug is about the **undo stack or redo stack** being corrupt, lost, or behaving incorrectly, OR
> 2. The bug is about **undo/redo count, size, or limitations**, OR
> 3. The bug is traced to the **main undo/redo layer** of the engine code itself.
>
> **DO NOT assign Undo/Redo when:**
> - A feature does not restore correctly after undo → assign **Feature tag**
> - The undo/redo response/request object is missing data → assign **API**
> - The word "undo"/"redo" appears but the root cause is in another feature

---

## 40. TAG NAME: ZSheet File I/O
**Description:** Handles reading and writing of native `.zsheet` format files — the application's own file format. Covers serialization, deserialization, and format integrity.

**Primary Keywords:**
`zsheet`, `.zsheet`, `native format`, `zsheet file`, `open zsheet`, `save zsheet`, `zsheet parser`, `zsheet writer`, `zsheet export`, `zsheet import`, `native save`

---

## 41. TAG NAME: Templates
**Description:** Covers creating, applying, managing, and sharing spreadsheet templates for quick-start document creation.

**Primary Keywords:**
`template`, `preset`, `starter`, `template file`, `apply template`, `create template`, `template manager`, `save as template`, `template gallery`, `default template`

---

## 42. TAG NAME: Sparkline
**Description:** Covers mini in-cell charts (sparklines) such as line, bar, and win/loss sparklines used to visualize trends within a single cell.

**Primary Keywords:**
`sparkline`, `mini chart`, `in-cell chart`, `line sparkline`, `bar sparkline`, `win loss`, `trend`, `sparkline range`, `insert sparkline`, `sparkline color`, `sparkline style`, `sparkline group`

---
---

# 📌 Multi-Tag Conflict Resolution Guide

---

## 🔴 FORCED Rules (Highest Priority — Always Win First)

| Priority | Trigger | Forced Tag | Overrides |
|---|---|---|---|
| 1st | `save`, `reopen`, `save and reopen`, `save & reopen` | **XLSX File I/O** | ALL other tags |
| 2nd | `cut`, `copy`, `paste`, `transpose` as primary action | **Cut/Copy/Paste** | ALL feature side-effects (CF, Style, Hyperlink, etc.) |
| 3rd | `meta` | **API** | ALL other tags including Features and Undo/Redo |

> **If XLSX File I/O and Cut/Copy/Paste both trigger** → **XLSX File I/O wins** (save/reopen is strongest)

---

## 🟡 Priority Rules (Applied when no FORCED rule triggers)

### Style vs Evaluation
| Scenario | Assigned Tag |
|---|---|
| Date format misidentified / not detected during submission | **Style** |
| Time format wrong / incorrect display | **Style** |
| Duration format displayed incorrectly | **Style** |
| Custom date not recognised on cell submit | **Style** |
| Currency detected wrong based on locale | **Style** |
| Number format returning wrong type | **Style** |
| Formula result/computation is wrong | **Evaluation** |
| Array formula not recalculating | **Evaluation** |
| Circular reference error | **Evaluation** |

### Formula Parser vs Evaluation
| Scenario | Assigned Tag |
|---|---|
| Formula string tokenization / syntax error | **Formula Parser** |
| Formula computed result is wrong | **Evaluation** |

### API vs Other Tags
| Scenario | Assigned Tag |
|---|---|
| `meta` keyword present | **API** (FORCED) |
| Response/request object missing fields, no feature root cause | **API** |
| Feature is root cause even if `response`/`request` present | **Feature Tag** |
| API + Undo/Redo (no feature) | **API** |

### Feature vs Undo/Redo
| Scenario | Assigned Tag |
|---|---|
| Feature not restored correctly after undo | **Feature Tag** |
| Undo/redo stack corrupt, lost, or count wrong | **Undo/Redo** |
| "undo" in title but root cause is a feature | **Feature Tag** |

### Other Known Multi-Tag Conflicts
| Scenario | Tags Matched | Assigned Tag |
|---|---|---|
| Sort inside Filter | Sort + Filter | **Sort** |
| Autofit after Merge | Autofit + Merge | **Autofit** |
| Hyperlink formula broken | Hyperlink + Formula Parser | **Hyperlink** |
| Rich text lost on paste | Rich Text + Cut/Copy/Paste | **Cut/Copy/Paste** *(paste is primary action)* |
| Table filter dropdown missing | Tables + Filter | **Tables** |
| Named range broken in formula | Defined Name + Evaluation | **Defined Name** |
| Sparkline not updating on recalculate | Sparkline + Evaluation | **Sparkline** |
| CF rule lost after theme change | Conditional Formatting + Themes | **Conditional Formatting** |
| Image position wrong after freeze | Images + Sheet View | **Images** |
| Group collapse breaks filter | Grouping + Filter | **Grouping** |
| Hide row breaks sort range | Hide/Unhide + Sort | **Hide/Unhide** |
| Data validation dropdown lost in CSV | Data Validation + DSV File I/O | **DSV File I/O** |

---

## 🟢 Decision Flow (Use this order)

```
1. Does the bug contain: save / reopen / save and reopen / save & reopen?
   → YES → Tag: XLSX File I/O (STOP)

2. Is cut / copy / paste / transpose the PRIMARY action in the bug?
   → YES → Tag: Cut/Copy/Paste (STOP)

3. Does the bug contain: meta?
   → YES → Tag: API (STOP)

4. Is the bug about date / time / duration / number format being
   misidentified, wrongly displayed, or incorrectly stored?
   → YES → Tag: Style (STOP)

5. Is there a clearly identifiable Feature as the root cause?
   → YES → Tag: Feature (STOP)
   (Even if response/request appears in description)

6. Is the bug explicitly about an API response/request object being
   wrong or incomplete — with no clear feature root cause?
   → YES → Tag: API (STOP)

7. Is the bug strictly about undo stack / redo stack / stack limit /
   main undo-redo engine layer?
   → YES → Tag: Undo/Redo (STOP)

8. Does the bug match a known multi-tag conflict in the Priority Rules table?
   → YES → Use the Assigned Tag from the table (STOP)

9. No conflict — assign the single matched tag.
```

---

*Document Version: 6.0 | Updated: 2026-03-03*
*New in v6.0: Cut/Copy/Paste FORCED rule added. Date/time/number format detection bugs moved from Evaluation → Style. Formula Parser and Evaluation scopes clarified.*