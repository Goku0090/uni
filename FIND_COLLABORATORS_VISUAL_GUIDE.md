# Find Collaborators - Visual Design Guide

## 🎨 Design System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    UniSync Find Collaborators                    │
│                         Design System                            │
└─────────────────────────────────────────────────────────────────┘

COLOR PALETTE
═════════════════════════════════════════════════════════════════

Primary Colors:
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   #2563eb   │  │   #1d4ed8   │  │   #3AB7BF   │
│  Blue       │  │  Dark Blue  │  │  Teal       │
│ (Buttons)   │  │ (Hover)     │  │ (Accent)    │
└─────────────┘  └─────────────┘  └─────────────┘

Background Colors:
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   #1E1E2F   │  │   #28293E   │  │   #2F3144   │
│  Main BG    │  │  Card BG    │  │  Card Hover │
│ (Pages)     │  │ (Default)   │  │ (Hover)     │
└─────────────┘  └─────────────┘  └─────────────┘

Text Colors:
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   #EAEAEA   │  │   #A0A0B0   │  │   #3F4158   │
│  Primary    │  │  Secondary  │  │  Borders    │
│ (Headings)  │  │ (Meta text) │  │ (Lines)     │
└─────────────┘  └─────────────┘  └─────────────┘
```

---

## 📐 Layout Structure

### Responsive Grid System

```
DESKTOP (1200px+)
═════════════════════════════════════════════════════════════════
┌──────────────────────────────────────────────────────────────┐
│ Navbar                                                         │
├──────────────────────────────────────────────────────────────┤
│ Hero Section                                                   │
├──────────────────────────────────────────────────────────────┤
│ Search & Filters                                              │
├──────────────────────────────────────────────────────────────┤
│  Results | Found X            [Grid] [List]                  │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │   Card 1   │  │   Card 2   │  │   Card 3   │   3 cols    │
│  └────────────┘  └────────────┘  └────────────┘             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │   Card 4   │  │   Card 5   │  │   Card 6   │             │
│  └────────────┘  └────────────┘  └────────────┘             │
└──────────────────────────────────────────────────────────────┘


TABLET (768px - 1024px)
═════════════════════════════════════════════════════════════════
┌──────────────────────────────────────────────────────────────┐
│ Navbar (Collapsed)                                             │
├──────────────────────────────────────────────────────────────┤
│ Hero Section (Smaller)                                         │
├──────────────────────────────────────────────────────────────┤
│ Search & Filters                                              │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │      Card 1         │  │      Card 2         │  2 cols   │
│  └─────────────────────┘  └─────────────────────┘           │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │      Card 3         │  │      Card 4         │           │
│  └─────────────────────┘  └─────────────────────┘           │
└──────────────────────────────────────────────────────────────┘


MOBILE (< 768px)
═════════════════════════════════════════════════════════════════
┌──────────────────────────────────────────────────────────────┐
│ Navbar (Mobile)                                                │
├──────────────────────────────────────────────────────────────┤
│ Hero Section (Mobile)                                          │
├──────────────────────────────────────────────────────────────┤
│ Search & Filters                                              │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────┐             │
│  │              Card 1                        │             │
│  │                                            │  1 col      │
│  └────────────────────────────────────────────┘             │
│  ┌────────────────────────────────────────────┐             │
│  │              Card 2                        │             │
│  └────────────────────────────────────────────┘             │
│  ┌────────────────────────────────────────────┐             │
│  │              Card 3                        │             │
│  └────────────────────────────────────────────┘             │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎯 Component Details

### Navbar Component

```
┌─────────────────────────────────────────────────────────────────┐
│  [Logo]                                   [Nav Links]            │
│  UniSync                                                         │
│                                    Home | Profile | Post | Messages
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
  ↑
  Sticky Position
  Dark background with 80% opacity
  Backdrop blur effect (10px)
  1px border bottom (light gray)
```

