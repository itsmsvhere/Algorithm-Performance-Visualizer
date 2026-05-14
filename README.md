# Algorithm Performance Visualizer

An interactive desktop-grade dashboard for visualizing, benchmarking, and comparing classical sorting and searching algorithms with live step-by-step animation, empirical runtime measurement, and asymptotic complexity analysis.

## 🎯 Features

- **Live Animation**: Step-by-step bar-chart visualization of every swap, comparison, and jump
- **Runtime Benchmarking**: Measures actual execution time across multiple input sizes with 3-trial averaging
- **Empirical Complexity Fitting**: Automatically classifies observed runtime into O(1), O(n), O(n log n), O(n²) etc.
- **Modern Dark UI**: JetBrains Mono monospace dashboard with custom CSS — zero default Streamlit styling
- **Input Shape Control**: Test algorithms against Random, Sorted, Reverse, Nearly Sorted, and Duplicate-heavy arrays
- **Asymptotic Reference Panel**: Growth function comparison chart for O(1) through O(n²) across n = 1…20
- **Search Highlighting**: Active index glows white, found index turns green in real time

## 🛠️ Technology Stack

- **Python 3.9+**
- **Streamlit** - Web application framework
- **Custom CSS** - Full dark theme injection via `st.markdown`
- **Python stdlib only** - `random`, `math`, `time` — zero ML/data dependencies

## 📦 Installation

### 1. Prerequisites

Ensure you have Python 3.9 or higher installed:

```bash
python --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/<your-username>/algo-visualizer.git
cd algo-visualizer
```

### 3. (Recommended) Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` by default.

## 📊 User Interface Overview

### Sidebar
- **Category Toggle** — Switch between Sorting and Searching
- **Algorithm Picker** — Color-coded buttons for each algorithm
- **Array Size Slider** — Control n from 10 to 120
- **Input Type Radio** — Choose the shape of the input array
- **Speed Slider** — Control animation delay (1% = slowest, 100% = fastest)
- **Target Value Display** — Shows the randomly selected search target (searching mode only)

### Main Workspace (Tabbed Interface)

#### Tab 1: Visualizer
- **Bar Chart** — Live animated array with percentage grid lines
- **Control Bar** — Run / Regenerate / Benchmark buttons + runtime metrics
- **Complexity Cards** — Best / Average / Worst / Space per selected algorithm
- **Search Result Banner** — Found / Not Found status after search completes

#### Tab 2: Benchmark
- **Run Benchmark Button** — Triggers measurement across n = [10, 50, 100, 250, 500, 1000]
- **Bar Chart** — Visual comparison of runtime per input size
- **Results Table** — Avg time (ms), fitted complexity class, theoretical complexity

#### Tab 3: Complexity
- **Algorithm Cards** — Full Big-O breakdown for all 9 algorithms in a 2-column grid
- **Growth Chart** — Stacked bar comparison of O(1), O(log n), O(n), O(n log n), O(n²) for n = 1…20

## 🔢 Algorithms Included

### Sorting (6)

| Algorithm | Best | Average | Worst | Space |
|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |

### Searching (3)

| Algorithm | Best | Average | Worst | Space |
|---|---|---|---|---|
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Jump Search | O(1) | O(√n) | O(√n) | O(1) |

## 📥 Input Types

| Type | Description |
|---|---|
| **Random** | Shuffled array with random values up to 2× array size |
| **Sorted** | Already sorted in ascending order (best case for some algorithms) |
| **Reverse** | Sorted descending (worst case for Bubble and Insertion Sort) |
| **Nearly Sorted** | Sorted with ~5% random swaps introduced |
| **Duplicates** | Array filled with heavily repeated values (≤10% unique) |

## 🔬 Processing Pipeline

### Sorting Visualization
1. **Input Generation** — Array created per selected type and size
2. **Algorithm Execution** — Full run captured as a list of intermediate array states (steps)
3. **Runtime Measurement** — `time.perf_counter()` wraps execution for ms precision
4. **Frame-by-Frame Animation** — Each step rendered as a bar chart with configurable delay
5. **Complexity Fitting** — Observed time mapped to nearest Big-O class

### Searching Visualization
1. **Target Selection** — Random element from array selected as search target
2. **Algorithm Execution** — Each probe captured as a step with index and metadata
3. **Highlight Rendering** — Active probe index highlighted white; found index rendered green
4. **Result Banner** — Found index or not-found status displayed post-animation

## 📋 Empirical Complexity Fitting

The application maps observed runtime to complexity class using a ratio heuristic:

| Runtime / n ratio | Fitted Class |
|---|---|
| < 0.001 | O(1) / O(log n) |
| 0.001 – 0.05 | O(√n) / O(log n) |
| 0.05 – 0.5 | O(n) |
| 0.5 – 5 | O(n log n) |
| > 5 | O(n²) |

## 💻 Code Structure

