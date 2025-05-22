# Full-Stack-Compiler

![status-badge](https://img.shields.io/badge/status-WIP-orange)

An **end-to-end educational compiler** written in Python that translates **VGraph** source
code into an x86 executable, updates a `800 × 600` RGB memory buffer **in real time**, and—if
an HDMI port is detected—mirrors the live image to an external monitor.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [VGraph Language](#vgraph-language)
4. [Project Layout](#project-layout)
5. [Installation](#installation)
6. [Basic Usage](#basic-usage)
7. [Road-map](#road-map)
8. [Tool Stack](#tool-stack)
9. [License](#license)

---

## Overview

The goal is to cover **every** compilation phase:

| Phase          | Purpose                                      | Key Files                                                                         |
| -------------- | -------------------------------------------- | --------------------------------------------------------------------------------- |
| **Front-End**  | Lexical, syntactic & semantic analysis       | `CompilerLogic/lexicalAnalyzer.py`, `syntacticAnalyzer.py`, `semanticAnalyzer.py` |
| **Middle-End** | High‐ & low-level **LLVM IR** + optimisation | `intermediateCodeGenerator.py`, `ir/irBuilder.py`, `optimizer.py`                 |
| **Back-End**   | Register allocation & code emission          | `codeGenerator.py`                                                                |
| **Support**    | IDE/GUI, image viewer, file browser          | `GUI/`, `ExternalPrograms/`                                                       |

The produced executable (`out/vGraph.exe`) writes directly into
`out/image.bin`; the Python viewer (`ExternalPrograms/imageViewer.py`)
memory-maps that file and displays it via **SDL 2 / Pygame**.

---

## Architecture

```
┌──────────────┐     ┌────────────┐     ┌────────────┐
│  Lexer/      │──► │  IR &      │──► │  ASM/EXE    │
│  Parser      │     │  Optimiser │     │  Generator │
└──────────────┘     └────────────┘     └────────────┘
        ▲                   │                   │
        │   GUI/IDE         │ LLVM passes       │ HDMI output
```

* **ANTLR 4** grammar (`assets/VGraph.g4`) for lexing/parsing.
* **LLVM (llvmlite)** for IR, optimisation & x86 back-end.
* Fully modular pipeline with hot-reloading IR view inside the IDE.

---

## VGraph Language

### Main Tokens

* Drawing: `draw line|circle|rect|pixel`
* State: `setcolor`, `clear`, `wait`
* Flow: `frame`, `loop`, `if`, `else`, `return`
* Types: `(int)`, `(color)`, `(bool)`
* Math helpers: `cos()`, `sin()`, arithmetic `+ - * / %`
* Comments start with `#`.

### Syntax Rules (extract)

* **Declarations**  `(int) x = 42;`  |  `(color) r, g, b;`
* **Loops**   `loop (i = 0; i < 10; i = i + 1) { … }`
* **If / else-if chain** is written as nested `else { if (…) { … } }` (no `elif`).
* **Angles** are given in degrees; trig functions expect degrees.
* **Identifiers**: lower-case letter followed by ≤ 9 alphanumerics.
* Screen coordinates: `x ∈ [0,799]`, `y ∈ [0,599]`.

### Mini Example

```text
(int) i;
(color) c;
frame {
    loop (i = 0; i < 360; i = i + 10) {
        c = (i % 2 == 0) ? rojo : azul; # pseudo-ternary via if-else in real code
        setcolor(c);
        draw circle(400, 300, i / 4);
        wait(5);
    }
}
```

See more programs under **`Examples/`** (spiral, mandala, snowflake tree …).

---

## Project Layout

```
FULL-STACK-COMPILER
├── assets/
│   ├── Images/              # generated PNGs for visualisations
│   ├── VGraph.g4            # grammar
│   └── fonts/               # JetBrainsMono, …
├── CompilerLogic/
│   ├── ir/                  # low-level runtime + IR builder
│   │   ├── irBuilder.py
│   │   ├── runtime.c|h|o
│   │   ├── libvgraphrt.a
│   │   └── build_runtime.sh
│   ├── SemanticComponents/  # symbol table, type checker, …
│   │   ├── astVisitor.py …
│   ├── lexicalAnalyzer.py
│   ├── syntacticAnalyzer.py
│   ├── semanticAnalyzer.py
│   ├── intermediateCodeGenerator.py
│   ├── optimizer.py
│   └── codeGenerator.py
├── GUI/
│   ├── components/          # reusable buttons, textboxes
│   ├── views/
│   │   ├── editor_view.py
│   │   ├── lexical_analysis_view.py
│   │   ├── syntactic_analysis_view.py
│   │   ├── semantic_analysis_view.py
│   │   ├── ir_view.py       # NEW – LLVM IR viewer
│   │   ├── symbol_table_view.py
│   │   ├── grammar_view.py
│   │   ├── credits_view.py
│   │   └── config_view.py
│   ├── design_base.py
│   ├── view_base.py
│   └── view_controller.py
├── ExternalPrograms/
│   ├── fileExplorer.py
│   └── imageViewer.py       # mmap + SDL2 viewer
├── Examples/
│   ├── SnowflakeTree.txt
│   └── Mandala.txt …        # more demos
├── out/
│   ├── image.bin            # 800×600 × 24-bit
│   ├── vGraph.asm|exe|ll    # outputs of each back-end
│   └── vGraph.o             # object file
├── requirements.txt         # **new** – pinned versions of pygame, llvmlite, antlr4-runtime …
├── config.py                # global constants
├── design_settings.json     # GUI colour theme
├── main.py                  # CLI / GUI entry-point
├── LICENSE
└── README.md (this file)
```

---

## Installation

```bash
# 1 – clone repo
$ git clone https://github.com/<user>/full-stack-compiler.git
$ cd full-stack-compiler

# 2 – create venv
$ python3 -m venv .venv
$ source .venv/bin/activate

# 3 – install deps
$ pip install -r requirements.txt

# 4 – assembler & linker (Linux)
$ sudo apt-get install nasm gcc

# 5 – generate lexer/parser (first time or when VGraph.g4 changes)
$ antlr4 -Dlanguage=Python3 assets/VGraph.g4 -o assets
```

---

## Basic Usage

| Action                | Command                                                |
| --------------------- | ------------------------------------------------------ |
| Build EXE             | `python main.py build Examples/SnowflakeTree.txt`      |
| Build with -O2        | `python main.py build Examples/SnowflakeTree.txt -O2`  |
| Emit LLVM IR          | `python main.py ir Examples/SnowflakeTree.txt`         |
| Launch IDE GUI        | `python main.py gui`                                   |
| Live framebuffer view | `python ExternalPrograms/imageViewer.py out/image.bin` |

> The generated program writes into `out/image.bin`; the viewer refreshes the
> SDL window (and HDMI) at 60 FPS.

---

## Road-map

1. **IDE & framework integration** – *done*
2. **Lexical + syntactic analysis** – *done*
3. **Semantic analysis** – *done*
4. **IR + basic optimiser** – in progress
5. **x86 code generator** – TBD
6. **Real-time HDMI visualisation** – TBD

---

## Tool Stack

| Purpose            | Tech                                 |
| ------------------ | ------------------------------------ |
| Main language      | Python 3.12                          |
| Lexer / Parser     | **ANTLR 4** (Python runtime)         |
| IR & back-end      | **LLVM** via `llvmlite`              |
| Assembler / Linker | `nasm`, `gcc`                        |
| Visualisation      | `pygame`, `PySDL2`, `mmap`, `pyudev` |
| GUI                | Custom MVC (Pygame + SDL2)           |
| Target OS          | Linux (Ubuntu 22.04)                 |

---

## License

Released under the **MIT License**. See [LICENSE](LICENSE) for details.