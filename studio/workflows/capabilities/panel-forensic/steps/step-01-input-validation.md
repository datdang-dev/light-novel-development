---
name: 'step-01-input-validation'
description: 'Validate input image and identify page for forensic analysis'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/panel-forensic'
thisStepFile: './step-01-input-validation.md'
nextStepFile: './step-02-layout-analysis.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
templateFile: '{workflow_path}/templates/forensic-report-template.md'
---

# Step 1: Input Validation

## STEP GOAL

Validate the input image, confirm it's readable, and establish page identification metadata for the forensic analysis session.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 NEVER proceed without viewing the actual image
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST speak in Vietnamese

### Role Reinforcement

- ✅ You are a forensic analyst preparing to examine visual evidence
- ✅ Maintain clinical, precise approach
- ✅ We engage in collaborative dialogue

### Step-Specific Rules

- 🎯 Focus only on validation and identification
- 🚫 FORBIDDEN to begin analysis before validation complete
- 💬 Confirm all inputs with user before proceeding

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly.

### 1. Request Input Information

If not already provided, ask user for:

```
"Xin chào! Để bắt đầu phân tích forensic, mình cần:

1. **Đường dẫn hình ảnh** hoặc page range (ví dụ: `page_001.jpg` hoặc `001-005`)
2. **Tên manga** (để đặt tên file output)
3. **Hướng đọc** (mặc định: phải-sang-trái)
4. **Director Notes** (nếu có yêu cầu soi chi tiết nào đặc biệt)

Vui lòng cung cấp thông tin!"
```

### 2. Validate Image File

Once path provided:

**CRITICAL - ZERO ASSUMPTION PROTOCOL:**

```
1. Use `view_file` tool to ACTUALLY SEE the image
2. NEVER assume content without viewing
3. If cannot view, STOP and request direct upload
```

Validate:

- [ ] Image file exists and is readable
- [ ] Format is supported (jpg, jpeg, png, webp)
- [ ] Image loads correctly

### 3. Initial Visual Assessment

After viewing image, document:

```markdown
## Page Identification

**Manga:** {manga_name}
**Page:** {page_num}
**Image Path:** {file_path}
**Reading Direction:** {right-to-left / left-to-right}

### Initial Assessment
- **Resolution:** {width x height}
- **Panel Count (initial):** {estimated count}
- **Page Type:** {standard / splash / double-page}
- **Content Rating:** {SFW / NSFW / R18}
- **Director Notes:** {User vision/requests}
```

### 4. Create Output File

Initialize output file at `{outputFile}` with frontmatter:

```markdown
---
manga: "{manga_name}"
page: {page_num}
created: "{current_date}"
stepsCompleted: ['step-01-input-validation']
status: IN_PROGRESS
---

# Forensic Analysis: {manga_name} - Page {page_num}

## Page Identification

{Insert validation data from step 3}

---
```

### 5. Present MENU OPTIONS

Display:

```
"✅ Image validated thành công!

**Thông tin:**
- Manga: {manga_name}
- Page: {page_num}
- Panels (sơ bộ): {count}

**Tiếp theo:** Layout analysis chi tiết

**Chọn:** [C] Continue to Layout Analysis"
```

#### Menu Handling Logic

- IF C: Update frontmatter với stepsCompleted, then load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN image is validated, output file is created with proper frontmatter, will you load and execute `{nextStepFile}`.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- Image actually viewed using view_file tool
- All metadata collected (manga name, page, direction)
- Output file created with proper frontmatter
- Initial panel count estimated
- User confirms validation

### ❌ SYSTEM FAILURE

- Not viewing the actual image file
- Assuming content without visual confirmation
- Proceeding without user-confirmed metadata
- Not creating output file with frontmatter
- Skipping to analysis without validation

**Master Rule:** NEVER assume. Always view. Always confirm.
