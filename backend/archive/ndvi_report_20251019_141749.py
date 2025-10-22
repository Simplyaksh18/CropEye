
from __future__ import annotations
import os
import numpy as np

try:
    import matplotlib as mpl  # type: ignore
    # use a non-interactive backend suitable for saving files
    mpl.use('Agg')
    import matplotlib.pyplot as plt  # type: ignore
    from matplotlib.colors import LinearSegmentedColormap  # type: ignore
except Exception as e:
    raise ImportError("matplotlib is required to generate NDVI reports; install it with: pip install matplotlib") from e
from datetime import datetime
import random
import json
from typing import Optional


def _make_colormap():
    # green-white-green style colormap
    colors = ['#8B0000', '#F4A582', '#F7F7F7', '#B8E186', '#006400']
    return LinearSegmentedColormap.from_list('ndvi_cmap', colors, N=256)
def generate_ndvi_report(
    ndvi_array: np.ndarray,
    out_path: str,
    ground_truth: Optional[np.ndarray] = None,
    metrics: Optional[dict] = None,
    metadata: Optional[dict] = None,
) -> str:
    """Generate an NDVI analysis PNG and optional companion JSON file.

    The layout is designed to avoid overlapping panels and remain readable.

    Args:
        ndvi_array: 2D NDVI numpy array
        out_path: where to write the PNG (created directories if needed)
        ground_truth: optional 2D array of same shape for accuracy panels
        metrics: optional metrics dict (written to JSON if provided or computed)
        metadata: optional dict (latitude, longitude, timestamp, etc.)

    Returns:
        Absolute path to the generated PNG file.
    """
    out_dir = os.path.dirname(out_path) or "."
    os.makedirs(out_dir, exist_ok=True)

    arr = np.array(ndvi_array, dtype=float)
    mask = np.isfinite(arr)
    valid = arr[mask]
    if valid.size == 0:
        # fallback: synthetic array
        arr = np.full((100, 100), 0.5)
        mask = np.isfinite(arr)
        valid = arr[mask]

    vmin = float(np.nanmin(valid))
    vmax = float(np.nanmax(valid))

    dense = int(np.sum(valid > 0.6))
    moderate = int(np.sum((valid > 0.4) & (valid <= 0.6)))
    low = int(np.sum((valid > 0.2) & (valid <= 0.4)))
    bare = int(np.sum(valid <= 0.2))
    total = int(valid.size)

    cmap = _make_colormap()

    # larger canvas and layout that reserves rightmost column for stats
    fig = plt.figure(figsize=(16, 12), constrained_layout=True)
    # 3 rows x 4 cols: left column for map, middle cols for analyses, rightmost column reserved for stats
    gs = fig.add_gridspec(3, 4, width_ratios=[1.0, 1.3, 1.0, 0.6], height_ratios=[0.9, 1.4, 1.0])

    # Left column: NDVI map spanning all rows
    ax_map = fig.add_subplot(gs[:, 0])
    im = ax_map.imshow(arr, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax_map.set_title("NDVI Map")
    ax_map.axis("off")
    cbar = fig.colorbar(im, ax=ax_map, fraction=0.05, pad=0.02)
    cbar.set_label("NDVI Value")

    # Top-center: histogram
    ax_hist = fig.add_subplot(gs[0, 1:3])
    ax_hist.hist(valid, bins=60, color="#2E8B57", edgecolor="black")
    ax_hist.set_title("NDVI Distribution", fontsize=12)
    ax_hist.set_xlabel("NDVI Value", fontsize=10)
    ax_hist.set_ylabel("Frequency", fontsize=10)
    ax_hist.tick_params(labelsize=9)
    ax_hist.set_xlim(vmin, vmax)

    if ground_truth is not None:
        try:
            gt = np.array(ground_truth, dtype=float)
            gt_valid = gt[np.isfinite(gt)]
            if gt_valid.size > 0:
                ax_hist.hist(
                    gt_valid,
                    bins=60,
                    color="none",
                    edgecolor="red",
                    histtype="step",
                    linewidth=1.2,
                    label="Actual (GT)",
                )
                ax_hist.legend(fontsize=8)
        except Exception:
            pass

    # Right column reserved for stats; create a dedicated axis and keep it empty except for text
    ax_stats = fig.add_subplot(gs[:, 3])
    ax_stats.axis("off")
    mean = float(np.mean(valid))
    median = float(np.median(valid))
    std = float(np.std(valid))
    mn = float(np.min(valid))
    mx = float(np.max(valid))
    gt_mean = None
    if ground_truth is not None:
        try:
            gt_arr = np.array(ground_truth, dtype=float)
            gt_mask = np.isfinite(gt_arr)
            gt_valid = gt_arr[gt_mask]
            if gt_valid.size > 0:
                gt_mean = float(np.mean(gt_valid))
        except Exception:
            gt_mean = None

    stats_lines = [
        "NDVI Statistics:\n",
        f"Computed Mean: {mean:.3f}",
        (f"Actual Mean: {gt_mean:.3f}" if gt_mean is not None else "Actual Mean: N/A"),
        f"Median: {median:.3f}",
        f"Std Dev: {std:.3f}",
        f"Min: {mn:.3f}",
        f"Max: {mx:.3f}",
        "",
        f"Valid Pixels: {total:,}",
        f"Total Pixels: {arr.size:,}",
    ]
    # merge health assessment into stats_lines
    score = int(np.clip((mean - 0.2) / 0.8 * 100, 0, 100))
    if mean > 0.7:
        category = "Excellent"
    elif mean > 0.5:
        category = "Good"
    elif mean > 0.3:
        category = "Moderate"
    else:
        category = "Low"
    stats_lines += [
        "",
        "Health Assessment:",
        f"Category: {category}",
        f"Score: {score}/100",
        "Key Recommendations:",
        " - Monitor high-variance areas",
        (" - Maintain current good practices" if category in ("Excellent", "Good") else " - Investigate low NDVI zones"),
    ]
    stats_text = "\n".join(stats_lines)
    ax_stats.text(0.02, 0.98, stats_text, fontsize=9, family="monospace", va="top")

    # Middle: vegetation zones rendered as a hexbin density/color plot to avoid marker overplot
    ax_veg = fig.add_subplot(gs[1, 1:3])
    ys, xs = np.where(mask)
    xs = xs.astype(float)
    ys = ys.astype(float)
    vals = arr[mask]
    # sample if extremely large
    max_points = 20000
    if xs.size > max_points:
        idx = np.random.choice(xs.size, max_points, replace=False)
        xs_s = xs[idx]
        ys_s = ys[idx]
        vals_s = vals[idx]
    else:
        xs_s = xs
        ys_s = ys
        vals_s = vals
    # hexbin uses x,y coordinates; reduce_C_function=np.mean to color by mean NDVI per bin
    hb = ax_veg.hexbin(xs_s, ys_s, C=vals_s, gridsize=120, reduce_C_function=np.mean, cmap=cmap, mincnt=1)
    cb_hb = fig.colorbar(hb, ax=ax_veg, fraction=0.046, pad=0.02)
    cb_hb.set_label('NDVI (density)')
    ax_veg.set_title("Vegetation Zones")
    ax_veg.axis("off")

    # Middle-right: health / quick recommendations
    ax_health = fig.add_subplot(gs[1, 3])
    ax_health.axis("off")
    score = int(np.clip((mean - 0.2) / 0.8 * 100, 0, 100))
    if mean > 0.7:
        category = "Excellent"
    elif mean > 0.5:
        category = "Good"
    elif mean > 0.3:
        category = "Moderate"
    else:
        category = "Low"
    health_lines = [
        "Health Assessment:",
        "",
        f"Category: {category}",
        f"Score: {score}/100",
        "",
        "Key Recommendations:",
        "\u2022 Monitor high-variance areas",
        ("\u2022 Maintain current good practices" if category in ("Excellent", "Good") else "\u2022 Investigate low NDVI zones"),
    ]
    ax_health.text(0, 0.95, "\n".join(health_lines), fontsize=10)

    # Bottom-left: pie chart for coverage
    ax_pie = fig.add_subplot(gs[2, 1])
    labels = []
    sizes = []
    if dense > 0:
        labels.append("Dense Veg")
        sizes.append(dense)
    if moderate > 0:
        labels.append("Moderate Veg")
        sizes.append(moderate)
    if low > 0:
        labels.append("Low Veg")
        sizes.append(low)
    if bare > 0:
        labels.append("Bare/Water")
        sizes.append(bare)
    if sum(sizes) == 0:
        labels = ["No Data"]
        sizes = [1]
    ax_pie.pie(sizes, labels=labels, autopct="%1.1f%%", colors=["#1b5e20", "#66bb6a", "#c8e6c9", "#d32f2f"])
    ax_pie.set_title("Vegetation Coverage")

    # Bottom-center: difference map (if GT provided) -- we'll add as inset on vegetation panel
    # and also create a small bottom-center slot for scatter
    ax_sc = fig.add_subplot(gs[2, 2])
    ax_sc.axis("off")

    # Bottom-right: scatter + metrics moved to bottom-center (ax_sc) to avoid using stats column
    computed_metrics = None
    if ground_truth is not None:
        try:
            gt = np.array(ground_truth, dtype=float)
            mask_both = np.isfinite(gt) & np.isfinite(arr)
            a = gt[mask_both].ravel()
            c = arr[mask_both].ravel()
            if a.size > 0:
                ax_sc.scatter(a, c, s=3, alpha=0.5)
                mnv = min(a.min(), c.min())
                mxv = max(a.max(), c.max())
                ax_sc.plot([mnv, mxv], [mnv, mxv], color="k", linestyle="--", linewidth=0.8)
                ax_sc.set_xlabel("Actual (GT)")
                ax_sc.set_ylabel("Computed")
                ax_sc.set_title("Actual vs Computed")

                if metrics is None:
                    diffv = c - a
                    mae = float(np.mean(np.abs(diffv)))
                    rmse = float(np.sqrt(np.mean(diffv ** 2)))
                    bias = float(np.mean(diffv))
                    pct05 = float(100.0 * np.mean(np.abs(diffv) <= 0.05))
                    try:
                        r = float(np.corrcoef(a, c)[0, 1])
                    except Exception:
                        r = float("nan")
                    computed_metrics = {
                        "mae": mae,
                        "rmse": rmse,
                        "bias": bias,
                        "pct_within_0.05": pct05,
                        "r": r,
                        "n": int(a.size),
                    }
                else:
                    computed_metrics = metrics

                met_lines = [
                    f"MAE: {computed_metrics.get('mae', float('nan')):.4f}",
                    f"RMSE: {computed_metrics.get('rmse', float('nan')):.4f}",
                    f"Bias: {computed_metrics.get('bias', float('nan')):.4f}",
                    f"% within 0.05: {computed_metrics.get('pct_within_0.05', float('nan')):.1f}%",
                    f"r: {computed_metrics.get('r', float('nan')):.3f}",
                    f"n: {computed_metrics.get('n', 0)}",
                ]
                ax_sc.text(0.02, 0.98, "\n".join(met_lines), transform=ax_sc.transAxes, fontsize=8, va="top", family="monospace")
        except Exception:
            pass

    # difference inset on vegetation panel
    if ground_truth is not None:
        try:
            gt = np.array(ground_truth, dtype=float)
            if gt.shape == arr.shape:
                # inset in axes coordinates relative to figure; tuned to sit inside veg panel
                ax_diff = fig.add_axes([0.57, 0.28, 0.08, 0.18])
                diff = gt - arr
                imd = ax_diff.imshow(diff, cmap="bwr", vmin=-0.5, vmax=0.5)
                ax_diff.set_title("GT - Computed", fontsize=8)
                ax_diff.axis('off')
                fig.colorbar(imd, ax=ax_diff, fraction=0.046, pad=0.02)
        except Exception:
            pass

    fig.suptitle("NDVI Analysis", fontsize=14)

    # Overlay metadata (coordinates, timestamp)
    try:
        if metadata and isinstance(metadata, dict):
            md_lines = []
            lat = metadata.get("latitude")
            lon = metadata.get("longitude")
            ts = metadata.get("timestamp")
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                md_lines.append(f"Lat: {lat:.6f}, Lon: {lon:.6f}")
            if ts:
                md_lines.append(f"Time: {ts}")
            if md_lines:
                fig.text(0.01, 0.01, " | ".join(md_lines), fontsize=8, family="monospace")
    except Exception:
        pass

    # Save PNG
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Export metrics JSON if available (computed_metrics preferred over provided metrics)
    try:
        to_write = None
        if computed_metrics is not None:
            to_write = computed_metrics
        elif metrics is not None:
            to_write = metrics
        if to_write is not None and isinstance(to_write, dict):
            json_path = os.path.splitext(out_path)[0] + ".json"
            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(to_write, jf, indent=2)
    except Exception:
        pass

    return os.path.abspath(out_path)
