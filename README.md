### Requirements

```bash
# linux only ? maybe it does not work on other os
pip install nuscenes-devkit==1.1.11
```

### Usage

```bash
python view.py <radar_file.pcd> [--show-points] [--num-points N] [--debug]
```

- Shows PCD file header and radar point shape.
- Use `--show-points` to print the first N points (default N=5, set with `--num-points`).
- Use `--debug` to print the full exception traceback if a file fails to load.

### Examples

```bash
python view.py nuscenes/n008-2018-08-30-15-16-55-0400__RADAR_FRONT__1535657112123599.pcd --show-points --debug
python view.py u5c/carla_log_2026-05-13.log__RADAR_FRONT__8055000.pcd --show-points --debug
```

### References

1. [data_classes.py#L261](https://github.com/nutonomy/nuscenes-devkit/blob/pip_1.1.12/python-sdk/nuscenes/utils/data_classes.py#L261)
