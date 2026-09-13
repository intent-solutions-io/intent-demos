---
name: Intent Demos
description: A proof-first public catalog built as a squared editorial ledger.
colors:
  paper: "#f2f1ed"
  paper-bright: "#fbfaf7"
  ink: "#171716"
  ink-soft: "#2b2b29"
  night: "#121412"
  night-raised: "#1b1e1b"
  orange: "#f05a28"
  orange-dark: "#a63a12"
  yellow: "#f7bd2d"
  mint: "#9bd1c5"
  muted: "#666660"
  line: "#c9c8c1"
  line-dark: "#3a3d39"
  danger: "#a52c25"
  success: "#1e6d4f"
typography:
  display:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "clamp(58px, 7.4vw, 104px)"
    fontWeight: 800
    lineHeight: 0.93
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "clamp(42px, 5vw, 70px)"
    fontWeight: 800
    lineHeight: 0.93
    letterSpacing: "-0.04em"
  title:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "21px"
    fontWeight: 800
    letterSpacing: "-0.03em"
  body:
    fontFamily: "IBM Plex Sans, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "11px"
    fontWeight: 800
    letterSpacing: "0.04em"
rounded:
  square: "0"
  status-dot: "50%"
spacing:
  xs: "8px"
  sm: "12px"
  md: "16px"
  lg: "24px"
  section: "112px"
components:
  button-primary:
    backgroundColor: "{colors.orange}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "11px 15px"
  button-primary-hover:
    backgroundColor: "{colors.orange-dark}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "11px 15px"
  filter-control:
    backgroundColor: "transparent"
    textColor: "#d5d7d1"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "8px 12px"
  filter-control-selected:
    backgroundColor: "{colors.orange}"
    textColor: "{colors.ink}"
  search-input:
    backgroundColor: "#1a1c1a"
    textColor: "#ffffff"
    rounded: "{rounded.square}"
    padding: "9px 12px"
  form-input:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.square}"
    padding: "12px"
---

# Design System: Intent Demos

## Overview

**Creative North Star: "The Proof Ledger"**

The system combines Learn's editorial restraint with OMA's evidence-board discipline. It should feel like a public operating record: warm paper and near-black fields, hard dividers, mono-led headlines, dated facts, and controls that look ready to be used rather than admired.

Proof creates the visual hierarchy. Large numbers, source labels, ledger rows, and real screenshots carry the page; orange is a scarce signal for action, verification, and measured facts. The system rejects ornamental agency language, soft card grids, and decoration without evidentiary purpose.

**Key Characteristics:**

- Warm paper and near-black sections alternate to establish chapters.
- JetBrains Mono carries proof, hierarchy, navigation, labels, and controls.
- IBM Plex Sans keeps explanatory copy calm and readable.
- One-pixel rules and square corners make every surface feel ledger-like.
- Real screenshots and attributable metrics are the principal visual media.

## Colors

The palette pairs warm paper neutrals with green-black night fields and uses ember orange as the principal proof and action signal.

### Primary

- **Receipt Orange:** Marks primary actions, verified quantities, active filters, and the emphasized word or fact that carries a section.
- **Stamped Orange:** Deepens the accent for hover states, light-surface links, and quieter property labels.

### Secondary

- **Source Yellow:** Identifies source links when they sit inside dark proof panels.

### Tertiary

- **Verified Mint:** Supports live or verified status language without competing with the primary orange signal.

### Neutral

- **Ledger Paper:** The default page ground and form-field surface.
- **Bright Sheet:** Separates raised light chapters and proof cards from the base paper.
- **Ledger Ink:** Primary text, control borders, and high-contrast marks on light surfaces.
- **Soft Ink:** Long-form explanation and secondary copy on light surfaces.
- **Night Ledger:** The primary dark chapter surface.
- **Raised Night:** The only dark hover layer used inside proof boards.
- **Muted Copy:** Timestamps, measurement notes, and secondary explanatory text.
- **Paper Rule:** Dividers and card edges on light surfaces.
- **Night Rule:** Dividers and card edges on dark surfaces.

### Status

- **Error Red:** Contact-form failure feedback only.
- **Success Green:** Contact-form success feedback only.

### Named Rules

**The Receipt Before Accent Rule.** Orange marks action, verification, or a measured fact; it never floods a page as decoration.

## Typography

**Display Font:** JetBrains Mono (with monospace fallback)

**Body Font:** IBM Plex Sans (with sans-serif fallback)

**Label/Mono Font:** JetBrains Mono (with monospace fallback)

**Character:** The pairing is technical without becoming terminal-themed. Dense mono headings and labels establish the public-record voice; the sans-serif body face supplies legibility and restraint between proof objects.

### Hierarchy

- **Display** (800, fluid 58–104px, 0.93 line-height): Reserved for the opening thesis and its emphasized proof word.
- **Headline** (800, fluid 42–70px, 0.93 line-height): Leads major chapters and large evidence statements.
- **Title** (800, 21px): Names catalog entries and compact proof objects.
- **Body** (400, 16px, 1.55 line-height): Explains systems, evidence, and relationships; longer measures stop around 54–68 characters.
- **Label** (800, 11px, 0.04em tracking, uppercase where categorical): Carries categories, controls, statuses, sources, and compact metadata.