### Hero Section Component

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│        Find Your Perfect Collaborators                          │
│        ────────────────────────────────  (Gradient text)       │
│                                                                 │
│  Connect with talented students who share your                │
│  interests and skills. Build amazing together.                │
│                                                                 │
│                    (Gradient background)                       │
│                    (135deg: Blue → Teal)                       │
└─────────────────────────────────────────────────────────────────┘
  Padding: 3rem vertical, 1.5rem horizontal
  Text align: Center
  Max-width: 600px for subtitle
```

### Search Bar Component

```
┌─────────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────┐  ┌────────────────┐  │
│  │ Search by name, skills, interests... │  │  [Search] 🔍   │  │
│  └──────────────────────────────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

Input:
- Background: #28293E
- Border: 1px solid #3F4158
- Padding: 0.75rem 1.5rem
- Border-radius: 0.75rem
- On focus: Border color → Teal, shadow → Teal glow

Button:
- Background: Linear gradient (Blue → Teal)
- Text: White, bold
- Padding: 0.75rem 2rem
- Border-radius: 0.75rem
- On hover: Lift up 2px, shadow enhancement
```

### Filter Tabs Component

```
┌─────────────────────────────────────────────────────────────────┐
│  [All Collaborators] [MIT] [Stanford] [IIT Delhi] [Other]      │
└─────────────────────────────────────────────────────────────────┘

Tab Style:
- Inactive:
  Background: #28293E
  Border: 1px solid #3F4158
  Color: #A0A0B0
  
- Active:
  Background: rgba(58, 183, 191, 0.2)
  Border: 1px solid #3AB7BF
  Color: #3AB7BF
  
- Hover:
  Border color: #3AB7BF
  Text color: #3AB7BF
```

### Collaborator Card Component

```
┌────────────────────────────────────────────────────────────────┐
│ ═══════════════════════════════════════════════════════════    ← Gradient bar
│                                        (animated on hover)      │
│  ┌─────────┐  Name                                              │
│  │         │  College  [✓ Connected]                           │
│  │ Avatar  │                                                    │
│  │  64x64  │                                                    │
│  └─────────┘                                                    │
│                                                                 │
│  Bio text preview up to 20 words truncated...                 │
│                                                                 │
│  SKILLS                                                         │
│  [Python] [React] [TypeScript] [+2]                           │
│                                                                 │
│  INTERESTS                                                      │
│  [Web Development] [Open Source]                              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐  ┌────────────────────┐               │
│  │  View Profile      │  │  + Connect         │               │
│  └────────────────────┘  └────────────────────┘               │
└────────────────────────────────────────────────────────────────┘

Card Style:
- Background: #28293E
- Border: 1px solid #3F4158
- Border-radius: 1rem
- Padding: 1.5rem
- On hover:
  - Transform: translateY(-4px)
  - Background: #2F3144
  - Border color: #3AB7BF
  - Shadow: 0 20px 25px rgba(58, 183, 191, 0.15)
  - Top border animates from left to right
```

### Badge Components

```
Skill Badge:
┌──────────────────┐
│ [Python] [React] │  Blue gradient background
│ [+2 more]        │  Color: Teal text
└──────────────────┘  Border: 1px solid rgba(58, 183, 191, 0.3)

Interest Badge:
┌──────────────────┐
│ [Web Dev]        │  Teal semi-transparent background
│ [AI & ML]        │  Color: Teal text
└──────────────────┘  Border: 1px solid rgba(58, 183, 191, 0.2)

Connection Status:
┌──────────────────┐
│ [✓ Connected]    │  Green background for connected
│ [○ Pending]      │  Amber background for pending
└──────────────────┘  Small badge, 0.75rem padding
```

### Button Styles

```
Connect Button (Primary):
┌──────────────────────┐
│  + Connect           │  Background: Blue → Teal gradient
│                      │  Text: White, 600 weight
└──────────────────────┘  Padding: 0.75rem 1rem
                          On hover: Lift (-2px), shadow
                          
