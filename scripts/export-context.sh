#!/bin/bash
echo "��� Exporting codebase to markdown..."
OUTPUT_DIR="docs/context"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/codebase_${TIMESTAMP}.md"
mkdir -p "$OUTPUT_DIR"

echo "# NotebookLM Video Generator - Complete Codebase" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "Generated: $(date)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Project Structure" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
tree -L 4 -I 'node_modules|venv|__pycache__|.git|dist' >> "$OUTPUT_FILE" 2>/dev/null || find . -type d -not -path "*/node_modules/*" -not -path "*/venv/*" -not -path "*/.git/*" | head -50 >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Backend Code" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
for file in $(find backend/app -name "*.py" 2>/dev/null); do
    echo "### \`${file}\`" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo '```
    cat "$file" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Frontend Code" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
for file in $(find frontend/src -name "*.tsx" -o -name "*.ts" 2>/dev/null); do
    echo "### \`${file}\`" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo '```
    cat "$file" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Remotion Code" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
for file in $(find remotion/src -name "*.tsx" -o -name "*.ts" 2>/dev/null); do
    echo "### \`${file}\`" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo '```
    cat "$file" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Config Files" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
for file in backend/requirements.txt frontend/package.json remotion/package.json .gitignore README.md PROJECT_PLAN.md PROGRESS.md; do
    if [ -f "$file" ]; then
        echo "### \`${file}\`" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo '```
        cat "$file" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done
echo "✅ Exported to: $OUTPUT_FILE"
echo "��� Size: $(du -h "$OUTPUT_FILE" | cut -f1)"
