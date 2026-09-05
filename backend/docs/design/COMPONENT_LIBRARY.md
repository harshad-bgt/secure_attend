# Component Library Guidelines

## 1. Buttons
- **Primary**: Solid background (Brand Primary), white text. Used for main actions (Login, Mark Attendance).
- **Secondary**: Outlined or soft background. Used for alternative actions.
- **Destructive**: Solid red background. Used for deletions or session ending.
- **Icon Buttons**: Circular or square buttons containing only an icon.

## 2. Cards
- Must have large border radius (16px) and Level 1 elevation.
- Internal padding must be consistently `md` (16px) or `lg` (24px).

## 3. Inputs
- **React**: Outlined inputs with floating labels or clear top labels. Validation text appears below in red.
- **Flutter**: `TextFormField` with `OutlineInputBorder` (Material 3).

## 4. Notifications / Toasts
- **Success**: Green accent, check icon.
- **Error**: Red accent, warning icon.
- **Info**: Blue accent, info icon.
- Duration: 3-5 seconds.

## 5. Skeleton Loaders
- Gray, pulsing shapes matching the exact dimensions of the content they are replacing.

## 6. Dialogs
- Centered on screen.
- Scrim (backdrop) opacity at 50% dark gray.
- Must contain a clear title, descriptive body text, and explicit action buttons (e.g., "Cancel" and "Confirm").
