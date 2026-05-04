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

### Synthesizing Elapsed Time

If you want the activity to show a specific elapsed time (e.g., 5 minutes), use the `-t` or `--elapsed` flag:

```bash
# Sets elapsed time to 300 seconds (5 minutes)
python solve_pka.py lab.pka -t 300
```

## Command Line Options

| Option | Description |
|--------|-------------|
| input_file | Input `.pka` file (required) |
| -o, --output | Output `.pka` path (optional) |
| -t, --elapsed | Synthesize elapsed time in seconds (optional) |
| -h, --help | Show help message |

## How It Works

The script executes a three-step pipeline:

1.  **Unpacket**: Decrypts the `.pka` file into an intermediate XML format (`_temp.xml`).
2.  **Solve**:
    - Parses the XML and identifies all `PACKETTRACER5` blocks.
    - Replaces the **Student Block** (Block 1) with the **Answer Key Block** (the last block).
    - This ensures all devices, links, configurations, and grading metadata are perfectly synchronized.
    - If specified, replaces the `ELAPSED` attribute in the XML to synthesize a custom time (automatically converting input seconds to the required milliseconds).
    - Saves the corrected XML as `_solved.xml`.
3.  **Repacket**: Encrypts the solved XML back into a functional `.pka` file.

## Tested on Cisco Packet Tracker v7 and v9. Some older versions might fail to decompile.