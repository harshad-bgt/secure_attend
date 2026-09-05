# Typography Guide

SecureAttend AI uses clean, highly readable geometric sans-serif fonts to maintain a professional and academic appearance.

## Font Families
- **Primary Font**: `Inter` (Google Fonts)
  - Used for all UI elements, forms, and general text.
- **Secondary/Display Font**: `Outfit` or `Plus Jakarta Sans`
  - Used for large headers (H1, H2), marketing sections, and the login splash screen.

## Typescale (Web & Mobile)

### Headings (Display Font)
- **H1 (Display)**: 48px, Bold (700), -0.5px tracking. (Used for Login Screen Welcome)
- **H2 (Page Title)**: 32px, SemiBold (600). (Used for Dashboard main titles)
- **H3 (Section Title)**: 24px, Medium (500). (Used for Card headers)

### Body (Primary Font)
- **Body Large**: 18px, Regular (400), 1.5 line height.
- **Body Regular**: 16px, Regular (400), 1.5 line height. (Standard text)
- **Body Small**: 14px, Regular (400). (Used for secondary text, labels)

### UI Elements
- **Button Text**: 16px, Medium (500), 0.5px tracking. All caps disabled.
- **Overlines/Badges**: 12px, Bold (700), 1px tracking, ALL CAPS. (Used for Role indicators e.g., "STUDENT", "FACULTY")

## Platform Specifics
- **React Admin**: Fonts will be loaded via Google Fonts CDN in `index.html`.
- **Flutter Mobile**: Fonts will be bundled in the `pubspec.yaml` as assets to ensure offline availability and prevent UI jumping.
