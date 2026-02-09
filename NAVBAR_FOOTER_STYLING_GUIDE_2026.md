# 🎨 UniSinq Navbar & Footer Styling Guide
**Date:** Feb 09, 2026 | **Version:** 1.0 | **Status:** Complete

---

## 🎯 Overview

The navbar and footer have been completely redesigned with UniSinq's brand identity:
- **Color Theme:** Purple, Pink, Cyan gradients on dark background
- **Logo:** High-quality gradient border with glow effect on hover
- **Typography:** Gradient text, bold headers, emoji icons
- **Animations:** Smooth transitions, hover effects, pulse animations
- **Responsive:** Mobile-first design with hamburger menu

---

## 🎨 Color Palette

### Primary Colors
| Element | Color | Hex |
|---------|-------|-----|
| **Primary Background** | Dark Blue-Gray | `#0d1117` |
| **Secondary Background** | Darker Gray | `#161b22` |
| **Accent (Primary)** | Cyan Blue | `#58a6ff` |
| **Accent (Secondary)** | Purple | `#9d4edd` |
| **Accent (Tertiary)** | Pink | `#f72585` |

### Tailwind Equivalents
```
- bg-gradient-to-r from-purple-600 to-pink-600
- text-cyan-400 / text-purple-400 / text-pink-400
- border-purple-500/30
- hover:text-purple-400 / hover:bg-purple-600
```

---

## 📱 Navbar Component

### Location
```
accounts/templates/main_home.html (Lines 29-105)
accounts/templates/base_with_footer.html (Lines 161-229)
```

### Features

#### 1. **Logo Section**
```html
<!-- Logo with Glow Effect -->
<div class="flex items-center space-x-3 group">
    <div class="relative">
        <div class="absolute -inset-0.5 bg-gradient-to-r from-purple-600 to-pink-600 
                    rounded-lg blur opacity-0 group-hover:opacity-75 transition duration-500"></div>
        <img src="{% static 'images/unisinq-logo.png' %}" 
             alt="UniSinq Logo" 
             class="relative h-10 w-10 object-cover rounded-lg shadow-md border border-purple-400/50">
    </div>
    <span class="text-white font-bold text-xl 
                 bg-gradient-to-r from-cyan-400 to-purple-400 
                 bg-clip-text text-transparent">
        UniSinq
    </span>
</a>
```

**Styling Highlights:**
- ✨ **Glow Effect:** Gradient blur on hover (purple→pink)
- 🎯 **Border:** Purple semi-transparent border
- 🌈 **Gradient Text:** Cyan to Purple text gradient
- 📊 **Scale Animation:** Hover scale(105%)

#### 2. **Navigation Links**
```html
<a href="{% url 'main_home' %}" 
   class="hover:text-accent transition flex items-center gap-2">
    <svg class="w-5 h-5">...</svg>
    <span class="text-xs font-medium">Home</span>
</a>
```

**Styling Highlights:**
- 🎨 **Color:** Inherits accent (cyan)
- ⚡ **Icons:** SVG icons next to text labels
- 📱 **Responsive:** Text hidden on mobile
- 🔄 **Hover:** Smooth transition to accent color

#### 3. **Navbar Background**
```css
bg-gradient-to-r from-primary to-purple-900
border-b border-purple-500/30
shadow-lg sticky top-0 z-50
```

**Features:**
- Gradient background (primary → purple)
- Purple border-bottom (semi-transparent)
- Shadow for depth
- Sticky positioning with high z-index

---

## 🦶 Footer Component

### Location
```
accounts/templates/components/footer.html (Lines 1-127)
```

### Structure

#### 1. **Footer Background & Border**
```html
<footer class="bg-gradient-to-b from-[#0d1117] to-[#161b22] 
                border-t-2 border-purple-500/30 py-16 mt-20">
```

**Styling:**
- ⬇️ Gradient: Dark → Slightly lighter dark
- 🎨 Border-top: Purple with opacity
- 📏 Padding: 16px vertical, auto horizontal

#### 2. **Brand Section (Left Column)**
```html
<!-- Logo with Glow Effect -->
<div class="flex items-center space-x-3 mb-4 group">
    <div class="relative">
        <div class="absolute -inset-1 bg-gradient-to-r from-purple-600 to-pink-600 
                    rounded-lg blur opacity-40 group-hover:opacity-100 transition duration-500"></div>
        <img src="{% static 'images/unisinq-logo.png' %}" 
             alt="UniSinq Logo" 
             class="relative h-12 w-12 object-cover rounded-lg shadow-lg border border-purple-500/50">
    </div>
    <div>
        <h3 class="text-xl font-bold text-white">UniSinq</h3>
        <p class="text-[10px] text-purple-400">v1.0</p>
    </div>
</div>
```