View Profile Button (Secondary):
┌──────────────────────┐
│  View Profile        │  Background: Dark (#28293E)
│                      │  Border: 1px solid #3F4158
└──────────────────────┘  Text: Teal
                          On hover: Teal background, darker border
```

---

## 🎬 Animation Specifications

### Fade In Animation
```
Duration: 0.6s
Easing: ease-out
From:   opacity: 0, translateY(20px)
To:     opacity: 1, translateY(0px)
Applied to: All cards on load
```

### Hover Animation
```
Duration: 0.3s
Easing: cubic-bezier(0.4, 0, 0.2, 1)
Transform: translateY(-4px)
Shadow: Enhanced
Border: Color to teal
```

### Top Border Animation
```
Duration: 0.3s
Origin: Left to right
Scale: 0 → 1
Applied to: Card top border on hover
```

### Pulse Animation (Loading)
```
Duration: 2s
Loop: Infinite
Opacity: 1 → 0.5 → 1
Applied to: Loading skeleton elements
```

---

## 📏 Spacing System

```
Base Unit: 0.25rem (4px)

Padding Scale:
- xs: 0.25rem (4px)
- sm: 0.5rem (8px)
- md: 1rem (16px)
- lg: 1.5rem (24px)
- xl: 2rem (32px)
- 2xl: 3rem (48px)

Gaps Between Elements:
- Cards: 1.5rem (24px)
- Sections: 2rem (32px)
- Card padding: 1.5rem (24px)
- Input padding: 0.75rem (12px)
```

---

## 🔤 Typography

```
Font Family: Inter (sans-serif)

Font Scale:
- Base: 1rem (16px)
- sm: 0.875rem (14px)
- xs: 0.75rem (12px)
- lg: 1.125rem (18px)
- xl: 1.5rem (24px)
- 2xl: 2.5rem (40px)

Weight Hierarchy:
- Regular: 400 (Body text)
- Medium: 500 (Labels, tags)
- Semibold: 600 (Card titles, buttons)
- Bold: 700 (Section titles)
- Extrabold: 800 (Hero title)

Line Height:
- Tight: 1.2
- Normal: 1.5
- Relaxed: 1.75

Letter Spacing:
- Normal: 0
- Tight: -0.01em
```

---

## 🎨 Visual States

### Button States

```
DEFAULT (Idle):
┌─────────────────┐
│  + Connect      │  Gradient fill
└─────────────────┘  Normal shadow

HOVER:
┌─────────────────┐
│  + Connect      │  Elevated position
└─────────────────┘  Enhanced shadow

ACTIVE (Click):
┌─────────────────┐
│  + Connect      │  Slight scale down
└─────────────────┘  Additional feedback

DISABLED:
┌─────────────────┐
│  + Connect      │  Opacity 0.5
└─────────────────┘  No hover effect
```

### Card States

```
DEFAULT (Idle):
┌─────────────────┐
│   Card          │  Subtle border
│   Content       │  Slight shadow
└─────────────────┘

HOVER:
┌─────────────────┐
│ ═══════════════ │  Gradient bar appears
│   Card          │  Lifted position
│   Content       │  Enhanced shadow
└─────────────────┘  Border color changes

ACTIVE (Clicked):
┌─────────────────┐
│   Card          │  Scale feedback
│   Content       │  Brief highlight
└─────────────────┘
```

---

## 📱 Responsive Breakpoints

```
Mobile: < 640px
┌──────────────────────┐
│ Full width cards     │
│ Single column        │
│ Larger touch targets │
│ Stacked navigation   │
└──────────────────────┘

Tablet: 640px - 1024px
┌────────────────┬────────────────┐
│ 2 column grid  │ Medium padding  │
│ Balanced nav   │ Medium cards    │
└────────────────┴────────────────┘

Desktop: 1024px+
┌─────────────┬─────────────┬─────────────┐
│ 3 column    │ Full nav    │ Large cards │
└─────────────┴─────────────┴─────────────┘
```

---

## 🌈 Color Combinations

### Gradients Used

**Primary Gradient (Buttons):**
```
Direction: 135deg
From: #2563eb (Blue)
To: #3AB7BF (Teal)
```

**Hero Title Gradient:**
```
Direction: 135deg
From: #3AB7BF (Teal)
Via: #2563eb (Blue)
To: #3AB7BF (Teal)
```

**Skill Badge Gradient:**
```
Direction: 135deg
From: rgba(37, 99, 235, 0.2)
To: rgba(58, 183, 191, 0.2)
With text color: #3AB7BF
```

---

## ✨ Special Effects

### Backdrop Blur
```
Navbar:
filter: blur(10px)
Effect: Glassmorphism appearance
Opacity: 80% background

Cards:
No blur, solid background
```

### Shadows

**Subtle Shadow (Default):**
```
Box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1)
```

**Medium Shadow (Hover):**
```
Box-shadow: 0 20px 25px -5px rgba(58, 183, 191, 0.15)
```

**Glow Shadow:**
```
Box-shadow: 0 0 30px rgba(58, 183, 191, 0.2)
```

---

## 📐 Icon Usage

```
Navigation Icons:
- Home: House icon
- Profile: User circle icon
- Post: Plus icon
- Messages: Chat bubble icon

