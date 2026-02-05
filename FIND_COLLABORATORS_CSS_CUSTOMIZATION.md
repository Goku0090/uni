# Find Collaborators - CSS Customization Guide

## Color Theme System

The entire design is built on CSS custom properties (variables) that can be easily customized.

### Current UniSync Theme

```css
:root {
    /* Primary Colors */
    --primary-blue: #2563eb;      /* Action buttons */
    --secondary-blue: #1d4ed8;    /* Button hover */
    --accent-teal: #3AB7BF;       /* UniSync signature */
    
    /* Background Colors */
    --light-bg: #1E1E2F;          /* Main page background */
    --card-bg: #28293E;           /* Card background */
    --card-hover: #2F3144;        /* Card hover state */
    
    /* Text Colors */
    --text-primary: #EAEAEA;      /* Main text */
    --text-secondary: #A0A0B0;    /* Secondary text */
    
    /* Border & Dividers */
    --border-color: #3F4158;      /* Card borders */
}
```

---

## Customization Examples

### 1. Change Accent Color (Easiest)

**Current Teal:** `#3AB7BF`

**To Change:**
```css
:root {
    --accent-teal: #FF6B9D;  /* Change to pink */
}
```

**Affects:**
- Button gradients
- Hover effects
- Badge colors
- Text gradients
- Border colors

**Example - Change to Purple:**
```css
:root {
    --accent-teal: #8B5CF6;  /* Purple */
}
```

---

### 2. Change Background Color

**Current Dark Navy:** `#1E1E2F`

**To Change:**
```css
:root {
    --light-bg: #0F0F1E;  /* Even darker */
}
```

**Results:**
- Entire page background changes
- Increases contrast with cards
- Affects overall darkness level

**Example - Change to True Black:**
```css
:root {
    --light-bg: #000000;
}
```

---

### 3. Change Card Background

**Current:** `#28293E`

**To Change:**
```css
:root {
    --card-bg: #1F2132;  /* Darker cards */
}
```

**Results:**
- All card backgrounds change
- Affects filter tabs background
- Affects search input background

**Example - Lighter Cards:**
```css
:root {
    --card-bg: #34354E;  /* Lighter */
}
```

---

### 4. Create Custom Color Scheme

#### Option A: Warm Theme
```css
:root {
    --light-bg: #2A1810;           /* Warm dark brown */
    --card-bg: #3D2817;            /* Darker brown */
    --card-hover: #4A3820;
    --accent-teal: #FF8C42;        /* Warm orange */
    --primary-blue: #D4511E;       /* Warm red */
    --text-primary: #F5E6D3;       /* Cream */
    --border-color: #5A4530;       /* Brown border */
}
```

#### Option B: Cool Blue Theme
```css
:root {
    --light-bg: #0B1929;           /* Very dark blue */
    --card-bg: #142D4C;            /* Dark blue */
    --card-hover: #1A3A5C;
    --accent-teal: #06B6D4;        /* Cyan */
    --primary-blue: #0EA5E9;       /* Light blue */
    --text-primary: #E0F2FE;       /* Light cyan */
    --border-color: #1E5A7C;       /* Blue border */
}
```

#### Option C: Vibrant Neon
```css
:root {
    --light-bg: #1A1A2E;           /* Dark purple */
    --card-bg: #16213E;            /* Darker purple */
    --card-hover: #0F3460;
    --accent-teal: #00D9FF;        /* Neon cyan */
    --primary-blue: #00FF00;       /* Neon green */
    --text-primary: #00FFFF;       /* Cyan */
    --border-color: #533483;       /* Purple */
}
```

---

## Component-Specific Styling

### 1. Navbar Customization

**Change Navbar Background:**
```css
.navbar {
    background: rgba(45, 45, 68, 0.8);
    /* Change first number for darkness */
}

.navbar {
    background: rgba(20, 20, 40, 0.9);  /* Darker */
}
```

**Change Navbar Backdrop Blur:**
```css
.navbar {
    backdrop-filter: blur(10px);  /* Current */
    backdrop-filter: blur(20px);  /* More blur */
    backdrop-filter: blur(5px);   /* Less blur */
}
```

### 2. Hero Section Customization

**Change Hero Gradient:**
```css
.hero-section {
    background: linear-gradient(135deg, 
        rgba(37, 99, 235, 0.15), 
        rgba(58, 183, 191, 0.1)
    );
}
```

