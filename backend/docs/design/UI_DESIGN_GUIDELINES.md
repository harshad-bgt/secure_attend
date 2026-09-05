# UI Design Guidelines

## Overall Aesthetic
SecureAttend AI is a premium, modern, AI-powered smart attendance platform. The aesthetic should resemble a high-end commercial SaaS application, not a typical college project.

## Key Principles
1. **Clarity**: Information must be easily digestible. Use whitespace generously.
2. **Consistency**: Use a unified design system across both React and Flutter.
3. **Professionalism**: Avoid cartoonish graphics. Use clean vectors, Lucide icons (React), and Material Icons (Flutter).
4. **Subtle Motion**: Use micro-interactions (hover states, ripple effects, gentle fade-ins) to make the UI feel alive but not distracting.

## Mobile (Flutter) Guidelines
- **Material 3**: Heavily utilize Material 3 components (Cards, FABs, NavigationBar).
- **Bottom Navigation**: Primary navigation method for both Student and Faculty roles.
- **Empty States**: Never show a blank screen. Always use an illustration + text describing why it's empty.
- **Skeletons**: Use skeleton loaders during network requests instead of blocking circular progress indicators where possible.

## Web (React) Guidelines
- **UI Framework**: Shadcn UI combined with Tailwind CSS for consistent, accessible, and premium components.
- **Dashboard Layout**: Fixed left sidebar, scrolling main content area, sticky top header for user profile and notifications.
- **Data Tables**: Must support pagination, sorting, and inline search.
- **Forms**: Use clear labels, inline validation, and distinct primary/secondary buttons.
- **Modals**: Used for destructive actions or multi-step processes (like Face Enrollment).

## Branding
- **Name**: SecureAttend AI
- **Logo**: A modern, abstract geometric shape combining a shield (security) and an eye/face (biometrics).
- **Tone**: Authoritative, secure, and academic.