Card Icons:
- View Profile: Info icon
- Connect: Plus icon
- Skills: Tag icon

Search & Filter:
- Search: Magnifying glass
- Filter: Funnel icon
- View Toggle: Grid / List icons
```

---

## 🎯 Design Principles

1. **Hierarchy** - Clear visual order guides user attention
2. **Consistency** - Same components styled uniformly
3. **Feedback** - Every action has visual response
4. **Accessibility** - Adequate contrast, touch-friendly
5. **Performance** - Optimized animations, minimal repaints
6. **Responsive** - Adapts gracefully to all screen sizes
7. **Brand Alignment** - Matches UniSync identity

---

## 🎨 Accessibility

```
Color Contrast:
- Text on background: AA compliant (4.5:1 minimum)
- UI components: AA compliant
- Focus states: Clearly visible

Touch Targets:
- Minimum: 44px × 44px
- Card buttons: 44px+ height

Keyboard Navigation:
- Tab through all interactive elements
- Enter/Space to activate buttons
- Proper focus indicators
```

---

## 📸 Visual Examples

### Light Theme Alternative
If you wanted to create a light theme version:
```
Background:    #FFFFFF
Card:          #F5F5F5
Text Primary:  #000000
Text Secondary:#666666
Accent:        #FF6B9D (Pink instead of Teal)
Border:        #CCCCCC
```

### Dark Plus Theme
A more extreme dark theme:
```
Background:    #0A0E27
Card:          #141829
Accent:        #00FFFF (Cyber cyan)
Text:          #FFFFFF
Border:        #2A2E42
```

---

## 🖌️ Design Tokens

```json
{
  "colors": {
    "primary": "#2563eb",
    "secondary": "#1d4ed8",
    "accent": "#3AB7BF",
    "background": "#1E1E2F",
    "surface": "#28293E",
    "text": {
      "primary": "#EAEAEA",
      "secondary": "#A0A0B0"
    },
    "border": "#3F4158"
  },
  "typography": {
    "fontFamily": "Inter, sans-serif",
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.5rem"
    }
  },
  "spacing": {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem"
  },
  "borderRadius": {
    "sm": "0.375rem",
    "md": "0.75rem",
    "lg": "1rem"
  }
}
```

---

## 🎬 Animation Timeline

```
Page Load:
0ms     → Page appears
300ms   → First cards fade in
600ms   → All cards visible
        → User can interact

Card Hover:
0ms     → Mouse enters
150ms   → Border color transitions
200ms   → Shadow expands
300ms   → Animation complete

Button Click:
0ms     → Click registered
50ms    → Button scales
100ms   → Action processes
300ms   → Animation resets
```

---

## 📋 Design Checklist

- [x] Color system defined
- [x] Layout responsive
- [x] Typography consistent
- [x] Spacing uniform
- [x] Components styled
- [x] Animations smooth
- [x] Accessibility met
- [x] Brand aligned
- [x] Performance optimized
- [x] Browser tested

---

This visual design guide provides the complete specification for the Find Collaborators interface, enabling consistent implementation and future enhancements.

**End of Visual Design Guide** ✨
