# Full‑Stack‑Compiler

![status-badge](https://img.shields.io/badge/status-WIP-orange)

An **end‑to‑end educational compiler** written in Python that translates **VGraph** source
code into an x86 executable, updates a `800 × 600` memory buffer **in real time**, and—if
an HDMI port is detected—mirrors the live image to an external monitor. citeturn0file0

---

## Table of Contents
1. [Overview](#overview)  
2. [Architecture](#architecture)  
3. [VGraph Language](#vgraph-language)  
4. [Project Layout](#project-layout)  
5. [Installation](#installation)  
6. [Basic Usage](#basic-usage)  
7. [Road‑map (Sprints)](#road-map-sprints)  
8. [Tool Stack](#tool-stack)  
9. [License](#license)  

---

## Overview
The goal is to cover **every** compilation phase:

| Phase | Purpose | Key Files |
|-------|---------|-----------|
| Front End | Lexical, syntactic, and semantic analysis | `CompilerLogic/lexicalAnalyzer.py`, `syntacticAnalyzer.py`, `semanticAnalyzer.py` |
| Middle End | High‑ & low‑level IR + optimisations | `intermediateCodeGenerator.py`, `optimizer.py` |
| Back End | Register allocation & code generation | `codeGenerator.py` |
| Support | IDE/GUI, image viewer, file browser | `GUI/`, `ExternalPrograms/` |

The produced executable (`out/vGraph.exe`) writes directly into
`out/image.bin`; the Python viewer (`ExternalPrograms/imageViewer.py`)
memory‑maps that file and displays it via **SDL 2 / Pygame**. citeturn0file0

---

## Architecture
```
┌──────────────┐     ┌────────────┐     ┌────────────┐
│  Lexer/      │──► │  IR &      │──► │  ASM/EXE    │
│  Parser      │     │  Optimiser │     │  Generator │
└──────────────┘     └────────────┘     └────────────┘
        ▲                   │                   │
        │ GUI/IDE           │ LLVM passes       │ HDMI output
```

* **ANTLR 4** grammar (`assets/VGraph.g4`) for lexing/parsing.  
* **LLVM (llvmlite)** for IR, optimisation, and x86 back‑end.  
* Fully modular pipeline. citeturn0file0

---

## VGraph Language
### Main Tokens
Keywords like `draw`, `setcolor`, `frame`, `loop`, `if`, `else`, etc.
Identifiers are **alphanumeric, ≤ 10 chars, start with a lowercase letter**.
Integers range 0‑639 / 0‑479. Comments start with `#`. citeturn0file0  

### Minimal Example
```text
(color) c = red;
frame {
    loop (i = 0; i < 100; i = i + 10) {
        draw circle(i, 120, 15);
        wait(3);
    }
}
```
Larger programs (spiral, mandala, fractal tree) live in `Examples/`. citeturn0file0  

---

## Project Layout
```
FULL-STACK-COMPILER
├── assets/                 # Grammar, fonts, sample images
│   ├── Images/ej?.png
│   └── VGraph.g4
├── CompilerLogic/          # Compiler core
│   ├── lexicalAnalyzer.py
│   ├── syntacticAnalyzer.py
│   ├── semanticAnalyzer.py
│   ├── intermediateCodeGenerator.py
│   ├── optimizer.py
│   └── codeGenerator.py
├── GUI/                    # Minimal IDE (MVC)
│   ├── components/…        # button.py, textbox.py, …
│   ├── models/execute_model.py
│   ├── views/
│   │   ├── editor_view.py
│   │   ├── grammar_view.py
│   │   ├── lexical_analysis_view.py
│   │   └── … (other views WIP)
│   └── view_controller.py
├── ExternalPrograms/       # Auxiliary tools
│   ├── fileExplorer.py
│   └── imageViewer.py
├── Examples/Test?.txt      # Test cases
├── out/                    # Build artefacts
│   ├── image.bin
│   ├── vGraph.asm
│   └── vGraph.exe
├── config.py               # Global settings
├── design_settings.json    # GUI theme
├── main.py                 # CLI / GUI entry‑point
└── README.md
```

---

## Installation
```bash
# 1 – clone repo
git clone https://github.com/<user>/full-stack-compiler.git
cd full-stack-compiler

# 2 – create venv
python3 -m venv .venv
source .venv/bin/activate

# 3 – install deps
pip install -r requirements.txt   # pygame, llvmlite, antlr4-python3-runtime, …

# 4 – assembler & linker (Linux)
sudo apt-get install nasm gcc

# 5 – generate lexer/parser (first time or on .g4 change)
antlr4 -Dlanguage=Python3 assets/VGraph.g4 -o assets
```

---

## Basic Usage

| Action | Command |
|--------|---------|
| Compile → `.exe` | `python main.py build Examples/Test1.txt` |
| Compile + O2     | `python main.py build Examples/Test1.txt -O2` |
| Emit IR          | `python main.py ir Examples/Test1.txt` |
| Launch IDE GUI   | `python main.py gui` |
| Live image view  | `python ExternalPrograms/imageViewer.py out/image.bin` |

> The generated executable writes into `out/image.bin`;  
> the viewer maps that buffer and refreshes the SDL window / HDMI at 60 FPS.

---

## Road‑map (Sprints)
1. **IDE & framework integration**  
2. **Lexical + syntactic analysis**  
3. **Semantic analysis**  
4. **IR + basic optimiser**  
5. **x86 code generator**  
6. **Real‑time HDMI visualisation** citeturn0file0  

---

## Tool Stack
| Purpose | Tech |
|---------|------|
| Main language | Python 3.12 |
| Lexer / Parser | **ANTLR 4** |
| IR & back‑end | **llvmlite** (LLVM) |
| Assembler / Linker | `nasm`, `gcc` |
| Visualisation | `pygame` / `PySDL2`, `mmap`, `pyudev` |
| GUI | Custom MVC + SDL2 |
| Target OS | Linux (Ubuntu) | citeturn0file0 |

---

## License
Released under the **MIT License**. See [LICENSE](LICENSE) for details.
