# Full-Stack-Compiler

A comprehensive compiler implementation covering all stages from lexical analysis to machine code generation.

## Overview

The Full-Stack-Compiler is an educational and practical project that implements a complete compilation pipeline. Unlike interpreters that execute source code directly, this compiler transforms high-level code into optimized machine code through a series of well-defined stages.

## Architecture

This compiler follows the traditional three-phase architecture:

### 1. Front End

- **Lexical Analysis (Scanning)**: Processes source code through a Lexer using regular grammar to produce a token stream.
- **Syntax Analysis (Parsing)**: Employs a Parser with context-free grammar to transform tokens into a concrete parse tree.
- **Semantic Analysis**: Applies attribute grammar to build an abstract syntax tree (AST) that captures the program's essential meaning.

### 2. Middle End

- **Intermediate Representation (IR)**: Converts the AST into both high-level and low-level intermediate representations.
- **IR Lowering**: Transforms high-level IR into three-address code for optimization.
- **Optimization**: Implements various passes to eliminate redundant operations, simplify expressions, and improve performance.

### 3. Back End

- **Parallelism Preparation**: Identifies opportunities for parallel execution.
- **Register Allocation**: Efficiently assigns variables to hardware registers.
- **Code Generation**: Produces target machine code or assembly language.

## Features

- Complete compilation pipeline from source code to executable
- Modular architecture with clearly separated components
- Configurable optimization levels
- Detailed error reporting and debugging information
- Support for [language features to be implemented]

## Installation

```bash
git clone https://github.com/username/full-stack-compiler.git
cd full-stack-compiler
make install
```

## Usage

```bash
# Basic compilation
fsc source.xyz -o executable

# With optimization level
fsc source.xyz -o executable -O2

# Generate intermediate output
fsc source.xyz --emit=ir
```

## Project Structure

```
full-stack-compiler/
├── src/
│   ├── frontend/
│   │   ├── lexer/
│   │   ├── parser/
│   │   └── semantic/
│   ├── middleend/
│   │   ├── ir/
│   │   └── optimization/
│   └── backend/
│       ├── codegen/
│       └── register/
├── include/
├── tests/
├── examples/
└── docs/
```

## Development Roadmap

- [ ] Implement lexical analyzer
- [ ] Develop parser for context-free grammar
- [ ] Build semantic analyzer with attribute grammar
- [ ] Create intermediate representation
- [ ] Implement basic optimizations
- [ ] Develop code generation for target architecture
- [ ] Add advanced optimization passes
- [ ] Support multiple target architectures

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