**Make Hero More Prominent:**
```css
.hero-section {
    background: linear-gradient(135deg, 
        rgba(37, 99, 235, 0.3),    /* Increase opacity */
        rgba(58, 183, 191, 0.2)
    );
    padding: 4rem 1.5rem;          /* Increase padding */
}
```

**Add Hero Overlay Image:**
```css
.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('background.jpg');
    opacity: 0.1;
}
```

### 3. Button Customization

**Change Button Gradient:**
```css
.btn-connect {
    background: linear-gradient(135deg, #2563eb, #3AB7BF);
    /* Change to custom colors */
}

.btn-connect {
    background: linear-gradient(135deg, #FF6B9D, #FF1493);  /* Pink */
}
```

**Change Button Radius:**
```css
.btn-connect {
    border-radius: 0.5rem;     /* Current */
    border-radius: 0.25rem;    /* More squared */
    border-radius: 9999px;     /* Fully rounded */
}
```

**Add Button Shadow:**
```css
.btn-connect:hover {
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.5);  /* Bigger */
}
```

### 4. Card Customization

**Change Card Border Radius:**
```css
.collaborator-card {
    border-radius: 1rem;       /* Current */
    border-radius: 0.5rem;     /* More squared */
    border-radius: 1.5rem;     /* More rounded */
}
```

**Change Card Shadow:**
```css
.collaborator-card:hover {
    box-shadow: 0 20px 25px -5px rgba(58, 183, 191, 0.15);
    /* Increase second value for bigger shadow */
    box-shadow: 0 30px 40px -5px rgba(58, 183, 191, 0.25);
}
```

**Add Card Glow Effect:**
```css
.collaborator-card {
    border: 1px solid var(--border-color);
    box-shadow: 0 0 20px rgba(58, 183, 191, 0.05);
}

.collaborator-card:hover {
    box-shadow: 0 0 30px rgba(58, 183, 191, 0.2);
}
```

### 5. Badge Customization

**Change Skill Badge Style:**
```css
.skill-badge {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.2), rgba(58, 183, 191, 0.2));
    /* Make more solid */
    background: linear-gradient(135deg, #2563eb, #3AB7BF);
    color: white;
}
```

**Change Interest Badge Color:**
```css
.interest-badge {
    background-color: rgba(58, 183, 191, 0.1);  /* Current */
    background-color: rgba(58, 183, 191, 0.2);  /* More opaque */
}
```

---

## Animation Customization

### 1. Change Fade-In Speed

```css
.fade-in-up {
    animation: fadeInUp 0.6s ease-out;  /* Current */
}

/* Make faster */
.fade-in-up {
    animation: fadeInUp 0.3s ease-out;
}

/* Make slower */
.fade-in-up {
    animation: fadeInUp 1s ease-out;
}
```

### 2. Change Hover Animation

**Current:**
```css
.collaborator-card:hover {
    transform: translateY(-4px);
    transition: all 0.3s ease;
}
```

**More dramatic:**
```css
.collaborator-card:hover {
    transform: translateY(-8px) scale(1.02);
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

**Subtle:**
```css
.collaborator-card:hover {
    transform: translateY(-2px);
    transition: all 0.2s ease;
}
```

### 3. Add Rotation on Hover

```css
.collaborator-card:hover {
    transform: translateY(-4px) rotate(1deg);
}
```

### 4. Change Pulse Animation

```css
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Faster pulse */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

/* Duration change */
.loading-skeleton {
    animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;  /* Faster */
}
```

---

## Typography Customization

### Change Font

```css
body {
    font-family: 'Inter', sans-serif;  /* Current */
}

/* Change to different font */
body {
    font-family: 'Poppins', sans-serif;
}

body {
    font-family: 'Space Grotesk', sans-serif;
}
```

### Change Text Sizes

```css
.hero-title {
    font-size: 2.5rem;     /* Current */
    font-size: 3rem;       /* Larger */
    font-size: 2rem;       /* Smaller */
}

.card-user-name {
    font-size: 1.125rem;   /* Current */
    font-size: 1.25rem;    /* Larger */
}
```

### Change Font Weights

```css
.card-user-name {
    font-weight: 600;      /* Current */
    font-weight: 700;      /* Bolder */
    font-weight: 500;      /* Lighter */
}
```

---

## Spacing Customization

### Change Card Padding

```css
.collaborator-card {
    padding: 1.5rem;       /* Current */
    padding: 2rem;        /* More spacious */
    padding: 1rem;        /* Compact */
}
```

### Change Section Padding

```css
.search-section {
    padding: 2rem 1.5rem;  /* Current */
    padding: 3rem 2rem;    /* More padding */
}
```

### Change Gap Between Cards

```css
.collaborators-grid {
    gap: 1.5rem;          /* Current */
    gap: 2rem;            /* Bigger gaps */
    gap: 1rem;            /* Smaller gaps */
}
```

---

## Responsive Customization

### Change Mobile Breakpoint

```css
@media (max-width: 768px) {  /* Current */
    .collaborators-grid {
        grid-template-columns: 1fr;
    }
}