**Features:**
- 🌟 Larger logo (12x12) than navbar (10x10)
- 💜 Version number displayed below
- 🎯 Stronger opacity on glow (40→100%)
- 📖 Brand tagline with emoji

#### 3. **Social Links Row**
```html
<div class="flex space-x-3">
    <a href="https://github.com/..." 
       class="w-10 h-10 flex items-center justify-center 
              text-[#8b949e] bg-white/5 
              hover:bg-purple-600 hover:text-white 
              rounded-lg transition-all duration-300 
              transform hover:scale-110" 
       title="GitHub">
        <i class="fab fa-github"></i>
    </a>
    <!-- Repeat for Twitter, LinkedIn, Instagram -->
</div>
```

**Styling:**
- 🔲 Square buttons (10x10)
- 🎨 Background: white/5 → hover color
- 📈 Scale: 100% → 110% on hover
- ⚡ Different colors per platform:
  - GitHub: purple-600
  - Twitter: blue-500
  - LinkedIn: blue-700
  - Instagram: pink-500

#### 4. **Footer Sections (Product, Resources, Legal)**
```html
<h4 class="text-white font-bold mb-4 text-sm flex items-center gap-2">
    <span class="text-purple-400">📦</span>
    Product
</h4>
<ul class="space-y-3">
    <li>
        <a href="..." 
           class="text-[#8b949e] hover:text-purple-400 
                  transition-colors text-sm flex items-center gap-2 group">
            <span class="group-hover:translate-x-1 transition">→</span>
            Features
        </a>
    </li>
    <!-- Repeat for other items -->
</ul>
```

**Styling:**
- 📌 Section Headers:
  - Bold text with emoji icons
  - Product: 📦 Purple
  - Resources: 📚 Pink
  - Legal: ⚖️ Cyan
- 🔗 Links:
  - Arrow animates on hover
  - Text color changes based on section theme
  - Smooth transition (300ms)
- 📐 Spacing: 3 units between items

#### 5. **Newsletter Section**
```html
<div class="max-w-md mx-auto mb-8 
            bg-white/5 backdrop-blur-sm 
            border border-purple-500/30 
            rounded-xl p-6">
    <h4 class="text-white font-bold text-sm mb-3 flex items-center gap-2">
        <span class="text-yellow-400">✉️</span>
        Stay Updated
    </h4>
    <form class="flex gap-2" onsubmit="return handleNewsletterSignup(event)">
        <input type="email" 
               placeholder="Enter your email" 
               class="flex-1 bg-[#1a1f26] 
                      border border-purple-500/30 
                      rounded-lg px-3 py-2 
                      text-[#c9d1d9] text-sm 
                      placeholder-[#8b949e] 
                      focus:border-purple-400 
                      focus:outline-none 
                      focus:ring-1 
                      focus:ring-purple-400/50 
                      transition-all" 
               required>
        <button type="submit" 
                class="bg-gradient-to-r from-purple-600 to-pink-600 
                       hover:from-purple-700 hover:to-pink-700 
                       text-white font-semibold px-4 py-2 
                       rounded-lg text-sm 
                       transition-all transform 
                       hover:scale-105 shadow-lg">
            Subscribe
        </button>
    </form>
    <p class="text-[#8b949e] text-[10px] mt-2">
        💜 We respect your privacy. Unsubscribe at any time.
    </p>
</div>
```

**Features:**
- 🎨 Glass-morphism effect (bg-white/5 + backdrop-blur)
- 📧 Email input with purple focus ring
- 🎯 Gradient subscribe button
- 💬 Privacy notice with heart emoji
- 🔄 Form submission feedback

#### 6. **Bottom Footer**
```html
<div class="border-t border-purple-500/20 pt-8 mt-8">
    <div class="flex flex-col md:flex-row 
                justify-between items-center 
                gap-4 text-center md:text-left">
        <p class="text-[#8b949e] text-xs leading-relaxed">
            &copy; 2025 <span class="text-white font-bold">UniSinq</span>. 
            All rights reserved. | Built with 💜 for students worldwide.
        </p>
        <div class="flex gap-6 text-[#8b949e] text-xs">
            <a href="/status/" class="hover:text-purple-400 transition-colors 
                                      flex items-center gap-1">
                <span>●</span> Status
            </a>
            <!-- Repeat for Security, Accessibility -->
        </div>
    </div>
</div>
```

