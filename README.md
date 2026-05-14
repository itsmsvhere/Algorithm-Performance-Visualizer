# ⬡ Algorithm Performance Visualizer

> Design & Analysis of Algorithms — Capstone Project  
> B.Tech Artificial Intelligence & Data Science · Saveetha School of Engineering (SIMATS)

A fully interactive algorithm visualizer built with Python and Streamlit. Visualize sorting and searching algorithms step-by-step, benchmark runtime across input sizes, and compare asymptotic complexities — all in a dark, monospace dashboard.

---

## Features

### Visualizer Panel
- **Live bar-chart animation** — watch the array transform step by step
- **Speed control** — dial animation from crawl to full speed
- **Search highlighting** — active index glows white, found index turns green
- **Complexity cards** — Best / Average / Worst / Space shown per algorithm
- **Runtime display** — actual measured ms + empirically fitted complexity class

### Benchmark Panel
- Runs each algorithm across `n = [10, 50, 100, 250, 500, 1000]`
- 3-trial average per size to reduce noise
- Bar chart + table with fitted vs theoretical complexity

### Complexity Reference Panel
- Cards for all 9 algorithms with full Big-O breakdown
- Growth function stacked-bar chart comparing O(1) → O(n²) across n = 1…20

---

## Algorithms Included

**Sorting (6)**
| Algorithm | Best | Average | Worst | Space |
|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |

**Searching (3)**
| Algorithm | Best | Average | Worst | Space |
|---|---|---|---|---|
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Jump Search | O(1) | O(√n) | O(√n) | O(1) |

---

## Input Types

| Type | Description |
|---|---|
| Random | Shuffled array with random values |
| Sorted | Already sorted (best case for some algos) |
| Reverse | Sorted descending (worst case for Bubble/Insertion) |
| Nearly Sorted | Sorted with ~5% random swaps |
| Duplicates | Array with many repeated values |

---

## Getting Started

### Prerequisites
- Python 3.9 or higher

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/algo-visualizer.git
cd algo-visualizer

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501` by default.

---

## Project Structure

```
algo-visualizer/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Dark theme + server config
├── .gitignore
└── README.md
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.9+ |
| Framework | Streamlit |
| Styling | Custom CSS injected via `st.markdown` |
| Animation | Frame-by-frame re-render with `time.sleep` |
| Font | JetBrains Mono (Google Fonts CDN) |

> No NumPy, Pandas, or Matplotlib required. Zero ML dependencies.  
> `random`, `math`, `time` — all Python stdlib.

---

## Deployment

### Streamlit Community Cloud (free)
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py` → Deploy

No extra config needed — `requirements.txt` and `.streamlit/config.toml` are picked up automatically.

---

## License

MIT