```
algo-visualizer/
├── app.py
│   ├── ALGO_META (dict)               — complexity + color metadata for all 9 algorithms
│   ├── Sorting Functions (6)          — bubble, selection, insertion, merge, quick, heap
│   ├── Searching Functions (3)        — linear, binary, jump
│   ├── generate_input()               — produces arrays per input type
│   ├── complexity_fit()               — maps runtime to Big-O class
│   ├── measure()                      — perf_counter-based timing wrapper
│   ├── init_state()                   — Streamlit session state initializer
│   ├── regenerate()                   — resets array, target, and animation state
│   ├── Sidebar                        — category, algorithm, size, input type, speed
│   ├── Tab: Visualizer                — bar chart animation + complexity cards
│   ├── Tab: Benchmark                 — multi-size runtime measurement + table
│   └── Tab: Complexity                — reference cards + growth function chart
├── .streamlit/
│   └── config.toml                    — dark theme + headless server config
├── requirements.txt
├── .gitignore
└── README.md
```

### Key Design Principles

- **Zero External Data Libraries** — No NumPy, Pandas, or Matplotlib; pure Python algorithms
- **Session State Architecture** — All app state persisted in `st.session_state` across reruns
- **Frame Capture Pattern** — Algorithms record intermediate states during execution, not during animation
- **CSS Injection** — Full dark monospace theme applied globally via `st.markdown`
- **Modular Panel Structure** — Each tab is fully independent with its own state and rendering logic

## 🎨 Theme

The application uses a fully custom dark theme — Streamlit's default styling is suppressed entirely.

| Token | Value |
|---|---|
| Background | `#0a0a12` |
| Sidebar | `#0c0c1a` |
| Card Surface | `#0e0e1c` |
| Border | `#1e1e30` |
| Primary Text | `#e8e8f0` |
| Muted Text | `#5a5a8a` |
| Font | JetBrains Mono (Google Fonts CDN) |

Algorithm accent colors are unique per algorithm and applied to bars, borders, buttons, and metric text consistently.

## ⚠️ Error Handling

| Scenario | Handling |
|---|---|
| Empty array state | Guarded with `if st.session_state.arr is None` before render |
| Zero max value in bars | `max_val = max(arr) if arr else 1` prevents division by zero |
| Speed out of range | Slider clamped to 1–100; delay floored at 10ms |
| Benchmark before run | Empty state message shown with instruction |
| Search on unsorted input | Binary/Jump Search sort internally before probing |

## 🚀 Workflow Example

1. **Launch Application**
   ```bash
   streamlit run app.py
   ```

2. **Select Algorithm**
   - Choose Sorting or Searching from the sidebar
   - Pick an algorithm (color-coded by accent)

3. **Configure Input**
   - Set array size with the slider
   - Select input type (try Reverse for worst-case Bubble Sort)
   - Adjust animation speed

4. **Run Visualization**
   - Click **▶ Run**
   - Watch the bars animate step by step
   - Check runtime, step count, and fitted complexity above the chart

5. **Benchmark**
   - Click **📊 Benchmark** or switch to the Benchmark tab
   - Click **▶ Run Benchmark**
   - Compare empirical vs theoretical complexity in the table

6. **Explore Complexity**
   - Switch to the Complexity tab
   - Review Big-O cards for all algorithms
   - Inspect the growth function chart

## 🚢 Deployment

### Streamlit Community Cloud (free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account → select repo → set `app.py` as entrypoint
4. Click **Deploy**

`requirements.txt` and `.streamlit/config.toml` are picked up automatically. No additional configuration needed.

## 🐛 Troubleshooting

### Application won't start
**Solution**: Ensure Streamlit is installed and Python ≥ 3.9:
```bash
pip install --upgrade streamlit
python --version
```

### Animation appears frozen
**Solution**: Reduce array size or increase speed slider. Large arrays (n > 80) with Bubble Sort produce thousands of frames.

### Dark theme not applying
**Solution**: Ensure `.streamlit/config.toml` is present in the project root. Streamlit reads it automatically on launch.

### Benchmark shows 0.0ms for all sizes
**Solution**: This occurs with searching algorithms on very small n where execution is sub-millisecond. Results are expected — try sorting algorithms for visible growth curves.

## 📚 References

- **Streamlit Documentation**: https://docs.streamlit.io
- **Streamlit Session State**: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
- **Python time.perf_counter**: https://docs.python.org/3/library/time.html#time.perf_counter
- **Big-O Cheat Sheet**: https://www.bigocheatsheet.com

## 📄 Academic Context

```
Algorithm Performance Visualizer v1.0
Design & Analysis of Algorithms — Capstone Project
B.Tech Artificial Intelligence & Data Science
Saveetha School of Engineering, SIMATS
```

## ⚖️ License

MIT — free to use for academic, research, and personal projects.

## 🎓 Author Notes

This application was designed for:
- **Academic Demonstrations** — Understanding algorithm behavior across input shapes
- **Capstone Submission** — Covers all 5 module requirements of the DAA course
- **Portfolio Projects** — Production-grade Streamlit app with zero boilerplate UI
- **Interview Prep** — Visual intuition for complexity analysis questions

The code follows best practices in:
- Algorithm implementation (pure Python, no library sort/search calls)
- Streamlit architecture (session state, tab isolation, rerun control)
- UI design (custom CSS, consistent design tokens, zero default styling)
- Performance (frame capture separate from animation, benchmarks averaged over 3 trials)

---

**Version**: 1.0
**Last Updated**: 2025
**Status**: Production Ready
