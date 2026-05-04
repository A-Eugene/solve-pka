import re
import os
import sys
import argparse
import subprocess

def solve_xml_logic(input_xml, output_xml, elapsed_time=None):
    with open(input_xml, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find all complete <PACKETTRACER5> ... </PACKETTRACER5> blocks using regex
    # Usually: Block 0 is Current, Block 1 is Initial, Block 2 is Answer Key
    # We always want the last one as the Answer Key.
    pattern = r'<PACKETTRACER5>.*?</PACKETTRACER5>'
    pt5_blocks = re.findall(pattern, content, flags=re.DOTALL)

    if len(pt5_blocks) < 2:
        print("[-] Error: Could not find both Student and Answer Key networks in the XML.")
        return False

    student_block = pt5_blocks[0]
    answer_block = pt5_blocks[-1] # Use the last block as the answer key

    # Completely overwrite the Student Block with the Answer Key Block.
    # This copies everything: devices, links, configs, and grading metadata.
    new_content = content.replace(student_block, answer_block, 1)
    
    # Synthesize elapsed time if requested (input is in seconds, XML uses milliseconds)
    if elapsed_time is not None:
        ms_time = elapsed_time * 1000
        print(f"[*] Synthesizing elapsed time to {elapsed_time} seconds ({ms_time} ms)...")
        new_content = re.sub(r'ELAPSED="\d+"', f'ELAPSED="{ms_time}"', new_content)

    with open(output_xml, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    parser = argparse.ArgumentParser(description="Unpacket, Solve, and Repacket a Cisco Packet Tracer Activity.")
    parser.add_argument("input_file", help="Path to the .pka or .pkt file.")
    parser.add_argument("-o", "--output", help="Path to the output .pka file. Defaults to <input>_SOLVED.pka")
    parser.add_argument("-t", "--elapsed", type=int, help="Synthesize elapsed time (in seconds).")
    
    args = parser.parse_args()
    input_path = args.input_file
    
    if not os.path.exists(input_path):
        print(f"[-] Error: File '{input_path}' not found.")
        sys.exit(1)

    # Determine paths
    base_name = os.path.splitext(input_path)[0]
    temp_xml = base_name + "_temp.xml"
    solved_xml = base_name + "_solved.xml"
    output_pka = args.output if args.output else base_name + "_SOLVED.pka"

    try:
        # 1. Unpacket
        print(f"[*] Unpacketing '{input_path}'...")
        subprocess.run([sys.executable, "unpacket.py", input_path, "-o", temp_xml], check=True)

        # 2. Solve
        print(f"[*] Solving XML logic...")
        if not solve_xml_logic(temp_xml, solved_xml, elapsed_time=args.elapsed):
            sys.exit(1)

        # 3. Repacket
        print(f"[*] Repacketing into '{output_pka}'...")
        subprocess.run([sys.executable, "repacket.py", solved_xml, "-o", output_pka], check=True)

        print(f"[+] Success! Solved activity saved to '{output_pka}'")

    except subprocess.CalledProcessError as e:
        print(f"[-] Subprocess failed: {e}")
    finally:
        # 4. Cleanup
        print("[*] Cleaning up temporary files...")
        if os.path.exists(temp_xml):
            os.remove(temp_xml)
        if os.path.exists(solved_xml):
            os.remove(solved_xml)

if __name__ == "__main__":
    main()