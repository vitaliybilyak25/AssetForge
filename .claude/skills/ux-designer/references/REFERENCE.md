# UX Designer Reference

## Nielsen's 10 Usability Heuristics

| # | Heuristic | Description | Example |
|---|-----------|-------------|---------|
| 1 | Visibility of system status | Keep users informed with timely feedback | Progress bar during metadata generation, batch status chips |
| 2 | Match between system and real world | Use familiar language and concepts | "Export to Adobe Stock" not "initiate platform upload" |
| 3 | User control and freedom | Support undo and easy exit | Cancel batch button, discard changes confirmation |
| 4 | Consistency and standards | Follow platform conventions | Components used consistently across all screens |
| 5 | Error prevention | Design to prevent problems | Confirm dialog before batch delete, form validation before submit |
| 6 | Recognition rather than recall | Minimize memory load | Show current profile selection, visible breadcrumbs |
| 7 | Flexibility and efficiency | Accelerators for expert users | Keyboard shortcuts, bulk selection, batch operations |
| 8 | Aesthetic and minimalist design | No irrelevant information | Clean asset grids, progressive disclosure for advanced settings |
| 9 | Help recover from errors | Plain language error messages with solutions | "API key invalid — update in Settings > Config" |
| 10 | Help and documentation | Easy to search, focused on tasks | Tooltips on complex fields, inline help text |

---

## WCAG AA Accessibility Checklist

### Perceivable
- [ ] Text contrast ≥ 4.5:1 (normal), 3:1 (large text, 18px+ or 14px+ bold)
- [ ] UI component contrast ≥ 3:1 against adjacent colors
- [ ] No information conveyed by color alone (use icon + color, or text + color)
- [ ] Images have meaningful alt text; decorative images have `alt=""`
- [ ] Video/audio has captions (not applicable for AssetForge currently)

### Operable
- [ ] All functionality accessible via keyboard
- [ ] No keyboard traps (focus can always leave a component)
- [ ] Focus order is logical (matches visual/reading order)
- [ ] Focus indicator is visible
- [ ] Skip navigation link for keyboard users (for long pages)
- [ ] Touch targets ≥ 44×44px on mobile

### Understandable
- [ ] Form inputs have associated `<label>` or `aria-label`
- [ ] Error messages identify the field and describe the issue
- [ ] Required fields are marked (asterisk + legend)
- [ ] Consistent navigation and labeling across pages
- [ ] Language attribute set on `<html>` tag

### Robust
- [ ] Valid semantic HTML (headings hierarchy, landmark regions)
- [ ] ARIA roles/attributes used correctly (don't override native semantics unnecessarily)
- [ ] Dynamic content changes announced to screen readers (`aria-live`)
- [ ] Status messages use `role="status"` or `role="alert"`

---

## ASCII Wireframe Conventions

```
Borders:     ┌─┐ └─┘ ├─┤ │ ─
Sections:    ═══ double line for major divisions
Buttons:     [Label]  or  [ Label ]  for primary CTAs
Icons:       (i) info  (x) close  (▼) dropdown  (☰) menu
Images:      [IMG] or [████] for image placeholder
Text input:  [________________]
Checkbox:    [x] checked  [ ] unchecked
Radio:       (•) selected  ( ) unselected
Loading:     [=====>    ] for progress bar
Status:      ● green  ● red  ● yellow  ○ grey
```
