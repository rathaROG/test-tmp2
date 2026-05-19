import argparse
import sys
import os
import traceback

try:
    from nuscenes.utils.data_classes import RadarPointCloud
except ImportError:
    print("Please install nuscenes-devkit==1.1.11")
    sys.exit(1)

def read_pcd_header(path, max_lines=40):
    header = []
    with open(path, "rb") as f:
        for _ in range(max_lines):
            line = f.readline()
            if not line:
                break
            header.append(line.decode("utf-8", "ignore").strip())
            if header[-1].startswith("DATA"):
                break
    return header

def check_pcd_size(header, path):
    fields = sizes = counts = width = None
    data_line_num = 0
    for i, line in enumerate(header):
        if line.startswith("FIELDS"):
            fields = line.split()[1:]
        if line.startswith("SIZE"):
            sizes = list(map(int, line.split()[1:]))
        if line.startswith("COUNT"):
            counts = list(map(int, line.split()[1:]))
        if line.startswith("WIDTH"):
            width = int(line.split()[1])
        if line.startswith("DATA"):
            data_line_num = i

    if not (fields and sizes and counts and width):
        print("Could not parse all necessary header info for size check.")
        return False, 0, 0, 0

    points_per_point = sum([s * c for s, c in zip(sizes, counts)])
    expected_points = width
    expected_bin_size = points_per_point * expected_points

    # Find offset in file where binary data starts (after header)
    with open(path, "rb") as f:
        offset = 0
        for _ in range(data_line_num + 1):
            line = f.readline()
            offset += len(line)
    file_size = os.stat(path).st_size
    actual_bin_size = file_size - offset

    print(f"Expected binary data size (from header): {expected_bin_size} bytes")
    print(f"Actual binary data size in file:        {actual_bin_size} bytes")

    if actual_bin_size < expected_bin_size:
        print("Warning: File binary data is smaller than expected! File may be truncated or format may not match.")
        return False, expected_bin_size, actual_bin_size, offset
    elif actual_bin_size > expected_bin_size:
        print("Warning: File binary data is larger than expected! File may have extra data or unexpected format.")
        return True, expected_bin_size, actual_bin_size, offset
    else:
        print("Binary data size matches header.")
        return True, expected_bin_size, actual_bin_size, offset

def main():
    parser = argparse.ArgumentParser(description="Safely view basic info of a nuScenes radar PCD file, with header and data size sanity check.")
    parser.add_argument("pcd_path", type=str, help="Path to the radar .pcd file.")
    parser.add_argument("--show-points", action="store_true", help="Print the first N points.")
    parser.add_argument("--num-points", type=int, default=5, help="Number of points to show (default: 5).")
    parser.add_argument("--debug", action="store_true", help="Print full exception tracebacks.")
    args = parser.parse_args()

    if not os.path.isfile(args.pcd_path):
        print(f"File does not exist: {args.pcd_path}")
        sys.exit(1)

    print(f"Reading PCD file: {args.pcd_path}")
    print("\n--- PCD HEADER ---")
    header = read_pcd_header(args.pcd_path)
    for line in header:
        print(line)

    # Size check
    print("\n--- PCD BINARY DATA SIZE CHECK ---")
    ok, exp, act, offset = check_pcd_size(header, args.pcd_path)

    if not ok:
        print("\nSanity check failed: Skipping RadarPointCloud.from_file() to avoid crash.")
        sys.exit(1)

    print("\n--- RadarPointCloud from_file ---")
    try:
        rpc = RadarPointCloud.from_file(args.pcd_path)
        points = rpc.points
        print(f"Shape of points array: {points.shape} (attributes x points)")
        print(f"Number of points: {points.shape[1]}")
        print(f"Data type: {points.dtype}")
        if args.show_points:
            n = min(args.num_points, points.shape[1])
            print(f"\nFirst {n} points (columns):\n{points[:, :n]}")
            print("RadarPointCloud attribute convention: X, Y, Z, dyn_prop, id, rcs, vx, vy, vx_comp, vy_comp, is_quality_valid, time, doppler_bin")
    except Exception as e:
        print(f"Failed to load radar file with RadarPointCloud.from_file().\nError: {e}")
        if args.debug:
            traceback.print_exc()

if __name__ == "__main__":
    main()
