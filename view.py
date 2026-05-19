import argparse
import sys
import os
import traceback

try:
    from nuscenes.utils.data_classes import RadarPointCloud
except ImportError:
    print("Please install nuscenes-devkit==1.1.11")
    sys.exit(1)

def read_pcd_header(path, max_lines=20):
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
