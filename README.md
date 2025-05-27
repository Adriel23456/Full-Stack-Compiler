# Full-Stack-Compiler

![status-badge](https://img.shields.io/badge/status-COMPLETE-green)
![platform-badge](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue)
![python-badge](https://img.shields.io/badge/python-3.7+-yellow)
![license-badge](https://img.shields.io/badge/license-MIT-purple)

An **end-to-end educational compiler** written in Python that translates **VGraph** source code into native executables, updates an `800 × 600` RGB memory buffer **in real time**, and supports **HDMI output** for external monitor visualization.

**✨ 100% Cross-Platform Compatible: Windows & Linux**

---

## 🎯 Key Features

- **Complete Compiler Pipeline**: From lexical analysis to native code generation
- **Cross-Platform**: Fully compatible with Windows and Linux
- **Real-Time Visualization**: Live preview of graphics output
- **HDMI Support**: Mirror output to external displays
- **Integrated IDE**: Custom-built development environment
- **Educational Design**: Clear separation of compilation phases

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [VGraph Language](#vgraph-language)
4. [Cross-Platform Compatibility](#cross-platform-compatibility)
5. [Project Layout](#project-layout)
6. [Installation](#installation)
7. [Usage Guide](#usage-guide)
8. [Execution Modes](#execution-modes)
9. [Development Status](#development-status)
10. [Tool Stack](#tool-stack)
11. [Contributing](#contributing)
12. [License](#license)

---

## Overview

This compiler covers **every** compilation phase:

| Phase          | Purpose                                      | Key Files                                                                         |
| -------------- | -------------------------------------------- | --------------------------------------------------------------------------------- |
| **Front-End**  | Lexical, syntactic & semantic analysis       | `CompilerLogic/lexicalAnalyzer.py`, `syntacticAnalyzer.py`, `semanticAnalyzer.py` |
| **Middle-End** | High‐ & low-level **LLVM IR** + optimization | `intermediateCodeGenerator.py`, `ir/irBuilder.py`, `optimizer.py`                 |
| **Back-End**   | Register allocation & native code emission   | `codeGenerator.py`                                                                |
| **Runtime**    | Graphics buffer management & HDMI output     | `Ir/runtime.c`, `ExternalPrograms/`                                              |
| **IDE**        | Integrated development environment           | `GUI/`, `main.py`                                                                 |

The compiler produces platform-specific executables that write directly to a shared memory buffer (`out/image.bin`), which is then displayed by the visualization components.

---

## Architecture

```
┌──────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Source Code     │     │                 │     │                 │
│  (.vgraph)       │───▶│  Lexer/Parser   │────▶│ Semantic        │
│                  │     │  (ANTLR 4)      │     │ Analyzer        │
└──────────────────┘     └─────────────────┘     └─────────────────┘
                                                            │
                                                            ▼
┌──────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Native Code     │     │  Code           │     │  IR Generator   │
│  (.exe)          │◀───│  Generator       │◀───│  & Optimizer    │
│                  │     │  (LLVM)         │     │  (LLVM)         │
└──────────────────┘     └─────────────────┘     └─────────────────┘
         │                                                 
         ▼                                                 
┌──────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  HDMI Output     │◀────│  Visualizer     │◀────│  Memory Buffer  │
│  (External)      │     │  (SDL2/Pygame)  │     │  (image.bin)    │
└──────────────────┘     └─────────────────┘     └─────────────────┘
```

### Key Components:
* **ANTLR 4** grammar (`assets/VGraph.g4`) for lexing/parsing
* **LLVM (llvmlite)** for IR generation, optimization & native code emission
* **SDL2/Pygame** for cross-platform graphics visualization
* **Custom Runtime** for memory buffer management and HDMI output

---

## VGraph Language

VGraph is a domain-specific language designed for educational graphics programming.

### Language Features

* **Drawing Primitives**: `draw line|circle|rect|pixel`
* **State Management**: `setcolor`, `clear`, `wait`
* **Control Flow**: `frame`, `loop`, `if`, `else`, `return`
* **Type System**: `(int)`, `(color)`, `(bool)`
* **Built-in Functions**: `cos()`, `sin()`, arithmetic operators `+ - * / %`
* **Comments**: Single-line comments with `#`

### Syntax Rules

* **Variable Declaration**: `(int) x = 42;` | `(color) r, g, b;`
* **Loop Structure**: `loop (i = 0; i < 10; i = i + 1) { … }`
* **Conditional Logic**: `if (condition) { … } else { … }`
* **Coordinate System**: Screen space `x ∈ [0,799]`, `y ∈ [0,599]`
* **Angle Units**: All trigonometric functions use degrees
* **Identifier Rules**: Start with lowercase letter, max 15 alphanumeric characters

### Example: Animated Spiral

```vgraph
# Spiral animation with color transitions
(int) x, y, t, radius;
(color) c;

frame {
    clear();
    loop (t = 0; t < 720; t = t + 5) {
        # Calculate spiral coordinates
        radius = t / 4;
        x = 400 + radius * cos(t);  # Center X = 400
        y = 300 + radius * sin(t);  # Center Y = 300
        
        # Cycle through colors
        if (t % 3 == 0) { 
            c = rojo; 
        } else if (t % 3 == 1) { 
            c = azul; 
        } else { 
            c = verde; 
        }
        
        setcolor(c);
        draw pixel(x, y);
        wait(50);  # Animation delay
    }
}
```

More examples available in the **`Examples/`** directory.

---

## Cross-Platform Compatibility

The compiler is **100% compatible** with both Windows and Linux:

### Platform-Specific Executables

| Component | Windows | Linux |
|-----------|---------|-------|
| Client Launcher | `Client_execute_windows.exe` | `Client_execute_linux` |
| HDMI Launcher | `HDMI_execute_windows.exe` | `HDMI_execute_linux` |
| Compiled Output | `vGraph.exe` | `vGraph` |

### Terminal Support

- **Windows**: CMD, PowerShell
- **Linux**: gnome-terminal, konsole, xfce4-terminal, xterm, terminator

### Automatic Platform Detection

The system automatically detects your OS and uses the appropriate:
- Executable formats
- Terminal emulators
- Path separators
- System commands

For unsupported operating systems, the message "OS [name] integration: Not yet implemented" will be displayed.

---

## Project Layout

```
FULL-STACK-COMPILER/
├── assets/
│   ├── Images/                      # Generated visualizations
│   ├── VGraph.g4                    # ANTLR grammar definition
│   └── fonts/                       # UI fonts (JetBrainsMono)
├── CompilerLogic/
│   ├── Ir/                          # LLVM IR and runtime
│   │   ├── irBuilder.py             # IR construction
│   │   ├── runtime.c|h              # C runtime library
│   │   ├── libvgraphrt.a            # Static runtime library
│   │   └── build_runtime.sh         # Runtime build script
│   ├── SemanticComponents/          # AST and semantic analysis
│   ├── lexicalAnalyzer.py           # Tokenization
│   ├── syntacticAnalyzer.py         # Parsing
│   ├── semanticAnalyzer.py          # Type checking & validation
│   ├── intermediateCodeGenerator.py # IR generation
│   ├── optimizer.py                 # LLVM optimization passes
│   └── codeGenerator.py             # Native code emission
├── GUI/
│   ├── components/                  # Reusable UI components
│   ├── views/                       # IDE views
│   │   ├── editor_view.py           # Code editor
│   │   ├── lexical_analysis_view.py # Token visualization
│   │   ├── syntactic_analysis_view.py # AST visualization
│   │   ├── semantic_analysis_view.py  # Semantic errors
│   │   ├── ir_view.py               # LLVM IR display
│   │   ├── optimizer_view.py        # Optimization passes
│   │   ├── code_generator_view.py   # Assembly output
│   │   └── symbol_table_view.py     # Symbol table viewer
│   ├── models/
│   │   ├── fileExplorer.py          # File browser
│   │   └── execute_model.py         # Cross-platform execution
│   └── view_controller.py           # MVC controller
├── Examples/                        # Sample VGraph programs
│   ├── Test0.txt                    # Basic shapes
│   ├── Test1.txt                    # Animation demo
│   ├── Test2.txt                    # Color manipulation
│   ├── Test3.txt                    # Mathematical curves
│   ├── Test6(ComplexFigure).txt     # Advanced graphics
│   ├── Test7(LexerError).txt        # Error handling demo
│   ├── Test8(SyntacticError).txt    # Parser error demo
│   └── Test11(SemanticError3).txt   # Semantic error demo
├── ExternalPrograms/
│   ├── imageViewer.py               # Memory-mapped display
│   └── hdmiOutput.py                # HDMI output handler
├── out/                             # Compiler output directory
│   ├── image.bin                    # 800×600×24-bit buffer
│   ├── vGraph.exe/                  # Compiled program
│   ├── Client_execute_*             # Platform launchers
│   └── HDMI_execute_*               # HDMI launchers
├── setup_dependencies.py            # Automated setup script
├── requirements.txt                 # Python dependencies
├── config.py                        # Global configuration
├── design_settings.json             # IDE theme settings
├── main.py                          # Entry point
├── LICENSE                          # MIT License
└── README.md                        # This file
```

---

## Installation

### Prerequisites

- Python 3.7 or higher
- Git
- Administrator/sudo privileges (for system packages)

### Quick Install

```bash
# 1. Clone the repository
git clone https://github.com/Adriel23456/Full-Stack-Compiler.git
cd Full-Stack-Compiler

# 2. Run the automated setup script
python setup_dependencies.py

# 3. Launch the IDE
python main.py
```

### Platform-Specific Requirements

#### Windows
- Visual Studio Build Tools or MinGW-w64
- Java Runtime Environment (JRE)

#### Linux
- GCC/Clang compiler
- SDL2 development libraries
- X11 development headers
- Java Runtime Environment (JRE)

The setup script will automatically detect your platform and install all necessary dependencies.

---

## Usage Guide

### IDE Mode (Recommended)

```bash
python main.py
```

This launches the integrated development environment with:
- Syntax highlighting editor
- Real-time compilation feedback
- Visual analysis tools for each compilation phase
- Integrated execution and visualization

---

## Execution Modes

### 1. Client Mode
Standard execution with local display window:
- Click "Execute Client" in the IDE
- Or run the platform-specific launcher directly

### 2. HDMI Mode
For external monitor output:
- Connect HDMI display
- Click "Execute HDMI" in the IDE
- The output will mirror to the external display

### 3. Development Mode
For debugging and analysis:
- Use the IDE's analysis views
- Step through compilation phases
- Examine IR and assembly output

---

## Development Status

### ✅ Completed Features

1. **Full Compiler Pipeline** - All phases implemented
2. **Cross-Platform Support** - Windows & Linux compatibility
3. **Integrated IDE** - Custom development environment
4. **Real-Time Visualization** - Live graphics preview
5. **HDMI Output** - External display support
6. **Error Handling** - Comprehensive error messages
7. **Optimization** - LLVM optimization passes
8. **Example Programs** - Educational samples included

### 🎉 Project Status: COMPLETE

The Full-Stack Compiler is now feature-complete and ready for educational use!

---

## Tool Stack

| Component          | Technology                           |
| ------------------ | ------------------------------------ |
| Language           | Python 3.7+                          |
| Parser Generator   | **ANTLR 4** (Python runtime)         |
| IR & Backend       | **LLVM** via `llvmlite`              |
| Native Toolchain   | `clang`, `gcc`, MSVC                 |
| Graphics           | `pygame`, `PySDL2`                   |
| Memory Mapping     | `mmap` (cross-platform)              |
| GUI Framework      | Custom MVC with Pygame               |
| Target Platforms   | Windows 10/11, Linux (Ubuntu 20.04+) |

---

### Areas for Contribution
- Support for macOS
- Additional VGraph language features
- More example programs
- Documentation improvements
- Performance optimizations

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- ANTLR team for the excellent parser generator
- LLVM project for the compilation infrastructure
- SDL/Pygame communities for graphics support
- All contributors and testers

---

## Contact

**Project Author**: Adriel23456  
**Repository**: [https://github.com/Adriel23456/Full-Stack-Compiler](https://github.com/Adriel23456/Full-Stack-Compiler)

Feel free to open an issue for questions, bug reports, or feature requests!