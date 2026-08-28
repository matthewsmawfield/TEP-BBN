#!/usr/bin/env python3
"""
TEP-BBN Sightline Ingestion Tool.

Downloads raw FITS files from the ESO archive (or uses existing local files),
coadds them, extracts spectral regions, and writes a union manifest with
full provenance information.

Usage:
    python scripts/ingest_sightline.py --sightline PKS1937-101
    python scripts/ingest_sightline.py --sightline PKS1937-101 --skip-download
    python scripts/ingest_sightline.py --sightline J1332+0052 --use-local data/raw/J1332/
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

SIGHTLINE_REGISTRY = {
    "Q1009+2956": {
        "eso_target": "Q1009+2956",
        "eso_program_id": "095.A-0854(A)",
        "instrument": "UVES",
        "resolving_power": 115000,
        "z_abs": 2.5042,
        "reference": "Zavarygin et al. 2018 (SQUAD DR1)",
    },
    "PKS1937-101": {
        "eso_target": "PKS1937-101",
        "eso_program_id": "0103.A-0837(A)",
        "instrument": "ESPRESSO",
        "resolving_power": 70000,
        "z_abs": 3.572,
        "reference": "Cooke et al. 2024 (arXiv:2402.05586)",
    },
    "J1332+0052": {
        "eso_target": "J1332+0052",
        "eso_program_id": "0103.A-0837(B)",
        "instrument": "UVES",
        "resolving_power": 50800,
        "z_abs": 3.4210863,
        "reference": "Riemer-Sørensen et al. 2024 (arXiv:2401.12797)",
    },
}


def sha256_file(filepath):
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_from_eso(target, program_id, output_dir):
    """
    Download raw FITS files from the ESO archive using eso_archive.py.
    Falls back to a placeholder if the archive script is not available.
    """
    archive_script = project_root / "scripts" / "lib" / "eso_archive.py"
    if archive_script.exists():
        result = subprocess.run(
            [sys.executable, str(archive_script), "--target", target,
             "--program-id", program_id, "--output-dir", str(output_dir)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"  Warning: ESO archive download failed: {result.stderr[-200:]}")
            return []
        # Return list of downloaded files
        fits_files = sorted(output_dir.glob("*.fits"))
        return fits_files
    else:
        print(f"  Warning: eso_archive.py not found. Skipping download.")
        print(f"  Please download {target} raw FITS from:")
        print(f"    http://archive.eso.org/wdb/wdb/eso/eso_archive_main?target={target}")
        print(f"  and place them in: {output_dir}")
        return []


def load_fits_spectrum(filepath):
    """
    Load a 1D spectrum from a FITS file.
    Returns (wave, flux, err) arrays.
    """
    try:
        from astropy.io import fits
        import numpy as np
    except ImportError:
        print("  Error: astropy not installed. Run: pip install astropy")
        sys.exit(1)

    with fits.open(filepath) as hdul:
        data = hdul[1].data  # assuming binary table in extension 1
        wave = np.array(data["WAVE"]).flatten()
        flux = np.array(data["FLUX"]).flatten()
        err = np.array(data["ERR"]).flatten() if "ERR" in data.names else np.zeros_like(flux)

    return wave, flux, err


def coadd_spectra(fits_files, resolving_power):
    """
    Coadd multiple spectra, handling wavelength binning and
    inverse-variance weighting.
    """
    import numpy as np

    if not fits_files:
        return None

    # Load all spectra
    spectra = []
    for f in fits_files:
        w, fl, er = load_fits_spectrum(f)
        spectra.append({"wave": w, "flux": fl, "err": er})

    # Find common wavelength grid (use the highest-resolution one)
    # For simplicity, use the first spectrum's grid
    ref = spectra[0]
    wave_grid = ref["wave"]
    coadd_flux = np.zeros_like(wave_grid)
    coadd_weight = np.zeros_like(wave_grid)

    for spec in spectra:
        # Interpolate onto common grid
        fl_interp = np.interp(wave_grid, spec["wave"], spec["flux"])
        er_interp = np.interp(wave_grid, spec["wave"], spec["err"])
        # Inverse-variance weighting
        mask = er_interp > 0
        coadd_flux[mask] += fl_interp[mask] / er_interp[mask] ** 2
        coadd_weight[mask] += 1.0 / er_interp[mask] ** 2

    coadd_flux = np.where(coadd_weight > 0, coadd_flux / coadd_weight, 0.0)
    coadd_err = np.where(coadd_weight > 0, 1.0 / np.sqrt(coadd_weight), 0.0)

    return wave_grid, coadd_flux, coadd_err


def extract_regions(wave, flux, err, z_abs, vpfit_model_path):
    """
    Extract spectral regions defined in the VPFIT .26 file.
    """
    import numpy as np

    regions = []
    with open(vpfit_model_path) as f:
        for line in f:
            if line.startswith("%%"):
                parts = line.strip().split()
                w_min = float(parts[3])
                w_max = float(parts[4])
                mask = (wave >= w_min) & (wave <= w_max)
                if mask.sum() > 0:
                    regions.append({
                        "wave": wave[mask].tolist(),
                        "flux": flux[mask].tolist(),
                        "err": err[mask].tolist(),
                        "w_min": w_min,
                        "w_max": w_max,
                        "transition": f"region_{len(regions)+1}",
                    })

    return regions


def build_manifest(sightline_id, fits_files, wave, flux, err, regions, z_abs,
                   instrument, resolving_power, reference):
    """Build the union manifest with full provenance."""
    import numpy as np

    # Compute SHA256 for each raw FITS file
    raw_provenance = []
    for f in fits_files:
        sha = sha256_file(f)
        raw_provenance.append({
            "filename": f.name,
            "sha256": sha,
            "size_bytes": f.stat().st_size,
        })

    manifest = {
        "sightline": sightline_id,
        "z_abs": z_abs,
        "instrument": instrument,
        "resolving_power": resolving_power,
        "total_exptime": sum(f.stat().st_size for f in fits_files),  # placeholder
        "source_files": [f.name for f in fits_files],
        "reference": reference,
        "coadds": {
            f"{sightline_id}_{instrument}": regions,
        },
        "n_regions": len(regions),
        "n_pixels": sum(len(r["wave"]) for r in regions),
        "transitions_covered": [r["transition"] for r in regions],
        "provenance": {
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
            "software_versions": {
                "python": sys.version.split()[0],
                "numpy": np.__version__,
            },
            "raw_fits_provenance": raw_provenance,
            "archive": "ESO Archive",
            "archive_url": f"http://archive.eso.org/wdb/wdb/eso/eso_archive_main?target={sightline_id}",
            "pipeline_script": "scripts/ingest_sightline.py",
            "coadd_method": "inverse-variance weighted",
            "normalization_method": "none (continuum normalized in VPFIT)",
            "region_extraction": "from VPFIT .26 file region definitions",
        },
    }

    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="TEP-BBN Sightline Ingestion Tool"
    )
    parser.add_argument(
        "--sightline",
        required=True,
        choices=list(SIGHTLINE_REGISTRY.keys()),
        help="Sightline to ingest",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip ESO archive download, use existing FITS files",
    )
    parser.add_argument(
        "--use-local",
        type=str,
        default=None,
        help="Use local FITS files from this directory",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output manifest path (default: data/processed/<sightline>_union_manifest.json)",
    )
    args = parser.parse_args()

    info = SIGHTLINE_REGISTRY[args.sightline]
    sightline_id = args.sightline

    print(f"\nTEP-BBN Sightline Ingestion: {sightline_id}")
    print(f"  Instrument: {info['instrument']}")
    print(f"  R = {info['resolving_power']}")
    print(f"  z_abs = {info['z_abs']}")
    print(f"  Reference: {info['reference']}")

    # Determine FITS file location
    if args.use_local:
        fits_dir = Path(args.use_local)
    else:
        fits_dir = project_root / "data" / "raw" / sightline_id.replace("+", "_")

    fits_dir.mkdir(parents=True, exist_ok=True)

    # Download or find FITS files
    if args.skip_download or args.use_local:
        fits_files = sorted(fits_dir.glob("*.fits"))
        if not fits_files:
            print(f"\n  Error: No FITS files found in {fits_dir}")
            if not args.skip_download:
                print(f"  Run without --skip-download to download from ESO archive")
            sys.exit(1)
        print(f"\n  Found {len(fits_files)} FITS files in {fits_dir}")
    else:
        print(f"\n  Downloading from ESO archive...")
        fits_files = download_from_eso(info["eso_target"], info["eso_program_id"], fits_dir)
        if not fits_files:
            print(f"  No files downloaded. Use --skip-download with existing files.")
            sys.exit(1)
        print(f"  Downloaded {len(fits_files)} FITS files")

    # Coadd spectra
    print(f"\n  Coadding spectra...")
    result = coadd_spectra(fits_files, info["resolving_power"])
    if result is None:
        print(f"  Error: Coadd failed")
        sys.exit(1)
    wave, flux, err = result
    print(f"  Coadd: {len(wave)} pixels, {wave.min():.1f}-{wave.max():.1f} Å")

    # Find VPFIT model file
    vpfit_model = project_root / f"data/literature_components/{sightline_id}_z{info['z_abs']:.3f}_vpfit_model.26"
    if not vpfit_model.exists():
        # Try alternative naming
        vpfit_model = project_root / "data/literature_components/model_6a.26"
    if not vpfit_model.exists():
        print(f"  Warning: VPFIT model not found, using full wavelength range")

    # Extract regions
    if vpfit_model.exists():
        print(f"\n  Extracting regions from {vpfit_model.name}...")
        regions = extract_regions(wave, flux, err, info["z_abs"], str(vpfit_model))
        print(f"  Extracted {len(regions)} regions, {sum(len(r['wave']) for r in regions)} pixels")
    else:
        # Use full spectrum as a single region
        regions = [{
            "wave": wave.tolist(),
            "flux": flux.tolist(),
            "err": err.tolist(),
            "w_min": float(wave.min()),
            "w_max": float(wave.max()),
            "transition": "full",
        }]

    # Build manifest
    manifest = build_manifest(
        sightline_id, fits_files, wave, flux, err, regions,
        info["z_abs"], info["instrument"], info["resolving_power"],
        info["reference"],
    )

    # Write manifest
    output_path = Path(args.output) if args.output else (
        project_root / f"data/processed/{sightline_id}_union_manifest.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n  Manifest written to: {output_path}")
    print(f"  Provenance: {len(manifest['provenance']['raw_fits_provenance'])} files recorded")
    print(f"\n  ✓ Ingestion complete for {sightline_id}")


if __name__ == "__main__":
    main()
