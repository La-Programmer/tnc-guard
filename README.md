# 🛡️ T&C Guard

**AI‑powered Terms & Conditions analyzer** — a privacy‑focused browser extension and cloud API that read lengthy Terms & Privacy policies, summarize them, highlight hidden clauses, and assign a transparent risk score so users know what they’re agreeing to.

---

### 🚀 Features
- **Smart Extraction** — Automatically detects T&C or Privacy pages and extracts readable text.
- **AI Analysis** — Uses a cloud LLM to identify risky clauses and produce human‑readable summaries.
- **Risk Scoring** — Converts findings into a clear A–F letter grade with rationale.
- **Inline Highlights** — Shows key risks directly inside the webpage.
- **Privacy‑First Mode (coming soon)** — Local model inference without sending data to servers.

---

### 🧱 Tech Stack
| Layer | Tools |
|--------|-------|
| **Extension** | React + TypeScript + Plasmo / WXT (MV3) |
| **Backend (Edge API)** | TypeScript + Cloudflare / Vercel Functions |
| **AI Layer** | Cloud LLM (OpenAI‑compatible JSON mode) |
| **Storage / Cache** | IndexedDB + KV Edge Cache |
| **Shared Contracts** | TypeScript schema (`Analysis`, `ClauseFinding`) |

---

### 📁 Repo Structure
```
tnc-guard/
├── apps/
│   ├── extension/     # Browser extension (MV3)
│   └── edge-api/      # Cloud inference API
├── packages/
│   ├── shared-schema/ # Shared TypeScript interfaces
│   └── utils/         # Reusable helpers
└── package.json       # pnpm workspaces root
```

---

### 🧩 Architecture Overview
```
[ Browser Page ] → [ Content Script ] → [ Cloud API / LLM ] → [ Analysis JSON ] → [ Popup / Sidebar UI ]
```

1. **Detection:** Content script checks URL/DOM for policy pages.
2. **Extraction:** Text is cleaned using Mozilla Readability.
3. **Analysis:** API sends normalized text to the LLM adapter.
4. **Aggregation:** Results merged, scored, and cached.
5. **Display:** Extension shows grade, summary, and highlights.

---

### 🧠 Roadmap
- [x] Cloud‑first LLM pipeline
- [ ] Local on‑device analysis (Transformers.js / WebGPU)
- [ ] Multi‑language support
- [ ] Organization dashboard (policy monitoring)

---

### 📜 License
MIT © 2025 T&C Guard Project
