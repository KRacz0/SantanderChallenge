import re
import json
import sys

def extract_value(log_line, pattern, group_index=0):
    match = re.search(pattern, log_line)
    if match:
        return match.group(group_index)
    return None

def convert_to_mb(value):
    if value is None:
        return "0"
    if 'M' in value:
        result = float(value.replace('M', ''))
    elif 'K' in value:
        result = float(value.replace('K', '')) / 1024
    elif 'B' in value:
        result = float(value.replace('B', '')) / (1024 * 1024)
    else:
        result = float(value)

    if result == 0.0:
        return "0"
    return str(result)

def parse_gc_log(input_file, output_file):
    gc_pause_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{4}):.*\[(GC pause \([^\)]+\))')
    eden_pattern_before = re.compile(r'Eden: (\d+\.\d+[A-Za-z]*)')
    eden_pattern_after = re.compile(r'->(\d+\.\d+[A-Za-z]*)')
    survivors_pattern_before = re.compile(r'Survivors: (\d+\.\d+[A-Za-z]*)')
    survivors_pattern_after = re.compile(r'Survivors: \d+\.\d+[A-Za-z]*->(\d+\.\d+[A-Za-z]*)')
    heap_pattern_before = re.compile(r'Heap: (\d+\.\d+[A-Za-z]*)\(\d+\.\d+[A-Za-z]*\)')
    heap_pattern_after = re.compile(r'Heap: \d+\.\d+[A-Za-z]*\(\d+\.\d+[A-Za-z]*\)->(\d+\.\d+[A-Za-z]*)')

    entries = []
    current_timestamp = None
    current_gc_name = None

    with open(input_file, 'r') as file:
        for line in file:
            gc_pause_match = gc_pause_pattern.search(line)
            if gc_pause_match:
                current_timestamp = gc_pause_match.group(1)
                current_gc_name = gc_pause_match.group(2)
            elif "Eden" in line:
                eden_before = extract_value(line, eden_pattern_before, 1)
                eden_after = extract_value(line, eden_pattern_after, 1)
                survivors_before = extract_value(line, survivors_pattern_before, 1)
                survivors_after = extract_value(line, survivors_pattern_after, 1)
                heap_before = extract_value(line, heap_pattern_before, 1)
                heap_after = extract_value(line, heap_pattern_after, 1)

                entries.append({
                    "timestamp": current_timestamp,
                    "eden_size": convert_to_mb(eden_before),
                    "survivors_size": convert_to_mb(survivors_before).split('.')[0],
                    "heap_size": convert_to_mb(heap_before),
                    "GC_name": current_gc_name,
                    "phase": "before"
                })
                entries.append({
                    "timestamp": current_timestamp,
                    "eden_size": convert_to_mb(eden_after),
                    "survivors_size": convert_to_mb(survivors_after).split('.')[0],
                    "heap_size": convert_to_mb(heap_after),
                    "GC_name": current_gc_name,
                    "phase": "after"
                })

    with open(output_file, 'w') as json_file:
        json.dump(entries, json_file, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Poprawne Użycie: python parse_gc_log.py <nazwa_pliku_wejściowego> <nazwa_pliku_wyjściowego>")
        sys.exit(1)

    input_log_file = sys.argv[1]
    output_json_file = sys.argv[2]

    parse_gc_log(input_log_file, output_json_file)
    print(f"Plik wyjściowy: {output_json_file}")
