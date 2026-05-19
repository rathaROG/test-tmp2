import argparse
import sys
import numpy as np

try:
    from nuscenes.utils.data_classes import RadarPointCloud
except ImportError:
    print("Please install nuscenes-devkit==1.1.11")
    sys.exit(1)

def read_pcd_header(path, max_lines=20):
    """Read the ASCII header of a PCD file up to max_lines lines."""
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

def main():
    parser = argparse.ArgumentParser(description="View basic info of a nuScenes radar PCD file.")
    parser.add_argument("pcd_path", type=str, help="Path to the radar .pcd file.")
    parser.add_argument("--show-points", action="store_true", help="Print the first 5 points.")
    args = parser.parse_args()

    print(f"Reading PCD file: {args.pcd_path}")
    print("\n--- PCD HEADER ---")
    header = read_pcd_header(args.pcd_path)
    for line in header:
        print(line)

    print("\n--- RadarPointCloud from_file ---")
    try:
        rpc = RadarPointCloud.from_file(args.pcd_path)
        points = rpc.points
        print(f"Shape of points array: {points.shape}")
        print(f"Number of points: {points.shape[1]}")
        if args.show_points:
            print(f"\nFirst 5 points (columns):\n{points[:, :5]}")
    except Exception as e:
        print(f"Failed to load radar file with RadarPointCloud.from_file().\nError: {e}")

if __name__ == "__main__":
    main()
