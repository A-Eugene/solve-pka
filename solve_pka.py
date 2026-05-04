import re
import os
import sys
import argparse
import subprocess

def solve_xml_logic(input_xml, output_xml):
    with open(input_xml, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    blocks = re.split(r'(<PACKETTRACER5>)', content)
    if len(blocks) < 7:
        print("[-] Error: Could not find enough network blocks in XML.")
        return False

    # 1. Copy DEVICES from Block 3 (Answer Key) to Block 1 (Student Current)
    answer_devices_match = re.search(r'(<DEVICES>.*?</DEVICES>)', blocks[6], re.DOTALL)
    if not answer_devices_match:
        print("[-] Error: Could not find DEVICES in Answer Key.")
        return False
    answer_devices = answer_devices_match.group(1)
    new_block1 = re.sub(r'<DEVICES>.*?</DEVICES>', answer_devices, blocks[2], flags=re.DOTALL)

    # 2. Copy LINKS (The Wires)
    answer_links_match = re.search(r'(<LINKS>.*?</LINKS>)', blocks[6], re.DOTALL)
    if not answer_links_match:
        print("[-] Error: Could not find LINKS in Answer Key.")
        return False
    answer_links = answer_links_match.group(1)
    new_block1 = re.sub(r'<LINKS[^>]*>.*?</LINKS>|<LINKS\s*/>', answer_links, new_block1, flags=re.DOTALL)
    
    new_content = blocks[0] + blocks[1] + new_block1 + blocks[3] + blocks[4] + blocks[5] + blocks[6] + "".join(blocks[7:])
    
    with open(output_xml, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    parser = argparse.ArgumentParser(description="Unpacket, Solve, and Repacket a Cisco Packet Tracer Activity.")
    parser.add_argument("input_file", help="Path to the .pka or .pkt file.")
    parser.add_argument("-o", "--output", help="Path to the output .pka file. Defaults to <input>_SOLVED.pka")
    
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
        if not solve_xml_logic(temp_xml, solved_xml):
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
