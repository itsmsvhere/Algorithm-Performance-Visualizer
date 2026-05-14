import streamlit as st
import random
import math
import time
import json

st.set_page_config(
    page_title="Algorithm Performance Visualizer",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Hide Streamlit header/footer/menu ───────────────────────────────────────
st.markdown("""
<style>
#MainMenu, header, footer, .stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─── Global Dark Theme CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    background-color: #0a0a12 !important;
    color: #e8e8f0 !important;
}

/* Remove default Streamlit padding */
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { background: #0c0c1a !important; border-right: 1px solid #1e1e30 !important; }
section[data-testid="stSidebar"] > div { padding-top: 12px !important; }

/* Sidebar labels */
.sidebar-label {
    font-size: 10px; color: #5a5a8a; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 8px; margin-top: 12px;
    display: block;
}

/* Buttons */
div[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid #2a2a40 !important;
    color: #8a8aaa !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    padding: 6px 16px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: #7c6ee6 !important;
    color: #7c6ee6 !important;
}

/* Radio / selectbox */
div[data-testid="stRadio"] label { color: #8a8aaa !important; font-size: 12px !important; }
div[data-testid="stRadio"] label:hover { color: #e8e8f0 !important; }
div[data-testid="stSelectbox"] > div { background: #0e0e1c !important; border: 1px solid #2a2a40 !important; color: #e8e8f0 !important; }

/* Sliders */
div[data-testid="stSlider"] > div > div > div > div { background: #7c6ee6 !important; }

/* Tabs */
div[data-testid="stTabs"] button {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #6a6a9a !important;
    background: transparent !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 6px !important;
    margin-right: 6px !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #7c6ee6 !important;
    border-color: #7c6ee6 !important;
    background: #7c6ee622 !important;
}
div[data-testid="stTabs"] > div > div:first-child {
    border-bottom: none !important;
    gap: 6px !important;
}

/* Cards and panels */
.algo-card {
    background: #0e0e1c;
    border-radius: 10px;
    padding: 16px;
    border: 1px solid #1a1a2e;
}
.complexity-card {
    background: #0e0e1c;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
}
.complexity-inner {
    background: #0a0a12;
    border-radius: 6px;
    padding: 8px 10px;
}

/* Info metric boxes */
.metric-box {
    background: #0e0e1c;
    border-radius: 8px;
    padding: 10px 14px;
    border: 1px solid #1a1a2e;
    text-align: center;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0a12; }
::-webkit-scrollbar-thumb { background: #2a2a40; border-radius: 3px; }

/* Table */
table { border-collapse: collapse; width: 100%; font-size: 12px; }
th { color: #5a5a8a !important; font-weight: 400 !important; letter-spacing: 1px; text-transform: uppercase; font-size: 10px !important; padding: 8px 12px; border-bottom: 1px solid #2a2a40; }
td { padding: 10px 12px; border-bottom: 1px solid #1a1a2e; color: #e8e8f0; }

/* Hide stray elements */
div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMarkdownContainer"] > p:empty) { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── Algorithm Definitions ────────────────────────────────────────────────────

ALGO_META = {
    "sorting": {
        "Bubble Sort":    {"complexity": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"}, "color": "#ff6b6b"},
        "Selection Sort": {"complexity": {"best": "O(n²)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"}, "color": "#feca57"},
        "Insertion Sort": {"complexity": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"}, "color": "#54a0ff"},
        "Merge Sort":     {"complexity": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(n)"}, "color": "#5f27cd"},
        "Quick Sort":     {"complexity": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n²)", "space": "O(log n)"}, "color": "#00d2d3"},
        "Heap Sort":      {"complexity": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(1)"}, "color": "#ff9f43"},
    },
    "searching": {
        "Linear Search": {"complexity": {"best": "O(1)", "avg": "O(n)", "worst": "O(n)", "space": "O(1)"}, "color": "#ee5a24"},
        "Binary Search": {"complexity": {"best": "O(1)", "avg": "O(log n)", "worst": "O(log n)", "space": "O(1)"}, "color": "#0652DD"},
        "Jump Search":   {"complexity": {"best": "O(1)", "avg": "O(√n)", "worst": "O(√n)", "space": "O(1)"}, "color": "#6c5ce7"},
    }
}

# ─── Algorithm Implementations ────────────────────────────────────────────────

def bubble_sort(arr):
    a = arr[:]
    steps = []
    for i in range(len(a) - 1):
        for j in range(len(a) - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
            steps.append(a[:])
    return {"sorted": a, "steps": steps}

def selection_sort(arr):
    a = arr[:]
    steps = []
    for i in range(len(a) - 1):
        m = i
        for j in range(i + 1, len(a)):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
        steps.append(a[:])
    return {"sorted": a, "steps": steps}

def insertion_sort(arr):
    a = arr[:]
    steps = []
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
        steps.append(a[:])
    return {"sorted": a, "steps": steps}

def merge_sort(arr):
    a = arr[:]
    steps = []
    def merge(a, l, m, r):
        L, R = a[l:m+1], a[m+1:r+1]
        i = j = 0
        k = l
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                a[k] = L[i]; i += 1
            else:
                a[k] = R[j]; j += 1
            k += 1
        while i < len(L): a[k] = L[i]; i += 1; k += 1
        while j < len(R): a[k] = R[j]; j += 1; k += 1
        steps.append(a[:])
    def sort(a, l, r):
        if l < r:
            m = (l + r) // 2
            sort(a, l, m); sort(a, m+1, r); merge(a, l, m, r)
    sort(a, 0, len(a) - 1)
    return {"sorted": a, "steps": steps}

def quick_sort(arr):
    a = arr[:]
    steps = []
    def partition(a, lo, hi):
        pivot = a[hi]; i = lo - 1
        for j in range(lo, hi):
            if a[j] <= pivot:
                i += 1; a[i], a[j] = a[j], a[i]
        a[i+1], a[hi] = a[hi], a[i+1]
        steps.append(a[:]); return i + 1
    def sort(a, lo, hi):
        if lo < hi:
            p = partition(a, lo, hi); sort(a, lo, p-1); sort(a, p+1, hi)
    sort(a, 0, len(a) - 1)
    return {"sorted": a, "steps": steps}

def heap_sort(arr):
    a = arr[:]
    steps = []
    def heapify(n, i):
        l, r, largest = 2*i+1, 2*i+2, i
        if l < n and a[l] > a[largest]: largest = l
        if r < n and a[r] > a[largest]: largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            steps.append(a[:])
            heapify(n, largest)
    n = len(a)
    for i in range(n//2 - 1, -1, -1): heapify(n, i)
    for i in range(n-1, 0, -1):
        a[0], a[i] = a[i], a[0]; steps.append(a[:])
        heapify(i, 0)
    return {"sorted": a, "steps": steps}

def linear_search(arr, target):
    steps = []; found = -1
    for i in range(len(arr)):
        steps.append({"index": i, "found": arr[i] == target})
        if arr[i] == target: found = i; break
    return {"found": found, "steps": steps, "arr": arr}

def binary_search(arr, target):
    sorted_arr = sorted(arr)
    steps = []; lo, hi, found = 0, len(sorted_arr)-1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        steps.append({"lo": lo, "hi": hi, "mid": mid, "val": sorted_arr[mid]})
        if sorted_arr[mid] == target: found = mid; break
        elif sorted_arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return {"found": found, "steps": steps, "arr": sorted_arr}

def jump_search(arr, target):
    sorted_arr = sorted(arr)
    steps = []; step = max(1, int(math.sqrt(len(sorted_arr))))
    prev = 0; found = -1
    while prev < len(sorted_arr) and sorted_arr[min(step, len(sorted_arr))-1] < target:
        steps.append({"index": prev, "jump": True})
        prev += step
    for i in range(prev, min(prev + step, len(sorted_arr))):
        steps.append({"index": i, "jump": False})
        if sorted_arr[i] == target: found = i; break
    return {"found": found, "steps": steps, "arr": sorted_arr}

SORT_FNS = {
    "Bubble Sort": bubble_sort, "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort, "Merge Sort": merge_sort,
    "Quick Sort": quick_sort, "Heap Sort": heap_sort,
}
SEARCH_FNS = {
    "Linear Search": linear_search,
    "Binary Search": binary_search,
    "Jump Search": jump_search,
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def generate_input(size, itype):
    arr = list(range(1, size + 1))
    if itype == "Random":
        random.shuffle(arr)
        arr = [random.randint(1, size * 2) for _ in range(size)]
    elif itype == "Sorted":
        pass
    elif itype == "Reverse":
        arr.reverse()
    elif itype == "Nearly Sorted":
        swaps = max(1, int(size * 0.05))
        for _ in range(swaps):
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            arr[x], arr[y] = arr[y], arr[x]
    elif itype == "Duplicates":
        arr = [random.randint(1, max(3, size // 10)) for _ in range(size)]
    return arr

def complexity_fit(n, t_ms):
    if n < 2: return "O(?)"
    ratio = t_ms / n
    if ratio < 0.001: return "O(1) / O(log n)"
    if ratio < 0.05:  return "O(√n) / O(log n)"
    if ratio < 0.5:   return "O(n)"
    if ratio < 5:     return "O(n log n)"
    return "O(n²)"

def measure(fn, *args):
    t0 = time.perf_counter()
    result = fn(*args)
    t1 = time.perf_counter()
    return result, round((t1 - t0) * 1000, 3)

# ─── State Init ───────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "tab": "sorting",
        "algo": "Bubble Sort",
        "input_type": "Random",
        "size": 40,
        "speed": 50,
        "arr": None,
        "anim_frames": [],
        "search_target": None,
        "search_result": None,
        "runtime_ms": None,
        "fitted": None,
        "total_steps": 0,
        "benchmarks": [],
        "active_panel": "visualizer",
        "display_frame": None,
        "search_highlighted": set(),
        "search_arr": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def regenerate():
    arr = generate_input(st.session_state.size, st.session_state.input_type)
    st.session_state.arr = arr
    st.session_state.display_frame = arr[:]
    st.session_state.anim_frames = []
    st.session_state.search_target = arr[random.randint(0, len(arr)-1)] if arr else None
    st.session_state.search_result = None
    st.session_state.runtime_ms = None
    st.session_state.fitted = None
    st.session_state.total_steps = 0
    st.session_state.search_highlighted = set()
    st.session_state.search_arr = None

if st.session_state.arr is None:
    regenerate()

# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<span class="sidebar-label">Category</span>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sorting", use_container_width=True,
                     type="primary" if st.session_state.tab == "sorting" else "secondary"):
            st.session_state.tab = "sorting"
            st.session_state.algo = "Bubble Sort"
            regenerate(); st.rerun()
    with col2:
        if st.button("Searching", use_container_width=True,
                     type="primary" if st.session_state.tab == "searching" else "secondary"):
            st.session_state.tab = "searching"
            st.session_state.algo = "Linear Search"
            regenerate(); st.rerun()

    st.markdown('<span class="sidebar-label">Algorithm</span>', unsafe_allow_html=True)
    algos = list(ALGO_META[st.session_state.tab].keys())
    for name in algos:
        color = ALGO_META[st.session_state.tab][name]["color"]
        selected = st.session_state.algo == name
        dot = f'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{color};margin-right:8px;"></span>'
        btn_style = f"""
        <style>
        div[data-testid="stButton"] > button[kind="{'primary' if selected else 'secondary'}"].algo-btn-{name.replace(' ','_')} {{
            border-color: {color} !important; color: {color} !important;
            background: {color}18 !important;
        }}
        </style>"""
        if st.button(f"● {name}", key=f"algo_{name}", use_container_width=True):
            st.session_state.algo = name
            regenerate(); st.rerun()

    st.markdown('<span class="sidebar-label">Array Size: {}</span>'.format(st.session_state.size), unsafe_allow_html=True)
    new_size = st.slider("Size", 10, 120, st.session_state.size, label_visibility="collapsed", key="size_slider")
    if new_size != st.session_state.size:
        st.session_state.size = new_size
        regenerate(); st.rerun()

    st.markdown('<span class="sidebar-label">Input Type</span>', unsafe_allow_html=True)
    input_types = ["Random", "Sorted", "Reverse", "Nearly Sorted", "Duplicates"]
    new_itype = st.radio("Input Type", input_types, index=input_types.index(st.session_state.input_type),
                         label_visibility="collapsed")
    if new_itype != st.session_state.input_type:
        st.session_state.input_type = new_itype
        regenerate(); st.rerun()

    st.markdown('<span class="sidebar-label">Animation Speed: {}%</span>'.format(st.session_state.speed), unsafe_allow_html=True)
    st.session_state.speed = st.slider("Speed", 1, 100, st.session_state.speed, label_visibility="collapsed", key="speed_slider")

    if st.session_state.tab == "searching" and st.session_state.search_target is not None:
        color = ALGO_META["searching"][st.session_state.algo]["color"]
        st.markdown(f"""
        <div style="background:#1a1a2e;border-radius:8px;padding:10px 12px;border:1px solid {color}44;margin-top:12px;">
            <div style="font-size:10px;color:#5a5a8a;letter-spacing:2px;margin-bottom:4px;">TARGET VALUE</div>
            <div style="font-size:22px;font-weight:700;color:{color};">{st.session_state.search_target}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────

algo_meta = ALGO_META[st.session_state.tab][st.session_state.algo]
algo_color = algo_meta["color"]

st.markdown(f"""
<div style="border-bottom:1px solid #1e1e30;padding:16px 24px;
background:linear-gradient(90deg,#0a0a12 0%,#12122a 100%);
display:flex;align-items:center;justify-content:space-between;margin-bottom:0;">
    <div>
        <div style="font-size:11px;color:#5a5a8a;letter-spacing:3px;text-transform:uppercase;margin-bottom:2px;">
            Design & Analysis of Algorithms · Capstone
        </div>
        <h1 style="margin:0;font-size:20px;font-weight:700;color:#fff;letter-spacing:-0.5px;">
            <span style="color:{algo_color};">⬡</span> Algorithm Performance Visualizer
        </h1>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Panel Tabs ───────────────────────────────────────────────────────────────

tab_vis, tab_bench, tab_comp = st.tabs(["Visualizer", "Benchmark", "Complexity"])

# ═══════════════════════════════════════════════════════════════════════════════
# PANEL 1: VISUALIZER
# ═══════════════════════════════════════════════════════════════════════════════

with tab_vis:
    ctrl1, ctrl2, ctrl3, ctrl_info = st.columns([1, 1, 1, 4])
    run_clicked = ctrl1.button("▶ Run", use_container_width=True, key="run_btn")
    regen_clicked = ctrl2.button("↺ Regenerate", use_container_width=True, key="regen_btn")
    bench_clicked = ctrl3.button("📊 Benchmark", use_container_width=True, key="bench_btn")

    if regen_clicked:
        regenerate(); st.rerun()

    if bench_clicked:
        st.session_state.active_panel = "benchmark"

    # ── Run Algorithm ─────────────────────────────────────────────────────────
    anim_frames = []
    search_result_data = None
    display_arr = st.session_state.display_frame or st.session_state.arr

    if run_clicked:
        arr = st.session_state.arr[:]
        target = st.session_state.search_target

        if st.session_state.tab == "sorting":
            fn = SORT_FNS[st.session_state.algo]
            result, ms = measure(fn, arr)
            anim_frames = result["steps"]
            st.session_state.runtime_ms = ms
            st.session_state.fitted = complexity_fit(st.session_state.size, ms)
            st.session_state.total_steps = len(anim_frames)
            st.session_state.search_arr = None
            st.session_state.search_result = None
        else:
            fn = SEARCH_FNS[st.session_state.algo]
            result, ms = measure(fn, arr, target)
            anim_frames = result["steps"]
            st.session_state.runtime_ms = ms
            st.session_state.fitted = complexity_fit(st.session_state.size, ms)
            st.session_state.total_steps = len(anim_frames)
            st.session_state.search_result = result["found"]
            st.session_state.search_arr = result.get("arr", arr)

    # ── Runtime Info ──────────────────────────────────────────────────────────
    info_parts = []
    if st.session_state.runtime_ms is not None:
        info_parts.append(f'Runtime: <span style="color:{algo_color};">{st.session_state.runtime_ms}ms</span>')
    if st.session_state.fitted:
        info_parts.append(f'Fitted: <span style="color:#feca57;">{st.session_state.fitted}</span>')
    if st.session_state.total_steps > 0:
        info_parts.append(f'Steps: <span style="color:#54a0ff;">{st.session_state.total_steps}</span>')
    if info_parts:
        ctrl_info.markdown(
            '<div style="padding:8px 12px;font-size:12px;color:#5a5a8a;display:flex;gap:20px;align-items:center;">' +
            ' &nbsp;&nbsp;'.join(info_parts) + '</div>', unsafe_allow_html=True)

    # ── Visualization Area ────────────────────────────────────────────────────
    viz_placeholder = st.empty()

    def render_bars(arr_data, color, highlighted=None, found_idx=None, tab="sorting"):
        if not arr_data: return ""
        max_val = max(arr_data) if arr_data else 1
        bars_html = ""
        total = len(arr_data)
        bar_w = max(2, min(18, int(900 / total)))
        gap = 1 if total > 60 else 2

        for i, v in enumerate(arr_data):
            h_pct = max(1, (v / max_val) * 100)
            is_found = (tab == "searching" and found_idx is not None and found_idx == i)
            is_highlighted = (highlighted is not None and i in highlighted)
            bar_color = "#2ecc71" if is_found else ("#ffffff" if is_highlighted else color)
            opacity = "0.3" if (tab == "searching" and highlighted and not is_highlighted and not is_found) else "1"
            glow = f"box-shadow:0 0 8px {bar_color};" if is_highlighted else ""
            bars_html += f'<div style="display:inline-block;width:{bar_w}px;height:{h_pct}%;background:{bar_color};opacity:{opacity};border-radius:2px 2px 0 0;margin-right:{gap}px;vertical-align:bottom;{glow}" title="{v}"></div>'

        grid_lines = ""
        for pct in [25, 50, 75]:
            grid_lines += f'<div style="position:absolute;left:0;right:0;bottom:{pct}%;border-top:1px solid #1a1a2e;pointer-events:none;"><span style="font-size:9px;color:#3a3a5a;position:absolute;right:4px;top:-10px;">{pct}%</span></div>'

        return f"""
        <div style="background:#0e0e1c;border-radius:10px;padding:12px 12px 0;
                    border:1px solid #1a1a2e;position:relative;overflow:hidden;
                    height:320px;display:flex;align-items:flex-end;">
            {grid_lines}
            <div style="width:100%;height:100%;display:flex;align-items:flex-end;overflow:hidden;">
                {bars_html}
            </div>
        </div>"""

    # Animate if frames exist
    if run_clicked and anim_frames:
        delay = max(0.01, (200 - st.session_state.speed * 1.8) / 1000)
        search_highlight_indices = set()
        search_display_arr = st.session_state.search_arr or st.session_state.arr

        for i, frame in enumerate(anim_frames):
            if st.session_state.tab == "sorting":
                bars_html = render_bars(frame, algo_color, tab="sorting")
                viz_placeholder.markdown(bars_html, unsafe_allow_html=True)
            else:
                step = frame
                highlighted = set()
                if "index" in step: highlighted.add(step["index"])
                if "mid" in step: highlighted.add(step["mid"])
                bars_html = render_bars(search_display_arr, algo_color,
                                        highlighted=highlighted, tab="searching")
                viz_placeholder.markdown(bars_html, unsafe_allow_html=True)
            time.sleep(delay)

        # Final frame
        if st.session_state.tab == "sorting":
            st.session_state.display_frame = anim_frames[-1] if anim_frames else st.session_state.arr
        else:
            st.session_state.display_frame = search_display_arr
    else:
        # Static display
        current_arr = st.session_state.display_frame or st.session_state.arr
        bars_html = render_bars(current_arr, algo_color, tab=st.session_state.tab)
        viz_placeholder.markdown(bars_html, unsafe_allow_html=True)

    # ── Complexity Cards ──────────────────────────────────────────────────────
    cxty = algo_meta["complexity"]
    card_data = [
        ("Best", cxty["best"], "#2ecc71"),
        ("Average", cxty["avg"], "#feca57"),
        ("Worst", cxty["worst"], "#ff6b6b"),
        ("Space", cxty["space"], "#54a0ff"),
    ]
    c1, c2, c3, c4 = st.columns(4)
    for col, (label, val, c) in zip([c1, c2, c3, c4], card_data):
        col.markdown(f"""
        <div style="background:#0e0e1c;border-radius:8px;padding:12px;border:1px solid {c}33;text-align:center;">
            <div style="font-size:9px;color:#5a5a8a;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">{label}</div>
            <div style="font-size:14px;font-weight:700;color:{c};">{val}</div>
        </div>""", unsafe_allow_html=True)

    # ── Search Result Banner ──────────────────────────────────────────────────
    if st.session_state.tab == "searching" and st.session_state.search_result is not None:
        found = st.session_state.search_result
        target = st.session_state.search_target
        if found >= 0:
            st.markdown(f"""
            <div style="background:#2ecc7122;border:1px solid #2ecc71;border-radius:8px;
                        padding:10px 16px;text-align:center;font-size:13px;color:#2ecc71;margin-top:8px;">
                ✓ Found target {target} at index {found}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#ff6b6b22;border:1px solid #ff6b6b;border-radius:8px;
                        padding:10px 16px;text-align:center;font-size:13px;color:#ff6b6b;margin-top:8px;">
                ✗ Target {target} not found in array
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PANEL 2: BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════

with tab_bench:
    st.markdown(f"""
    <div style="margin-bottom:20px;">
        <h2 style="margin:0 0 4px;font-size:16px;color:#fff;">Runtime Benchmark — {st.session_state.algo}</h2>
        <p style="margin:0;font-size:12px;color:#5a5a8a;">Average of 3 trials per input size · Input type: {st.session_state.input_type}</p>
    </div>""", unsafe_allow_html=True)

    if st.button("▶ Run Benchmark", key="bench_run"):
        sizes = [10, 50, 100, 250, 500, 1000]
        results = []
        with st.spinner("Running benchmarks..."):
            for n in sizes:
                a = generate_input(n, st.session_state.input_type)
                trials = 3
                total = 0
                for _ in range(trials):
                    if st.session_state.tab == "sorting":
                        fn = SORT_FNS[st.session_state.algo]
                        _, t = measure(fn, a)
                    else:
                        fn = SEARCH_FNS[st.session_state.algo]
                        tgt = a[random.randint(0, len(a)-1)]
                        _, t = measure(fn, a, tgt)
                    total += t
                results.append({"n": n, "time": round(total / trials, 4)})
        st.session_state.benchmarks = results

    benchmarks = st.session_state.benchmarks
    if not benchmarks:
        st.markdown("""
        <div style="color:#5a5a8a;text-align:center;margin-top:80px;">
            Click <strong style="color:#e8e8f0;">Run Benchmark</strong> to measure performance across input sizes.
        </div>""", unsafe_allow_html=True)
    else:
        # Bar chart
        max_t = max(b["time"] for b in benchmarks) or 0.001
        bars_html = '<div style="display:flex;align-items:flex-end;height:260px;gap:8px;background:#0e0e1c;border-radius:10px;padding:20px;border:1px solid #1a1a2e;margin-bottom:20px;">'
        for b in benchmarks:
            h = max(4, (b["time"] / max_t) * 85)
            bars_html += f"""
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end;">
                <div style="font-size:9px;color:{algo_color};margin-bottom:4px;">{b['time']}ms</div>
                <div style="width:100%;background:{algo_color};height:{h}%;border-radius:4px 4px 0 0;
                            box-shadow:0 0 12px {algo_color}55;min-height:4px;"></div>
                <div style="font-size:10px;color:#5a5a8a;margin-top:6px;">n={b['n']}</div>
            </div>"""
        bars_html += '</div>'
        st.markdown(bars_html, unsafe_allow_html=True)

        # Table
        cxty = algo_meta["complexity"]
        table_html = """
        <table>
            <thead><tr>
                <th>Input Size</th><th>Avg Time (ms)</th>
                <th>Fitted Complexity</th><th>Theoretical</th>
            </tr></thead><tbody>"""
        for b in benchmarks:
            fitted = complexity_fit(b["n"], b["time"])
            table_html += f"""
            <tr>
                <td>{b['n']}</td>
                <td style="color:{algo_color};font-weight:700;">{b['time']}</td>
                <td style="color:#feca57;">{fitted}</td>
                <td style="color:#8a8aaa;">{cxty['avg']}</td>
            </tr>"""
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PANEL 3: COMPLEXITY REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════

with tab_comp:
    st.markdown('<h2 style="margin:0 0 20px;font-size:16px;color:#fff;">Asymptotic Complexity Reference</h2>', unsafe_allow_html=True)

    all_algos = {**ALGO_META["sorting"], **ALGO_META["searching"]}
    names = list(all_algos.keys())

    # 2-column grid
    for row_start in range(0, len(names), 2):
        cols = st.columns(2)
        for ci, name in enumerate(names[row_start:row_start+2]):
            meta = all_algos[name]
            c = meta["color"]
            cxty = meta["complexity"]
            card_inner = ""
            for label, val, lc in [("Best", cxty["best"], "#2ecc71"), ("Average", cxty["avg"], "#feca57"),
                                    ("Worst", cxty["worst"], "#ff6b6b"), ("Space", cxty["space"], "#54a0ff")]:
                card_inner += f"""
                <div style="background:#0a0a12;border-radius:6px;padding:8px 10px;">
                    <div style="font-size:9px;color:#5a5a8a;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:2px;">{label}</div>
                    <div style="color:{lc};font-size:12px;font-weight:700;">{val}</div>
                </div>"""
            cols[ci].markdown(f"""
            <div style="background:#0e0e1c;border-radius:10px;padding:16px;border:1px solid {c}33;margin-bottom:16px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                    <span style="width:10px;height:10px;border-radius:50%;background:{c};display:inline-block;"></span>
                    <span style="font-weight:700;color:#fff;font-size:13px;">{name}</span>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">{card_inner}</div>
            </div>""", unsafe_allow_html=True)

    # Growth function comparison chart
    st.markdown("""
    <div style="margin-top:8px;background:#0e0e1c;border-radius:10px;padding:20px;border:1px solid #1a1a2e;">
        <h3 style="margin:0 0 16px;font-size:13px;color:#8a8aaa;">Growth Function Comparison (n=1…20)</h3>""",
    unsafe_allow_html=True)

    ns = list(range(1, 21))
    growth_fns = {
        "O(1)": lambda n: 1,
        "O(log n)": lambda n: math.log2(n) if n > 1 else 0,
        "O(n)": lambda n: n,
        "O(n log n)": lambda n: n * math.log2(n) if n > 1 else 0,
        "O(n²)": lambda n: n * n,
    }
    colors_g = ["#2ecc71", "#54a0ff", "#feca57", "#ff9f43", "#ff6b6b"]
    max_val_g = 20 * 20  # n²(20)

    bars_html = '<div style="display:flex;align-items:flex-end;height:120px;gap:3px;">'
    for n in ns:
        bars_html += '<div style="flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end;gap:1px;">'
        for (label, fn), col in zip(growth_fns.items(), colors_g):
            v = fn(n)
            h = max(2, (v / max_val_g) * 100)
            bars_html += f'<div style="width:100%;background:{col};height:{h}%;opacity:0.7;min-height:2px;"></div>'
        bars_html += '</div>'
    bars_html += '</div>'

    legend_html = '<div style="display:flex;gap:16px;margin-top:12px;flex-wrap:wrap;">'
    for (label, _), col in zip(growth_fns.items(), colors_g):
        legend_html += f'<div style="display:flex;align-items:center;gap:6px;font-size:11px;"><div style="width:10px;height:10px;background:{col};border-radius:2px;"></div><span style="color:#8a8aaa;">{label}</span></div>'
    legend_html += '</div>'

    st.markdown(bars_html + legend_html + '</div>', unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="border-top:1px solid #1e1e30;padding:8px 24px;display:flex;
align-items:center;justify-content:space-between;font-size:10px;
color:#3a3a5a;background:#0c0c1a;margin-top:16px;">
    <span>Module 1: Algo Library · Module 2: Input Generator · Module 3: Runtime Measurement · Module 4: Complexity Fitting · Module 5: Dashboard</span>
    <span style="color:{algo_color};">Algorithm Performance Visualizer</span>
</div>
""", unsafe_allow_html=True)
