import os
import json
import glob
from pathlib import Path

# Absolute paths
REPO_ROOT = Path("/home/datdang/working/lnd_dev")
ARTIFACT_DIR = REPO_ROOT / "_out_lnd" / "gooner-alchemist" / "I_Will_Collect_Your_Semen_Series" / "artifact"
OUTPUT_HTML = ARTIFACT_DIR / "full-novel-reader.html"

# Mapping & Sorting definitions
FILE_ORDER = {
    "prose_canon_ch1.json": 1,
    "prose_canon_ch2.json": 2,
    "prose_canon_ch3.json": 3,
    "prose_canon_ch4.json": 4,
    "prose_bonus.json": 5
}

CHAPTER_TITLES = {
    "prose_canon_ch1.json": "Chapter 01: Khế Ước Bắt Đầu - Khi Cô Nàng Tsundere Mở Lời",
    "prose_canon_ch2.json": "Chapter 02: Gia Tăng Áp Lực - Khoảnh Khắc Lớp Phòng Vệ Rạn Nứt",
    "prose_canon_ch3.json": "Chapter 03: Cực Khoái Đầu Hàng - Lý Trí Chìm Đắm Trong Khoái Cảm",
    "prose_canon_ch4.json": "Chapter 04: Cưỡng Chế Định Mức - Đêm Nhồi Tinh Lấp Đầy Tử Cung",
    "prose_bonus.json": "Bonus Chapter: Đêm Thu Hoạch Mất Kiểm Soát"
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tui Sẽ Vắt Kiệt Tinh Trùng Từ 2 Hòn Dái Của Chú! - Full Novel Reader</title>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..700;1,400..700&family=Lora:ital,wght@0,400..700;1,400..700&family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #080410;
            --bg-card: rgba(20, 15, 35, 0.45);
            --bg-sidebar: rgba(11, 7, 20, 0.85);
            --border-color: rgba(255, 0, 127, 0.15);
            --text-primary: #f2eaff;
            --text-secondary: #a395be;
            --accent-pink: #ff007f;
            --accent-purple: #b624ff;
            --tsun-blue: #00f0ff;
            --font-garamond: 'EB Garamond', Georgia, serif;
            --font-lora: 'Lora', serif;
            --font-ui: 'Outfit', sans-serif;
            --font-reader: var(--font-lora);
            --sidebar-width: 320px;
        }

        /* Cream Theme */
        body.theme-cream {
            --bg-base: #fdfaf5;
            --bg-card: rgba(245, 238, 226, 0.8);
            --bg-sidebar: #f5ece2;
            --border-color: rgba(190, 130, 90, 0.2);
            --text-primary: #2e1d0f;
            --text-secondary: #735d49;
            --accent-pink: #d9383a;
            --accent-purple: #8e44ad;
            --tsun-blue: #2980b9;
        }

        /* Sepia Theme */
        body.theme-sepia {
            --bg-base: #1a120b;
            --bg-card: rgba(35, 25, 16, 0.7);
            --bg-sidebar: #130d08;
            --border-color: rgba(212, 143, 56, 0.15);
            --text-primary: #e8d0a7;
            --text-secondary: #a69172;
            --accent-pink: #d35400;
            --accent-purple: #9b59b6;
            --tsun-blue: #16a085;
        }

        /* OLED Black Theme */
        body.theme-oled {
            --bg-base: #000000;
            --bg-card: #040404;
            --bg-sidebar: #020202;
            --border-color: rgba(255, 0, 127, 0.25);
            --text-primary: #ffffff;
            --text-secondary: #888888;
            --accent-pink: #ff007f;
            --accent-purple: #b624ff;
            --tsun-blue: #00ffff;
        }

        /* Font Family Classes */
        body.font-garamond { --font-reader: var(--font-garamond); }
        body.font-lora { --font-reader: var(--font-lora); }
        body.font-sans { --font-reader: var(--font-ui); }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: background-color 0.4s cubic-bezier(0.25, 1, 0.5, 1), 
                        color 0.4s cubic-bezier(0.25, 1, 0.5, 1), 
                        border-color 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: var(--font-ui);
            display: flex;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Sidebar Styling */
        aside {
            width: var(--sidebar-width);
            background: var(--bg-sidebar);
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            position: fixed;
            height: 100vh;
            z-index: 100;
            box-shadow: 10px 0 40px rgba(0,0,0,0.6);
        }

        .sidebar-header {
            padding: 30px 24px;
            border-bottom: 1px solid var(--border-color);
            background: linear-gradient(135deg, rgba(255, 0, 127, 0.08), rgba(182, 36, 255, 0.08));
        }

        .sidebar-header h1 {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .sidebar-header h1 span {
            color: var(--accent-pink);
        }

        .sidebar-header p {
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 6px;
            font-weight: 500;
        }

        .chapter-list {
            list-style: none;
            overflow-y: auto;
            flex: 1;
            padding: 20px 12px;
        }

        .chapter-item {
            padding: 14px 18px;
            border-radius: 10px;
            cursor: pointer;
            margin-bottom: 8px;
            border: 1px solid transparent;
            font-weight: 500;
            font-size: 0.95rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .chapter-item:hover {
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-primary);
            border-color: rgba(255, 255, 255, 0.05);
            transform: translateX(4px);
        }

        .chapter-item.active {
            background: linear-gradient(90deg, rgba(255, 0, 127, 0.15), rgba(182, 36, 255, 0.05));
            color: var(--text-primary);
            border-color: var(--border-color);
            box-shadow: inset 4px 0 0 var(--accent-pink);
        }

        @keyframes pulse-badge {
            0% { box-shadow: 0 0 5px rgba(255, 0, 127, 0.4); }
            50% { box-shadow: 0 0 15px rgba(255, 0, 127, 0.8); }
            100% { box-shadow: 0 0 5px rgba(255, 0, 127, 0.4); }
        }

        .chapter-item.custom-chap::after {
            content: "R18";
            background: var(--accent-pink);
            color: #fff;
            font-size: 0.65rem;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            animation: pulse-badge 2s infinite ease-in-out;
        }

        /* Main Content Styling */
        main {
            margin-left: var(--sidebar-width);
            flex: 1;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        /* Top Control Bar */
        .control-bar {
            height: 75px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            background: rgba(8, 4, 16, 0.4);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 90;
        }

        .theme-selectors {
            display: flex;
            gap: 10px;
        }

        .theme-btn {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            border: 2px solid transparent;
            cursor: pointer;
            outline: none;
            transition: transform 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .theme-btn:hover {
            transform: scale(1.2);
        }

        .theme-btn.active {
            border-color: var(--accent-pink);
            transform: scale(1.1);
        }

        .btn-night { background-color: #080410; border-color: rgba(255,255,255,0.2); }
        .btn-cream { background-color: #fdfaf5; border-color: rgba(0,0,0,0.15); }
        .btn-sepia { background-color: #1a120b; border-color: rgba(255,255,255,0.1); }
        .btn-oled { background-color: #000000; border-color: rgba(255,255,255,0.3); }

        .text-controls {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .ctrl-btn {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 7px 14px;
            border-radius: 8px;
            cursor: pointer;
            font-family: var(--font-ui);
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .ctrl-btn:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--accent-pink);
        }

        .ctrl-btn.active {
            background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
            color: white;
            border-color: transparent;
        }

        /* Sensory Affect Dashboard Panel */
        .sensory-panel {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            backdrop-filter: blur(15px);
            border-radius: 16px;
            padding: 24px 30px;
            margin: 35px auto 15px auto;
            max-width: 820px;
            width: 90%;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            box-shadow: 0 15px 45px rgba(0,0,0,0.5);
        }

        .sensory-stat {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .stat-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: var(--text-secondary);
            font-weight: 600;
            display: flex;
            justify-content: space-between;
        }

        .stat-value {
            font-weight: 700;
            color: var(--accent-pink);
        }

        .stat-bar-container {
            height: 10px;
            background: rgba(255, 255, 255, 0.04);
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.01);
        }

        .stat-bar {
            height: 100%;
            border-radius: 6px;
            width: 0%;
            transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .bar-dere {
            background: linear-gradient(90deg, var(--tsun-blue), var(--accent-pink));
        }

        .bar-stroke {
            background: linear-gradient(90deg, var(--accent-purple), var(--accent-pink));
        }

        .stat-tags {
            grid-column: 1 / -1;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            border-top: 1px solid rgba(255,255,255,0.06);
            padding-top: 18px;
            margin-top: 5px;
        }

        .sensory-tag {
            font-size: 0.75rem;
            padding: 5px 12px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 8px;
            transition: transform 0.2s ease;
        }

        .sensory-tag:hover {
            transform: scale(1.05);
        }

        .sensory-tag.olfactory { border-color: rgba(255, 0, 127, 0.3); color: #ff80bf; }
        .sensory-tag.tactile { border-color: rgba(182, 36, 255, 0.3); color: #d699ff; }
        .sensory-tag.visual { border-color: rgba(0, 240, 255, 0.3); color: #99f0ff; }

        /* Reader Area Styling */
        .reader-wrapper {
            flex: 1;
            padding: 40px 20px 100px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .prose-container {
            max-width: 820px;
            width: 100%;
            font-family: var(--font-reader);
            font-size: 1.25rem;
            line-height: 1.95;
            letter-spacing: 0.2px;
            opacity: 1;
            transform: translateY(0);
            transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* Slide-fade effect for butter-smooth loading */
        .prose-container.fade-out {
            opacity: 0;
            transform: translateY(18px);
        }

        .prose-container p {
            margin-bottom: 26px;
            text-align: justify;
        }

        /* Formatting elements */
        .prose-container .dialogue {
            color: #ff80bf;
            font-weight: 500;
            padding: 16px 20px;
            border-left: 4px solid var(--accent-pink);
            margin: 25px 0;
            font-style: italic;
            background: rgba(255, 0, 127, 0.03);
            border-radius: 0 12px 12px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        body.theme-cream .prose-container .dialogue {
            color: #9c1c3f;
            background: rgba(217, 56, 58, 0.05);
            border-left-color: var(--accent-pink);
        }

        .prose-container .sfx {
            color: var(--accent-purple);
            font-weight: 700;
            font-style: italic;
            letter-spacing: 1px;
            display: block;
            margin: 25px 0;
            text-align: center;
            opacity: 0.9;
            font-family: var(--font-ui);
            text-shadow: 0 0 10px rgba(182, 36, 255, 0.2);
        }

        /* Chapter Title Inside Prose Container */
        .prose-header {
            margin-bottom: 45px;
            text-align: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 35px;
            width: 100%;
        }

        .prose-header h2 {
            font-family: var(--font-ui);
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.5px;
        }

        .prose-header .meta {
            font-family: var(--font-ui);
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 12px;
            text-transform: uppercase;
            letter-spacing: 1.2px;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-base);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-pink);
        }

        /* Progress Bar bottom */
        .progress-bar-container {
            position: fixed;
            bottom: 0;
            left: var(--sidebar-width);
            right: 0;
            height: 4px;
            background: rgba(255,255,255,0.02);
            z-index: 101;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-purple), var(--accent-pink));
            width: 0%;
            transition: width 0.1s ease;
        }
    </style>
</head>
<body>

    <!-- SIDEBAR CHAPTER NAVIGATION -->
    <aside>
        <div class="sidebar-header">
            <h1>LND <span>Studio</span></h1>
            <p>Tui Sẽ Vắt Kiệt Tinh Trùng Từ 2 Hòn Dái Của Chú!</p>
        </div>
        <ul class="chapter-list" id="chapterList">
            <!-- Populated via Javascript -->
        </ul>
    </aside>

    <!-- MAIN APP CANVAS -->
    <main>
        <!-- Control Bar -->
        <div class="control-bar">
            <!-- Theme selectors -->
            <div class="theme-selectors">
                <button class="theme-btn btn-night active" onclick="setTheme('night')"></button>
                <button class="theme-btn btn-sepia" onclick="setTheme('sepia')"></button>
                <button class="theme-btn btn-cream" onclick="setTheme('cream')"></button>
                <button class="theme-btn btn-oled" onclick="setTheme('oled')"></button>
            </div>

            <!-- Typography & View Options -->
            <div class="text-controls">
                <button class="ctrl-btn font-select-btn" id="fn-garamond" onclick="setFontFamily('garamond')">EB Garamond</button>
                <button class="ctrl-btn font-select-btn" id="fn-lora" onclick="setFontFamily('lora')">Lora</button>
                <button class="ctrl-btn font-select-btn" id="fn-sans" onclick="setFontFamily('sans')">Sans-serif</button>
                
                <span style="color: var(--border-color); margin: 0 5px;">|</span>
                
                <button class="ctrl-btn" onclick="adjustFontSize(-2)">A-</button>
                <button class="ctrl-btn" onclick="adjustFontSize(2)">A+</button>
            </div>
        </div>

        <!-- Sensory Dashboard Panel -->
        <div class="sensory-panel" id="sensoryPanel">
            <div class="sensory-stat">
                <div class="stat-label">
                    <span>Dere Breakdown (Tsun-Dere)</span>
                    <span class="stat-value" id="valDere">0.0</span>
                </div>
                <div class="stat-bar-container">
                    <div class="stat-bar bar-dere" id="barDere"></div>
                </div>
            </div>

            <div class="sensory-stat">
                <div class="stat-label">
                    <span>Stroking Metric (Arousal)</span>
                    <span class="stat-value" id="valStroke">0/10</span>
                </div>
                <div class="stat-bar-container">
                    <div class="stat-bar bar-stroke" id="barStroke"></div>
                </div>
            </div>

            <div class="stat-tags" id="sensoryTags">
                <!-- Sensory tags populated dynamically -->
            </div>
        </div>

        <!-- Novel Reader Canvas -->
        <div class="reader-wrapper">
            <div class="prose-container" id="proseContainer">
                <div class="prose-header">
                    <h2 id="chapTitle">Chương đang tải...</h2>
                    <div class="meta" id="chapMeta">Trang 0</div>
                </div>
                <div id="proseBody">
                    <!-- Prose text goes here -->
                </div>
            </div>
        </div>

        <!-- Reading Progress Tracker -->
        <div class="progress-bar-container">
            <div class="progress-bar" id="progressBar"></div>
        </div>
    </main>

    <script>
        // EMBEDDED NOVEL DATABASE
        const NOVEL_DATA = {__NOVEL_DATABASE__};

        let currentChapterKey = "";
        let fontSize = 20;

        // Populate Sidebar
        function initSidebar() {
            const list = document.getElementById("chapterList");
            list.innerHTML = "";

            Object.keys(NOVEL_DATA).forEach(key => {
                const chap = NOVEL_DATA[key];
                const li = document.createElement("li");
                li.className = "chapter-item";
                if (chap.is_custom) {
                    li.className += " custom-chap";
                }
                li.innerText = chap.title;
                li.setAttribute("data-key", key);
                li.onclick = () => selectChapter(key);
                list.appendChild(li);
            });
        }

        // Select & Render Chapter
        function selectChapter(key) {
            if (!NOVEL_DATA[key]) return;

            const container = document.getElementById("proseContainer");
            
            // Butter-smooth hardware-accelerated slide-fade out
            container.classList.add("fade-out");

            setTimeout(() => {
                currentChapterKey = key;
                localStorage.setItem("lnd_last_read", key);

                // Update Active Sidebar Link
                document.querySelectorAll(".chapter-item").forEach(item => {
                    if (item.getAttribute("data-key") === key) {
                        item.classList.add("active");
                    } else {
                        item.classList.remove("active");
                    }
                });

                const chap = NOVEL_DATA[key];
                
                // Update Title & Header
                document.getElementById("chapTitle").innerText = chap.title;
                document.getElementById("chapMeta").innerText = `Độ dài: ${chap.word_count} từ | Kiểu: ${chap.is_custom ? "Ngoại Truyện" : "Chương Chính"}`;

                // Render Prose Paragraphs
                const body = document.getElementById("proseBody");
                body.innerHTML = "";

                const paragraphs = chap.content.split("\\n");
                paragraphs.forEach(p => {
                    const cleanP = p.trim();
                    if (!cleanP) return;

                    const pEl = document.createElement("p");
                    
                    // Style Dialogue format
                    if (cleanP.startsWith("「") && cleanP.endsWith("」")) {
                        pEl.className = "dialogue";
                        pEl.innerText = cleanP;
                    }
                    // Style SFX format
                    else if (cleanP.startsWith("***") && cleanP.endsWith("***")) {
                        pEl.className = "sfx";
                        pEl.innerText = cleanP.replace(/\\*\\*\\*/g, "");
                    }
                    else {
                        pEl.innerText = cleanP;
                    }
                    body.appendChild(pEl);
                });

                // Update Sensory Dashboard
                updateSensoryDashboard(chap.sensory_affect);

                // Butter-smooth slide-fade in
                container.classList.remove("fade-out");
                window.scrollTo({ top: 0, behavior: 'smooth' });

            }, 400); // Perfect duration for visual novel slide-fade
        }

        // Update Dashboard Indicators
        function updateSensoryDashboard(affect) {
            const panel = document.getElementById("sensoryPanel");
            
            if (!affect) {
                panel.style.display = "none";
                return;
            }
            panel.style.display = "grid";

            // Dere breakdown
            const dereVal = affect.tsundere_breakdown || 0.0;
            document.getElementById("valDere").innerText = dereVal.toFixed(1);
            document.getElementById("barDere").style.width = `${dereVal * 10}%`;

            // Stroking metric
            const strokeVal = affect.stroking_metric || 0;
            document.getElementById("valStroke").innerText = `${strokeVal}/10`;
            document.getElementById("barStroke").style.width = `${strokeVal * 10}%`;

            // Render tags
            const tagContainer = document.getElementById("sensoryTags");
            tagContainer.innerHTML = "";

            if (affect.olfactory) {
                affect.olfactory.forEach(tag => {
                    const tagEl = document.createElement("div");
                    tagEl.className = "sensory-tag olfactory";
                    tagEl.innerHTML = `👃 ${tag}`;
                    tagContainer.appendChild(tagEl);
                });
            }

            if (affect.tactile) {
                affect.tactile.forEach(tag => {
                    const tagEl = document.createElement("div");
                    tagEl.className = "sensory-tag tactile";
                    tagEl.innerHTML = `🖐️ ${tag}`;
                    tagContainer.appendChild(tagEl);
                });
            }

            if (affect.visual) {
                affect.visual.forEach(tag => {
                    const tagEl = document.createElement("div");
                    tagEl.className = "sensory-tag visual";
                    tagEl.innerHTML = `👁️ ${tag}`;
                    tagContainer.appendChild(tagEl);
                });
            }
        }

        // Adjust Font Size
        function adjustFontSize(delta) {
            fontSize = Math.max(16, Math.min(30, fontSize + delta));
            document.getElementById("proseContainer").style.fontSize = `${fontSize}px`;
            localStorage.setItem("lnd_font_size", fontSize);
        }

        // Set Font Family
        function setFontFamily(font) {
            document.body.classList.remove("font-garamond", "font-lora", "font-sans");
            document.body.classList.add(`font-${font}`);
            
            document.querySelectorAll(".font-select-btn").forEach(btn => {
                if (btn.id === `fn-${font}`) {
                    btn.classList.add("active");
                } else {
                    btn.classList.remove("active");
                }
            });
            localStorage.setItem("lnd_font_family", font);
        }

        // Themes
        function setTheme(theme) {
            document.body.classList.remove("theme-night", "theme-sepia", "theme-cream", "theme-oled");
            document.body.classList.add(`theme-${theme}`);
            document.querySelectorAll(".theme-btn").forEach(btn => {
                if (btn.classList.contains(`btn-${theme}`)) {
                    btn.classList.add("active");
                } else {
                    btn.classList.remove("active");
                }
            });
            localStorage.setItem("lnd_theme", theme);
        }

        // Scroll progress bar
        window.addEventListener("scroll", () => {
            const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById("progressBar").style.width = `${scrolled}%`;
        });

        // Initialize App
        window.onload = () => {
            initSidebar();

            // Load saved settings
            const savedTheme = localStorage.getItem("lnd_theme") || "night";
            setTheme(savedTheme);

            const savedFontFamily = localStorage.getItem("lnd_font_family") || "lora";
            setFontFamily(savedFontFamily);

            const savedFont = localStorage.getItem("lnd_font_size");
            if (savedFont) {
                fontSize = parseInt(savedFont);
                document.getElementById("proseContainer").style.fontSize = `${fontSize}px`;
            }

            // Restore last read chapter
            const lastRead = localStorage.getItem("lnd_last_read");
            const initialKey = (lastRead && NOVEL_DATA[lastRead]) ? lastRead : Object.keys(NOVEL_DATA)[0];
            selectChapter(initialKey);
        };
    </script>
</body>
</html>
"""

def build_full_novel():
    print(f"Reading folder: {ARTIFACT_DIR}")
    
    # Discover all JSON draft prose files
    json_files = glob.glob(str(ARTIFACT_DIR / "prose_*.json"))
    
    # Sort files based on custom mapping
    sorted_files = []
    for filepath in json_files:
        basename = os.path.basename(filepath)
        if basename in FILE_ORDER:
            sorted_files.append((FILE_ORDER[basename], basename, filepath))
        else:
            # Fallback sort for unknown JSON files at the end
            sorted_files.append((99, basename, filepath))
            
    sorted_files.sort()
    
    novel_db = {}
    
    for order, basename, filepath in sorted_files:
        print(f"Loading [{order}]: {basename}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Extract content & details
            prose_content = data.get("prose_content", "") or data.get("content", {}).get("caption", "")
            word_count = data.get("word_count", 0)
            if not word_count:
                word_count = len(prose_content.split())
                
            # Parse sensory metrics (support fallback for older chapters without schema)
            sensory_affect = data.get("sensory_affect", None)
            
            # If older chapter, mock basic metrics for visual UI consistency
            if not sensory_affect:
                sensory_affect = {
                    "tsundere_breakdown": 1.5 if "custom" not in basename else 6.0,
                    "stroking_metric": 3 if "custom" not in basename else 8,
                    "olfactory": ["mùi hoóc-môn đực nhè nhẹ"] if "custom" not in basename else ["mùi dâm dịch khai nồng"],
                    "tactile": ["ma sát nhẹ"] if "custom" not in basename else ["cọ xát bạo liệt"],
                    "visual": ["má hồng hào"] if "custom" not in basename else ["mắt lờ đờ sung sướng"]
                }
                
            is_custom = "custom" in basename
            title = CHAPTER_TITLES.get(basename, basename.replace(".json", "").replace("draft-prose-", "Chương "))
            
            novel_db[basename] = {
                "title": title,
                "content": prose_content,
                "word_count": word_count,
                "is_custom": is_custom,
                "sensory_affect": sensory_affect
            }
        except Exception as e:
            print(f"❌ Error loading {basename}: {e}")

    # Embed novel database into HTML template
    db_json_string = json.dumps(novel_db, ensure_ascii=False, indent=2)
    final_html = HTML_TEMPLATE.replace("{__NOVEL_DATABASE__}", db_json_string)
    
    # Save compiled novel
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"\n🎉 FULL NOVEL COMPILED SUCCESSFULLY!")
    print(f"📂 Saved at: {OUTPUT_HTML}")

if __name__ == "__main__":
    build_full_novel()