### Named Rules

**The Mono Carries Proof Rule.** JetBrains Mono carries headings, metrics, controls, labels, and links; IBM Plex Sans carries explanation.

## Layout

The primary shell is capped at 1180px with 24px desktop gutters, tightening to 20px below 1000px and 14px below 720px. Large sections use 112px vertical padding on desktop and 76px on mobile. The desktop composition relies on asymmetric two-column grids, usually placing a concise thesis beside a denser ledger, proof board, or screenshot.

At 1000px, major split layouts collapse to one column and the primary navigation keeps only its final action. At 720px, proof pairs, sibling cards, product cards, metrics, forms, and ledger rows become single-column; the sticky masthead becomes part of normal flow. Dense evidence stays readable by changing grid structure rather than shrinking type below its established floor.

Spacing is compact inside controls and ledgers and generous between chapters. Repeated 8px, 12px, 16px, and 24px steps form the working rhythm; large fluid gaps bridge asymmetric desktop columns.

## Elevation & Depth

The system uses no shadows. Depth comes from alternating paper and night surfaces, a small raised-night hover shift, one-pixel rules, and screenshot crops contained by hard edges. The sticky light masthead alone uses a translucent paper surface with a 12px backdrop blur.

### Named Rules

**The Flat Ledger Rule.** Surfaces are separated with tonal shifts and one-pixel rules; shadows are not part of the vocabulary.

## Shapes

The form language is square. Buttons, filter controls, inputs, panels, screenshot frames, catalog rows, and product cards use zero radius and rely on borders for definition. The only circles are six-pixel status indicators, which makes their live-state meaning unambiguous.

### Named Rules

**The Square Contract Rule.** Interactive controls, panels, fields, and cards use zero radius; circles are reserved for compact status indicators.

## Components

### Buttons

- **Shape:** Square, bordered controls with a 44px minimum touch target and compact mono labels.
- **Primary:** Receipt-orange fill, matching border, ledger-ink text, and 11px by 15px padding.
- **Hover / Focus:** Primary buttons deepen to stamped orange; every focus-visible state receives a three-pixel orange outline offset by four pixels.
- **Secondary:** Transparent on paper with an ink border; hover reverses to an ink fill with bright-paper text.

### Chips

- **Style:** Square 38px-minimum filter controls with dark borders, compact uppercase mono labels, and 8px by 12px padding.
- **State:** Hover and `aria-pressed="true"` use the same receipt-orange fill and ledger-ink text, so selection is explicit without adding an icon.

### Cards / Containers

- **Corner Style:** Square with one-pixel borders.
- **Background:** Bright sheet on light chapters; night or the product-specific deep teal on dark proof chapters.
- **Shadow Strategy:** None; see Elevation & Depth.
- **Border:** Paper rules on light cards and night rules on dark cards.
- **Internal Padding:** Usually 24–26px for card bodies and 18–22px for compact evidence cells.

### Inputs / Fields

- **Style:** Square, one-pixel bordered fields. Catalog search uses a raised dark field; the contact form uses ledger paper on a bright sheet.
- **Focus:** The global three-pixel receipt-orange outline supplies the visible keyboard state.
- **Error / Disabled:** Form status uses the dedicated semantic colors; disabled submit controls shift to neutral gray and retain a wait cursor.

### Navigation

The network rail is a compact night strip with uppercase mono links and an orange current-page state. The light masthead is sticky on larger viewports, uses a mono wordmark, and reserves its filled orange treatment for the final action. Below 1000px, non-action links hide; below 720px, the masthead stops sticking.

### Proof Board

The signature proof board is a dark, ruled matrix of linked metrics. Numbers use oversized tabular mono figures; labels use body text; sources return to compact mono. A single orange scan line runs once across the top on load, and the entire motion vocabulary collapses under reduced-motion preference.

### Catalog Ledger

Each row separates evidence type, system description, and destination links into three desktop columns. On mobile the row becomes one vertical record and its links wrap left. Filtering hides whole rows rather than visually dimming irrelevant evidence.

## Do's and Don'ts

### Do:

- **Do** lead with a concrete artifact, metric, source, or dated status.
- **Do** alternate light and dark chapters to clarify the narrative sequence.
- **Do** keep components square and separate them with one-pixel rules.
- **Do** preserve the mono/sans division between proof language and explanation.
- **Do** provide visible focus and a reduced-motion path for every interaction.

### Don't:

- **Don't** turn the catalog into an undifferentiated grid of generic cards.
- **Don't** use orange as an ambient background or decorative wash.
- **Don't** add shadows, soft radii, glass cards, or ornamental illustration.
- **Don't** present a metric without its source and date context.
- **Don't** shrink dense evidence to preserve desktop columns on a narrow screen.
