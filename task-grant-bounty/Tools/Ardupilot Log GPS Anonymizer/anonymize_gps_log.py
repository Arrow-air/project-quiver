def anonymize_gps_log(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    output_lines = []

    # Confirmed field index mapping from your log
    field_indices = {
        "GPS":   {"Lat": 7, "Lng": 8, "Alt": 9},
        "AHR2":  {"Lat": 6, "Lng": 7},
        "EAHR":  {"Lat": 5, "Lng": 6},  # assumed
        "POS":   {"Lat": 2, "Lng": 3},  # ✅ corrected
        "TERR":  {"Lat": 3, "Lng": 4},  # ✅ corrected
        "ORGN":  {"Lat": 3, "Lng": 4}
    }

    for line in lines:
        line_stripped = line.strip()
        for msg_type, fields in field_indices.items():
            if line_stripped.startswith(msg_type):
                parts = line_stripped.split(',')
                try:
                    for field_name, index in fields.items():
                        if len(parts) > index:
                            parts[index] = "0"
                    line = ','.join(parts) + '\n'
                except IndexError:
                    pass
                break  # don't process the same line more than once
        output_lines.append(line)

    with open(output_path, 'w') as f:
        f.writelines(output_lines)

    print(f"✅ All GPS-related fields zeroed: {output_path}")




anonymize_gps_log("2025-04-25 13-29-57.log", "007-2025-04-25 13-29-57.log")
