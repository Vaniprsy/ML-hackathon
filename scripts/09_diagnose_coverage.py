import sys

import numpy as np
import shapely
from shapely import STRtree

from pathsnap import config
from pathsnap.preprocess.io import load_trip
from pathsnap.preprocess.geo import make_projector, project


def diagnose(trip_id):
    trip_name = f"{trip_id:08d}"
    trip = load_trip(trip_id=trip_name, partition="train", with_route=False)
    trip_dir = config.DATA_DIR / trip.partition / trip.trip_id
    missing = [
        trip_dir / f"{trip_name}.{suffix}"
        for suffix, rows in (
            ("track", trip.track),
            ("nodes", trip.nodes),
            ("arcs", trip.arcs),
        )
        if len(rows) == 0
    ]
    if missing:
        for path in missing:
            print(f"Trip {trip_name}: missing or empty input {path}", file=sys.stderr)
        return False

    lon = trip.track[:, 0]
    lat = trip.track[:, 1]

    transformer = make_projector(lon, lat)
    obs_xy = project(transformer, lon, lat)
    nodes_xy = project(
        transformer, trip.nodes[:, 0], trip.nodes[:, 1]
    )

    starts = nodes_xy[trip.arcs[:, 0]]
    ends = nodes_xy[trip.arcs[:, 1]]

    lines = shapely.linestrings(
        np.stack([starts, ends], axis=1)
    )

    tree = STRtree(lines)
    points = shapely.points(obs_xy)

    nearest_idx = tree.nearest(points)
    nearest_dist = shapely.distance(
        points, lines[nearest_idx]
    )

    print(f"\nTRIP {trip_id}")
    print("Observations:", len(points))
    print("Median distance:", round(np.median(nearest_dist), 2), "m")
    print("95th percentile:", round(np.percentile(nearest_dist, 95), 2), "m")
    print("Maximum distance:", round(np.max(nearest_dist), 2), "m")

    for radius in [25, 50, 75, 100, 150, 200]:
        coverage = np.mean(nearest_dist <= radius) * 100
        print(f"Coverage at {radius} m: {coverage:.2f}%")
    return True


if __name__ == "__main__":
    results = [diagnose(trip_id) for trip_id in (54, 33, 2)]
    sys.exit(0 if all(results) else 1)
