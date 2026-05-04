# solve-pka

**solve-pka** is a command-line utility designed to solve Cisco Packet Tracer (`.pka`) activities by fixing incorrectly placed or missing logical components in the XML representation.

## Features

- **Automated XML Logic Correction**

  - Detects and fixes mispositioned `DEVICES` and `LINKS` blocks.
  - Extracts the correct topology from the Answer Key section and injects it into the student's Current layer.
- **Wrapper Script**

  - Chains `unpacket.py` → custom solving logic → `repacket.py` for a seamless workflow.
- **Temporary File Management**

  - Automatically cleans up intermediate XML files.

## Installation

Ensure you have the following Python scripts in your directory:

- `unpacket.py`
- `repacket.py`

No additional packages are required.

## Usage

Run the script with the path to the `.pka` file:

```bash
python solve_pka.py lab.pka
```

This will generate a new file named `lab_SOLVED.pka`.

You can specify a custom output path using the `-o` flag:

```bash
python solve_pka.py lab.pka -o my_fixed_lab.pka
```

## Command Line Options

| Option | Description |
|--------|-------------|
| input_file | Input `.pka` file (required) |
| -o, --output | Output `.pka` path (optional) |
| -h, --help | Show help message |

## How It Works

The script executes a three-step pipeline:

1.  **Unpacket**: Decrypts the `.pka` file into an intermediate XML format (`_temp.xml`).
2.  **Solve**:
    - Parses the XML and identifies the "Answer Key" section (Block 3).
    - Extracts the correct `DEVICES` and `LINKS` structures from the Answer Key.
    - Replaces the corresponding sections in the "Current" layer (Block 1).
    - Saves the corrected XML as `_solved.xml`.
3.  **Repacket**: Encrypts the solved XML back into a functional `.pka` file.