/* Change to 1024px */
@media (max-width: 1024px) {
    .collaborators-grid {
        grid-template-columns: 1fr;
    }
}
```

### Change Grid Columns

```css
.collaborators-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    /* minmax(320px, 1fr) = min 320px wide cards */
}

/* Make cards wider */
.collaborators-grid {
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
}

/* Make cards narrower */
.collaborators-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
}
```

---

## Complete Theme Override Example

Here's a complete alternative theme you could apply:

```css
/* Minimalist Light Theme */
:root {
    --primary-blue: #000000;
    --secondary-blue: #333333;
    --accent-teal: #FF0000;
    --light-bg: #FFFFFF;
    --card-bg: #F5F5F5;
    --card-hover: #EFEFEF;
    --text-primary: #000000;
    --text-secondary: #666666;
    --border-color: #DDDDDD;
}

.navbar {
    background: rgba(245, 245, 245, 0.95);
    border-bottom: 1px solid #DDDDDD;
}

.collaborator-card {
    background-color: white;
    border: 1px solid #CCCCCC;
}

/* ... update other components accordingly ... */
```

---

## Testing Your Changes

### Step 1: Edit CSS Variables
```css
:root {
    --accent-teal: #YOUR_COLOR;
}
```

### Step 2: Reload Page
Press `Ctrl+Shift+R` (hard refresh) to clear cache

### Step 3: Check All Elements
- [ ] Buttons show new color
- [ ] Badges show new color
- [ ] Hover effects use new color
- [ ] Gradients include new color

### Step 4: Test Responsive
- [ ] Desktop view looks good
- [ ] Tablet view responsive
- [ ] Mobile view readable

---

## Best Practices

1. **Use CSS Variables** - Don't hardcode colors
2. **Test Contrast** - Ensure text readable
3. **Consistent Gradient** - Use same gradient throughout
4. **Mobile First** - Test on mobile first
5. **Browser Test** - Check on Chrome, Firefox, Safari
6. **Keep Backups** - Save original before major changes
7. **Document Changes** - Note what you modified

---

## Troubleshooting

### Problem: Changes not showing
**Solution:** Hard refresh browser cache
```
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)
```

### Problem: Color looks wrong
**Solution:** Check color format
```
✅ Correct: #3AB7BF
❌ Wrong: 3AB7BF (missing #)
```

### Problem: Gradient doesn't show
**Solution:** Ensure text has `background-clip`
```css
background-clip: text;
-webkit-text-fill-color: transparent;
-webkit-background-clip: text;
```

### Problem: Animation too slow
**Solution:** Decrease animation duration
```css
animation: fadeInUp 0.3s ease-out;  /* Was 0.6s */
```

---

## Quick Color Reference

### Web Safe Colors
- Black: `#000000`
- White: `#FFFFFF`
- Red: `#FF0000`
- Blue: `#0000FF`
- Green: `#00FF00`

### Material Design Colors
- Indigo: `#3F51B5`
- Purple: `#9C27B0`
- Pink: `#E91E63`
- Orange: `#FF9800`
- Teal: `#009688`

### CSS Color Names
```css
background: cornflowerblue;
background: lightseagreen;
background: mediumslateblue;
```

---

## Advanced Customization

### Add Custom Font
```html
<link href="https://fonts.googleapis.com/css2?family=YourFont&display=swap" rel="stylesheet">

<style>
body {
    font-family: 'YourFont', sans-serif;
}
</style>
```

### Add Background Pattern
```css
body {
    background-image: 
        repeating-linear-gradient(
            45deg,
            #1E1E2F,
            #1E1E2F 10px,
            #252538 10px,
            #252538 20px
        );
}
```

### Add Glassmorphism
```css
.card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
```

---

## Conclusion

The Find Collaborators page is fully customizable through CSS variables. You can:

- ✅ Change colors instantly
- ✅ Adjust spacing and sizing
- ✅ Modify animations
- ✅ Update typography
- ✅ Create complete themes

All changes are non-breaking and can be reverted by resetting CSS variables to default values.

**Happy customizing! 🎨**
