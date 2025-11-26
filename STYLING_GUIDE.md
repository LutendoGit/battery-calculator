# Styling & PDF Export Guide

## What's New ✨

### 1. **Attractive Color Scheme**
- **Primary Gradient**: Purple to darker purple (#667eea → #764ba2)
- **Background**: Full-screen gradient for a modern look
- **Cards**: White cards with rounded corners and smooth shadows
- **Hover Effects**: Cards lift up and shadows deepen on hover

### 2. **Enhanced Typography**
- Modern font: Segoe UI with fallbacks
- Bold headings with text shadow for depth
- Better spacing and readability
- Responsive design for all screen sizes

### 3. **PDF Export Feature**
- **One-click export**: Click "Export as PDF" button on results page
- **Uses html2pdf.js**: No server-side processing needed
- **Automatic filename**: `battery-design-result.pdf`
- **Print-optimized**: Buttons hidden in PDF view

### 4. **Color Palette Used**
```
Primary Purple: #667eea
Dark Purple: #764ba2
Light Gray: #f5f5f5
Dark Text: #333
Success/Buttons: Purple gradient
```

### 5. **Button Features**
- **Calculate Button**: Primary gradient with hover scale effect
- **Export PDF**: Success-styled button with icon
- **Back Button**: Secondary gray with hover effects
- All buttons have smooth transitions and hover feedback

## How to Use PDF Export

1. Fill in the calculator form on the home page
2. Click "Calculate Pack" or "Calculate Bank"
3. On the results page, click **"Export as PDF"** button
4. PDF automatically downloads to your Downloads folder

## Customization Tips

To change colors, edit the CSS variables in both templates:
```css
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}
```

Or modify:
- `.card-title { color: #667eea; }` - Title colors
- `border-left: 4px solid #667eea;` - Accent borders
- Button gradients in `.btn-primary` and `.btn-success` classes
