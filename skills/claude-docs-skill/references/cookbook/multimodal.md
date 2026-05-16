# Multimodal Capabilities

Working with images, PDFs, and documents in Claude.

## Vision

Claude can analyze images passed as base64 or URLs.

### When to Use
- Image description and analysis
- Chart/graph interpretation
- Document/receipt OCR
- UI screenshot analysis
- Visual Q&A

### Supported Formats
- JPEG, PNG, GIF, WebP
- Max 20MB per image
- Multiple images per request supported

### Implementation

**Base64:**
```python
{
    "type": "image",
    "source": {
        "type": "base64",
        "media_type": "image/jpeg",
        "data": "<base64-encoded-data>"
    }
}
```

**URL:**
```python
{
    "type": "image",
    "source": {
        "type": "url",
        "url": "https://example.com/image.jpg"
    }
}
```

### Best Practices
- Place images before text questions for best results
- Be specific about what to analyze
- For multiple images, reference them by position ("first image", "second image")
- Resize large images to reduce tokens (Claude downscales anyway)

→ Source: `multimodal/` directory

## PDF Support

Native PDF processing without external tools.

### When to Use
- Document Q&A
- Contract analysis
- Report summarization
- Form extraction

### Implementation
```python
{
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": "<base64-encoded-pdf>"
    }
}
```

### Considerations
- PDFs are rendered as images internally
- Text-heavy PDFs: consider extracting text for efficiency
- Complex layouts: vision approach handles better
- Large PDFs: split into sections or summarize hierarchically

→ Source: `misc/pdf_upload_summarization.ipynb`

## Vision + Tools

Combine image analysis with tool calling.

### Use Cases
- Analyze chart → extract data → perform calculations
- Read receipt → call expense API
- Analyze UI screenshot → generate test code

### Pattern
Include image in user message content alongside tool definitions. Claude can reference image content when deciding tool calls.

→ Source: `tool_use/vision_with_tools.ipynb`

## Reading Charts and Graphs

Claude can interpret visual data representations.

### What Works Well
- Bar charts, line graphs, pie charts
- Tables in images
- Diagrams with clear labels
- Infographics

### What's Challenging
- Very dense scatter plots
- Small text/labels
- 3D visualizations
- Poor image quality

### Tips
- Ask for specific data points
- Request trend descriptions
- Have Claude explain its interpretation
- Cross-validate extracted numbers when precision matters

## Document Processing Best Practices

1. **Format selection:**
   - Structured text → plain text in message
   - Layout matters → PDF/image
   - Forms → image for visual layout

2. **Chunking long documents:**
   - Split at natural boundaries (sections, pages)
   - Maintain context with overlap
   - Consider hierarchical summarization

3. **Prompt design:**
   - Specify output format explicitly
   - Ask for quotes/citations to ground responses
   - Use structured extraction for forms

4. **Quality vs. efficiency:**
   - Vision: higher accuracy for complex layouts
   - Text extraction: lower cost, faster
   - Hybrid: extract text, fall back to vision for complex pages