**Styling:**
- 📍 Bullet separator (●) between links
- 🎨 Hover color: purple-400
- 💜 Logo in bold white
- 📱 Responsive: column on mobile, row on desktop

---

## 🎬 Animations & Transitions

### Hover Effects

#### Logo Glow (Navbar & Footer)
```css
.group:hover .absolute {
    opacity: 0.75 / 1.0;  /* Footer: stronger */
    transition: opacity 500ms;
}
```

#### Link Arrow Animation
```css
.group-hover span {
    transform: translateX(0.25rem);  /* translate-x-1 */
    transition: all 300ms;
}
```

#### Social Icon Scale
```css
button:hover {
    transform: scale(1.1);
    transition: all 300ms;
}
```

#### Button Scale
```css
.hover\:scale-105:hover {
    transform: scale(1.05);
    transition: all 300ms;
}
```

### Continuous Animations

#### Logo Pulse
```css
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

#### Status Indicator
```css
.bg-green-400.animate-pulse {
    /* Green dot that pulses */
    animation: pulse 2s infinite;
}
```

---

## 📐 Responsive Design

### Desktop (≥ md breakpoint)
- Full navbar with all links visible
- Footer grid: 5 columns (1 brand + 4 sections)
- Bottom footer: flex row with space-between

### Mobile (< md breakpoint)
```html
<!-- Mobile Menu Button -->
<button class="md:hidden" id="mobile-menu-btn">
    <svg>Menu Icon</svg>
</button>

<!-- Mobile Menu (hidden by default) -->
<div class="md:hidden hidden" id="mobile-menu">
    <!-- Links in column -->
</div>
```

**Styling:**
- 📱 Hamburger menu icon on mobile
- 📋 Dropdown menu below navbar
- 🔄 Toggle on click
- 📌 Border-top separator
- Full-width links with padding

---

## 🔄 Customization Guide

### Change Primary Accent Color
**Find:** All instances of `from-purple-600` or `to-pink-600`

```html
<!-- Change to blue -->
<div class="bg-gradient-to-r from-blue-600 to-indigo-600">
```

### Update Logo Image
**File:** `static/images/unisinq-logo.png`

```html
<!-- Update src path if needed -->
<img src="{% static 'images/your-logo.png' %}" ... >
```

### Add New Social Links
**Location:** Footer brand section

```html
<a href="https://facebook.com/..." 
   class="w-10 h-10 flex items-center justify-center 
          text-[#8b949e] bg-white/5 
          hover:bg-blue-600 hover:text-white 
          rounded-lg transition-all duration-300 
          transform hover:scale-110" 
   title="Facebook">
    <i class="fab fa-facebook"></i>
</a>
```

### Change Newsletter Email Placeholder
**Find:** `placeholder="Enter your email"`

```html
<input type="email" placeholder="Get updates..." required>
```

---

## ✅ Current Implementation Files

| File | Purpose | Lines |
|------|---------|-------|
| `accounts/templates/main_home.html` | Main feed page navbar | 29-105 |
| `accounts/templates/base_with_footer.html` | Base template navbar | 161-229 |
| `accounts/templates/components/footer.html` | Reusable footer | All |
| `static/images/unisinq-logo.png` | Logo image | - |

---

## 🐛 Troubleshooting

### Logo Not Showing
- ✅ Check image exists: `E:\login\auth_project\static\images\unisinq-logo.png`
- ✅ Verify path: `{% static 'images/unisinq-logo.png' %}`
- ✅ Run: `python manage.py collectstatic` (production)

### Gradient Not Appearing
- ✅ Ensure Tailwind CDN loaded (main_home.html has `<script src="https://cdn.tailwindcss.com"></script>`)
- ✅ Use proper Tailwind syntax: `bg-gradient-to-r from-purple-600 to-pink-600`

### Hover Effects Not Working
- ✅ Ensure `.group` and `group-hover:` classes are paired
- ✅ Verify CSS loaded (no conflicts)

### Mobile Menu Not Toggling
- ✅ JavaScript event listener present in base_with_footer.html
- ✅ Check: `id="mobile-menu-btn"` and `id="mobile-menu"` match

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 09, 2026 | Initial comprehensive styling with gradient logos, purple/pink theme |

---

## 🎯 Next Steps

1. Test responsiveness on all device sizes
2. Verify footer displays on all template pages
3. Test newsletter signup functionality
4. Monitor glow effect performance
5. Consider animation speed preferences (prefers-reduced-motion)

---

**Last Updated:** Feb 09, 2026 | **Author:** UniSinq Development Team
