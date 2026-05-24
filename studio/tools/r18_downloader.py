#!/usr/bin/env python3
"""
LND Studio Universal R18 Downloader & Scraper Tool
Supports:
1. Syosetu Nocturne/Moonlight Novels (Scrapes full chapters to structured Markdown)
2. Hitomi.la (Delegates to node-hitomi downloader script)
3. nhentai (Delegates to nhentai-downloander)
4. Telegraph / Teletype (Directly downloads all image assets)
"""

import sys
import os
import re
import json
import subprocess
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Style/Console helpers
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, status="info"):
    icon = "🔍"
    color = Colors.BLUE
    if status == "success":
        icon = "✅"
        color = Colors.GREEN
    elif status == "warning":
        icon = "⚠️"
        color = Colors.YELLOW
    elif status == "error":
        icon = "💥"
        color = Colors.FAIL
    print(f"{color}{Colors.BOLD}{icon} {message}{Colors.ENDC}")

def clean_filename(title):
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', title)[:200].strip()

# ---------------------------------------------------------------------------
# 1. SYOSETU NOVEL DOWNLOADER
# ---------------------------------------------------------------------------
def download_syosetu_novel(novel_id, output_base):
    print_status(f"Starting Syosetu R18 Novel scrape for ID: {novel_id}", "info")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    cookies = {'over18': 'yes'}
    
    # Try different domains
    domains = [
        "novel18.syosetu.com",
        "noc.syosetu.com",
        "mnlt.syosetu.com",
        "mid.syosetu.com"
    ]
    
    html_text = ""
    domain_used = ""
    for dom in domains:
        url = f"https://{dom}/{novel_id}/"
        try:
            r = requests.get(url, cookies=cookies, headers=headers, timeout=15)
            if r.status_code == 200:
                html_text = r.text
                domain_used = dom
                break
        except Exception as e:
            pass
            
    if not html_text:
        print_status(f"Failed to fetch novel metadata for ID {novel_id} across all domains.", "error")
        return False
        
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # Get Title and Writer
    title_elem = soup.find('h1') or soup.find(class_='novel_title') or soup.find(class_='p-novel__title')
    title = title_elem.text.strip() if title_elem else f"Syosetu Novel {novel_id}"
    
    writer_elem = soup.find(class_='novel_writername') or soup.find(class_='p-novel__author')
    writer = writer_elem.text.replace("作者：", "").strip() if writer_elem else "Unknown"
    
    synopsis_elem = soup.find(id='novel_ex') or soup.find(class_='p-novel__summary')
    synopsis = synopsis_elem.text.strip() if synopsis_elem else ""
    
    print_status(f"Title: {title}", "success")
    print_status(f"Author: {writer}", "info")
    
    novel_dir = os.path.join(output_base, clean_filename(title))
    os.makedirs(novel_dir, exist_ok=True)
    
    # Check if serialized or short story
    chapter_links = re.findall(rf'href=\"(/{novel_id}/\d+/)\"', html_text)
    
    metadata = {
        "novel_id": novel_id,
        "title": title,
        "author": writer,
        "synopsis": synopsis,
        "domain": domain_used,
        "type": "serialization" if chapter_links else "short_story"
    }
    
    if not chapter_links:
        print_status("Detected Short Story (短編). Extracting content directly...", "info")
        # Short story extraction
        body_parts = soup.find_all(class_='js-novel-text')
        content = ""
        for part in body_parts:
            content += part.text + "\n\n"
            
        full_md = f"# {title}\n\n**Author:** {writer}\n\n**Synopsis:**\n{synopsis}\n\n---\n\n{content}"
        
        with open(os.path.join(novel_dir, "novel_full.md"), "w", encoding="utf-8") as f:
            f.write(full_md)
            
        print_status(f"Saved short story to: {novel_dir}/novel_full.md", "success")
    else:
        # Serialized story
        unique_chapters = sorted(list(set(chapter_links)), key=lambda x: int(re.search(r'/(\d+)/', x).group(1)))
        total_chapters = len(unique_chapters)
        print_status(f"Detected Serialization (連載). Found {total_chapters} chapters. Starting crawl...", "info")
        
        chapters_dir = os.path.join(novel_dir, "chapters")
        os.makedirs(chapters_dir, exist_ok=True)
        
        metadata["chapters_count"] = total_chapters
        metadata["chapters"] = []
        
        def download_chapter(idx, ch_url_path):
            ch_num = idx + 1
            ch_url = f"https://{domain_used}{ch_url_path}"
            try:
                r = requests.get(ch_url, cookies=cookies, headers=headers, timeout=15)
                if r.status_code != 200:
                    print_status(f"Failed to fetch chapter {ch_num}: HTTP {r.status_code}", "warning")
                    return None
                    
                ch_soup = BeautifulSoup(r.text, 'html.parser')
                
                # Title
                sub_elem = ch_soup.find(class_='p-novel__title') or ch_soup.find(class_='novel_subtitle')
                subtitle = sub_elem.text.strip() if sub_elem else f"Chapter {ch_num}"
                
                # Preface, body, afterword
                preface = ch_soup.find(class_='p-novel__text--preface')
                body = ch_soup.find(class_='p-novel__text') or ch_soup.find(id='novel_honbun')
                afterword = ch_soup.find(class_='p-novel__text--afterword')
                
                ch_md = f"# {subtitle}\n\n"
                if preface:
                    ch_md += f"*Preface:*\n{preface.text.strip()}\n\n---\n\n"
                if body:
                    ch_md += f"{body.text.strip()}\n"
                if afterword:
                    ch_md += f"\n---\n\n*Afterword:*\n{afterword.text.strip()}\n"
                    
                file_name = f"chapter_{ch_num:03d}.md"
                with open(os.path.join(chapters_dir, file_name), "w", encoding="utf-8") as f:
                    f.write(ch_md)
                    
                return {"number": ch_num, "title": subtitle, "file": file_name}
            except Exception as e:
                print_status(f"Error downloading chapter {ch_num}: {e}", "warning")
                return None

        # Multi-threaded downloading for fast crawls
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(lambda x: download_chapter(x[0], x[1]), enumerate(unique_chapters)))
            
        metadata["chapters"] = [r for r in results if r is not None]
        print_status(f"Successfully downloaded {len(metadata['chapters'])}/{total_chapters} chapters.", "success")
        
    with open(os.path.join(novel_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
        
    print_status(f"Saved metadata & novel package in: {novel_dir}", "success")
    return True

# ---------------------------------------------------------------------------
# 2. TELEGRAPH IMAGE DOWNLOADER
# ---------------------------------------------------------------------------
def download_telegraph_images(url, output_base):
    print_status(f"Scraping Telegraph/Teletype images from: {url}", "info")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print_status(f"HTTP Error {r.status_code} for URL: {url}", "error")
            return False
            
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Get Title
        title_elem = soup.find('title') or soup.find('h1')
        title = title_elem.text.replace(" – Telegraph", "").replace(" — Teletype", "").strip() if title_elem else "Untitled"
        
        print_status(f"Article Title: {title}", "success")
        manga_dir = os.path.join(output_base, clean_filename(title))
        os.makedirs(manga_dir, exist_ok=True)
        
        # Extract images
        img_urls = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if not src:
                continue
            if src.startswith('/'):
                if 'teletype.in' in url:
                    img_urls.append('https://teletype.in' + src)
                else:
                    img_urls.append('https://telegra.ph' + src)
            else:
                img_urls.append(src)
                
        img_urls = list(set(img_urls))
        total_imgs = len(img_urls)
        print_status(f"Found {total_imgs} unique image assets. Starting download...", "info")
        
        def download_img(idx, img_url):
            try:
                res = requests.get(img_url, headers=headers, timeout=15)
                if res.status_code == 200:
                    ext = ".jpg"
                    content_type = res.headers.get('content-type', '')
                    if 'png' in content_type: ext = ".png"
                    elif 'webp' in content_type: ext = ".webp"
                    elif 'gif' in content_type: ext = ".gif"
                    
                    filename = f"page_{idx+1:03d}{ext}"
                    with open(os.path.join(manga_dir, filename), "wb") as f:
                        f.write(res.content)
                    return True
            except Exception as e:
                pass
            return False

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(lambda x: download_img(x[0], x[1]), enumerate(img_urls)))
            
        success_count = sum(1 for r in results if r)
        print_status(f"Successfully downloaded {success_count}/{total_imgs} images.", "success")
        
        # Save a basic info file
        with open(os.path.join(manga_dir, "info.json"), "w", encoding="utf-8") as f:
            json.dump({"title": title, "source": url, "pages": total_imgs}, f, indent=2, ensure_ascii=False)
            
        return True
    except Exception as e:
        print_status(f"Error scraping Telegraph images: {e}", "error")
        return False

# ---------------------------------------------------------------------------
# 5. NOCTURNE NOVEL SEARCHER
# ---------------------------------------------------------------------------
def search_nocturne(query):
    print_status(f"Searching Syosetu Nocturne for: {query}", "info")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    cookies = {'over18': 'yes'}
    
    encoded_query = requests.utils.quote(query)
    url = f"https://noc.syosetu.com/search/search/?word={encoded_query}"
    
    try:
        r = requests.get(url, cookies=cookies, headers=headers, timeout=15)
        if r.status_code != 200:
            print_status(f"Search failed with status code {r.status_code}", "error")
            return False
            
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Try both old and new search result container classes
        novels = soup.find_all(class_='searchresult_box') or soup.find_all(class_='p-search-result')
        if not novels:
            # Fallback to finding links containing /n[a-z0-9]+/
            print_status("No explicit searchresult_box found. Parsing raw links...", "warning")
            links = soup.find_all('a')
            seen = set()
            unique_links = []
            for link in links:
                href = link.get('href', '')
                title = link.text.strip()
                id_match = re.search(r'/(n\d+[a-zA-Z0-9]+)/?', href)
                if id_match:
                    nid = id_match.group(1)
                    if nid not in seen and title and title != "作品情報" and title != "しおりを挟む":
                        seen.add(nid)
                        unique_links.append((title, nid, href))
            if not unique_links:
                print_status("No novel search results found.", "warning")
                return True
                
            print_status(f"Found {len(unique_links)} works matching your query:", "success")
            print("-" * 80)
            for idx, (title, nid, href) in enumerate(unique_links[:20]):
                print(f"{Colors.BOLD}{idx+1}. {title}{Colors.ENDC}")
                print(f"   {Colors.BLUE}ID:{Colors.ENDC} {nid} | {Colors.YELLOW}URL:{Colors.ENDC} {href}")
                print("-" * 80)
            return True

        print_status(f"Found {len(novels)} works matching your query:", "success")
        print("-" * 80)
        
        for idx, box in enumerate(novels[:20]):
            # Title & Link
            title_a = box.find(class_='novel_title') or box.find('a')
            if not title_a:
                continue
            title = title_a.text.strip()
            href = title_a.get('href', '')
            
            # Novel ID extraction
            id_match = re.search(r'/(n\d+[a-zA-Z0-9]+)/', href)
            novel_id = id_match.group(1) if id_match else "unknown"
            
            # Author
            writer_div = box.find(class_='novel_writername') or box.find(class_='p-search-result__author')
            writer = writer_div.text.replace("作者：", "").strip() if writer_div else "Unknown"
            
            # Type (short or serialized)
            type_text = "Unknown Type"
            novel_info = box.text
            if "短編" in novel_info:
                type_text = "Short Story (短編)"
            elif "連載" in novel_info:
                type_text = "Serialized (連載)"
                
            # Synopsis
            synopsis_div = box.find(class_='ex') or box.find(class_='p-search-result__abstract')
            synopsis = synopsis_div.text.strip() if synopsis_div else ""
            if len(synopsis) > 150:
                synopsis = synopsis[:150] + "..."
                
            print(f"{Colors.BOLD}{idx+1}. {title}{Colors.ENDC}")
            print(f"   {Colors.BLUE}ID:{Colors.ENDC} {novel_id} | {Colors.BLUE}Author:{Colors.ENDC} {writer} | {Colors.BLUE}Type:{Colors.ENDC} {type_text}")
            print(f"   {Colors.YELLOW}URL:{Colors.ENDC} {href}")
            if synopsis:
                print(f"   {Colors.GREEN}Synopsis:{Colors.ENDC} {synopsis}")
            print("-" * 80)
            
        return True
    except Exception as e:
        print_status(f"Error executing search: {e}", "error")
        return False


# ---------------------------------------------------------------------------
# 6. NOVEL PROSE ANALYZER
# ---------------------------------------------------------------------------
def analyze_novel(novel_id_or_path):
    print_status(f"Analyzing prose and vocabulary for: {novel_id_or_path}", "info")
    
    # Resolve path
    target_dir = None
    if os.path.exists(novel_id_or_path):
        target_dir = novel_id_or_path
    else:
        # Check standard output directories
        potential_paths = [
            os.path.join("/home/datdang/working/lnd_dev/sources/novels", novel_id_or_path),
            novel_id_or_path
        ]
        # Search inside sources/novels
        if not target_dir and os.path.exists("/home/datdang/working/lnd_dev/sources/novels"):
            for folder in os.listdir("/home/datdang/working/lnd_dev/sources/novels"):
                folder_path = os.path.join("/home/datdang/working/lnd_dev/sources/novels", folder)
                if not os.path.isdir(folder_path):
                    continue
                # Check folder name match
                if novel_id_or_path.lower() in folder.lower() or novel_id_or_path.lower() == folder.lower():
                    target_dir = folder_path
                    break
                # Check metadata.json match
                meta_path = os.path.join(folder_path, "metadata.json")
                if os.path.exists(meta_path):
                    try:
                        with open(meta_path, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                            novel_id = meta.get("novel_id", meta.get("id", ""))
                            if novel_id and novel_id.lower() == novel_id_or_path.lower():
                                target_dir = folder_path
                                break
                    except Exception:
                        pass
        
        if not target_dir:
            for p in potential_paths:
                if os.path.exists(p):
                    target_dir = p
                    break
                    
    if not target_dir:
        print_status(f"Could not find novel directory for '{novel_id_or_path}'", "error")
        return False
        
    print_status(f"Found novel directory at: {target_dir}", "success")
    
    # Gather all text content
    chapters_dir = os.path.join(target_dir, "chapters")
    text_files = []
    
    if os.path.exists(chapters_dir):
        for f in sorted(os.listdir(chapters_dir)):
            if f.endswith(".md"):
                text_files.append(os.path.join(chapters_dir, f))
    elif os.path.exists(os.path.join(target_dir, "novel_full.md")):
        text_files.append(os.path.join(target_dir, "novel_full.md"))
        
    if not text_files:
        print_status("No text files found to analyze.", "error")
        return False
        
    print_status(f"Found {len(text_files)} text files for analysis.", "info")
    
    # Metrics containers
    total_lines = 0
    dialogue_lines = 0
    monologue_lines = 0
    physical_action_lines = 0
    
    # Keyword list mapping
    vocabulary_stats = {
        "smell_and_scent": ["匂い", "におい", "香り", "残り香", "嗅ぐ", "鼻", "フェロモン", "むわっ"],
        "clothing_fetish": ["パンツ", "下着", "体操服", "スク水", "スパンデックス", "スパッツ", "ブルマ", "布", "衣類", "靴下", "タイツ"],
        "bodily_fluids": ["ザーメン", "精液", "汁", "愛液", "膣", "分泌", "尿", "我慢汁", "汗"],
        "sensory_friction": ["擦り", "擦る", "サオ", "肉棒", "ペニス", "アソコ", "亀頭", "股間", "勃起", "締めつけ"],
        "sfx_onomatopoeia": ["しこしこ", "しゅこしこ", "しこっ", "しゅこっ", "びゅーっ", "びゅるる", "どぷどぷ", "ぬるぬる", "じゅぷじゅぷ", "びゅくっ", "どぷっ"]
    }
    
    vocabulary_hits = {category: {} for category in vocabulary_stats}
    
    for file_path in text_files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or line_str.startswith("#") or line_str.startswith("---") or line_str.startswith("*"):
                    continue
                    
                total_lines += 1
                
                # Check dialogue
                if "「" in line_str and "」" in line_str:
                    dialogue_lines += 1
                # Check monologue
                elif "（" in line_str and "）" in line_str:
                    monologue_lines += 1
                else:
                    physical_action_lines += 1
                    
                # Scan vocabulary
                for category, keywords in vocabulary_stats.items():
                    for kw in keywords:
                        count = line_str.count(kw)
                        if count > 0:
                            vocabulary_hits[category][kw] = vocabulary_hits[category].get(kw, 0) + count
                            
    if total_lines == 0:
        print_status("No processable lines found in files.", "warning")
        return True
        
    # Calculate ratios
    dialogue_ratio = (dialogue_lines / total_lines) * 100
    monologue_ratio = (monologue_lines / total_lines) * 100
    action_ratio = (physical_action_lines / total_lines) * 100
    
    # Format Analysis Markdown
    analysis_md = f"# LND Studio Novel Prose Analysis\n\n"
    analysis_md += f"**Novel:** {os.path.basename(target_dir)}\n"
    analysis_md += f"**Analyzed Files:** {len(text_files)} files\n\n"
    
    analysis_md += f"## 1. Pacing Topology (Cấu trúc Nhịp độ)\n"
    analysis_md += f"- **Total Processed Lines:** {total_lines}\n"
    analysis_md += f"- **Dialogue Ratio (Tỷ lệ Thoại):** {dialogue_ratio:.2f}% ({dialogue_lines} lines)\n"
    analysis_md += f"- **Monologue Ratio (Tỷ lệ Nội tâm):** {monologue_ratio:.2f}% ({monologue_lines} lines)\n"
    analysis_md += f"- **Action/Description Ratio (Tỷ lệ Hành động/Miêu tả):** {action_ratio:.2f}% ({physical_action_lines} lines)\n\n"
    
    analysis_md += f"## 2. Sensory Vocabulary Analysis (Tần suất Từ vựng Đặc trưng)\n"
    
    for category, hits in vocabulary_hits.items():
        sorted_hits = sorted(hits.items(), key=lambda x: x[1], reverse=True)
        analysis_md += f"### {category.replace('_', ' ').title()}\n"
        if not sorted_hits:
            analysis_md += "*No keywords matched in this category.*\n\n"
        else:
            analysis_md += "| Keyword | Count | Meaning / Role |\n"
            analysis_md += "|---|---|---|\n"
            for kw, count in sorted_hits:
                meaning = ""
                if kw == "匂い" or kw == "におい": meaning = "Scent / Smell"
                elif kw == "残り香": meaning = "Lingering Scent"
                elif kw == "パンツ": meaning = "Panties"
                elif kw == "下着": meaning = "Underwear"
                elif kw == "体操服": meaning = "Gym clothes"
                elif kw == "スク水": meaning = "School swimsuit"
                elif kw == "ザーメン" or kw == "精液": meaning = "Semen"
                elif kw == "しこしこ" or kw == "しゅこしこ": meaning = "Jerk off SFX"
                elif kw == "びゅーっ" or kw == "びゅるる": meaning = "Ejaculation SFX"
                elif kw == "クロッチ": meaning = "Crotch lining"
                elif kw == "擦る": meaning = "Friction"
                else: meaning = "Sensory cue"
                analysis_md += f"| `{kw}` | {count} | {meaning} |\n"
            analysis_md += "\n"
            
    # Save report
    report_path = os.path.join(target_dir, "analysis_prose.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(analysis_md)
        
    print_status(f"Saved analysis report to: {report_path}", "success")
    
    # Also print summary to terminal
    print("\n" + "="*50)
    print(f"{Colors.HEADER}PROSE ANALYSIS SUMMARY{Colors.ENDC}")
    print(f"Dialogue: {dialogue_ratio:.1f}% | Monologue: {monologue_ratio:.1f}% | Action: {action_ratio:.1f}%")
    print(f"Total Lines Analyzed: {total_lines}")
    print("="*50)
    
    return True


# ---------------------------------------------------------------------------
# MAIN CLI DISPATCHER
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print(f"{Colors.HEADER}LND Studio Universal R18 Downloader & Scraper CLI{Colors.ENDC}")
        print("Usage:")
        print("  python studio/tools/r18_downloader.py <URL_or_ID> [--output <custom_dir>]")
        print("  python studio/tools/r18_downloader.py --search <query>")
        print("  python studio/tools/r18_downloader.py --analyze <Novel_ID_or_Path>")
        print("\nSupported inputs:")
        print("  - Syosetu ID (e.g. n1481bn) or full Syosetu/Nocturne/Moonlight URL")
        print("  - Hitomi ID (e.g. 3444767) or full Hitomi.la gallery URL")
        print("  - nhentai ID (e.g. 123456) or full nhentai URL")
        print("  - Telegraph / Teletype URL (e.g. https://telegra.ph/...)")
        sys.exit(0)

    # 1. Check for search option
    if sys.argv[1] == "--search":
        if len(sys.argv) < 3:
            print_status("Please specify a search query.", "error")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        success = search_nocturne(query)
        sys.exit(0 if success else 1)
        
    # 2. Check for analyze option
    if sys.argv[1] == "--analyze":
        if len(sys.argv) < 3:
            print_status("Please specify a novel ID or directory path to analyze.", "error")
            sys.exit(1)
        target = sys.argv[2]
        success = analyze_novel(target)
        sys.exit(0 if success else 1)

    input_val = sys.argv[1].strip()
    
    # Custom output parsing
    custom_output = None
    if "--output" in sys.argv:
        try:
            idx = sys.argv.index("--output")
            custom_output = sys.argv[idx + 1]
        except (IndexError, ValueError):
            pass

    # Root folders for storage
    novel_output_root = custom_output or "/home/datdang/working/lnd_dev/sources/novels"
    manga_output_root = custom_output or "/home/datdang/working/lnd_dev/sources/manga"

    # Make sure output roots exist
    os.makedirs(novel_output_root, exist_ok=True)
    os.makedirs(manga_output_root, exist_ok=True)

    # 1. Detect Syosetu Novel
    syosetu_match = re.search(r'(n\d+[a-zA-Z0-9]+)', input_val) or re.search(r'syosetu\.com/(n\d+[a-zA-Z0-9]+)', input_val)
    if syosetu_match:
        novel_id = syosetu_match.group(1).lower()
        success = download_syosetu_novel(novel_id, novel_output_root)
        sys.exit(0 if success else 1)

    # 2. Detect Hitomi.la
    hitomi_match = re.search(r'hitomi\.la/galleries/(\d+)\.html', input_val) or re.match(r'^(\d{7,8})$', input_val)
    if hitomi_match:
        gallery_id = hitomi_match.group(1)
        print_status(f"Detected Hitomi Gallery ID: {gallery_id}", "info")
        out_path = os.path.join(manga_output_root, f"hitomi_{gallery_id}")
        
        cmd = ["node", "hitomi_downloader.mjs", gallery_id, out_path]
        print_status(f"Running node integration: {' '.join(cmd)}", "info")
        res = subprocess.run(cmd, cwd="/home/datdang/working/lnd_dev/hitomi_test")
        sys.exit(res.returncode)

    # 3. Detect nhentai
    nhentai_match = re.search(r'nhentai\.net/g/(\d+)/?', input_val) or re.match(r'^(\d{5,6})$', input_val)
    if nhentai_match:
        gallery_id = nhentai_match.group(1)
        print_status(f"Detected nhentai Gallery ID: {gallery_id}", "info")
        url = f"https://nhentai.net/g/{gallery_id}/"
        
        cmd = ["python3", "/home/datdang/working/Telegraph-Image-Downloader/nhentai-downloander/main.py", url, manga_output_root, "--archive", "--lang", "en"]
        print_status(f"Running nhentai downloader: {' '.join(cmd)}", "info")
        res = subprocess.run(cmd)
        sys.exit(res.returncode)

    # 4. Detect Telegraph / Teletype
    if "telegra.ph/" in input_val or "teletype.in/" in input_val:
        success = download_telegraph_images(input_val, manga_output_root)
        sys.exit(0 if success else 1)

    # If it falls through, we don't know the format!
    print_status(f"Format not recognized for input: '{input_val}'", "error")
    print_status("Please check the usage by running this script without arguments.", "info")
    sys.exit(1)

if __name__ == "__main__":
    main()
