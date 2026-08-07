#!/usr/bin/env python3
"""
Generate PDF from TEP Site
==========================

Generates a high-quality PDF from the built TEP site static HTML.
Uses the html_to_pdf.py converter with optimized settings for academic manuscripts.

Usage:
    python scripts/generate_site_pdf.py
    python scripts/generate_site_pdf.py --quality high --wait-time 5
"""

import argparse
import asyncio
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent / "utils"))

from html_to_pdf import HTMLToPDFConverter, create_preset_configs

try:
    import yaml
except ImportError:
    yaml = None


def load_citation_metadata():
    """Load version, codename and paper code from VERSION.json and CITATION.cff."""
    base_dir = Path(__file__).parent.parent
    version_file = base_dir / "VERSION.json"
    citation_file = base_dir / "CITATION.cff"

    # Default fallback
    metadata = {
        "version": "v0.1",
        "codename": "Dubai",
        "paper_code": "TEP-BBN",
        "paper_num": "29",
    }

    # Try VERSION.json first for paper code and number
    if version_file.exists():
        try:
            import json

            with open(version_file, "r") as f:
                vdata = json.load(f)
            desc = vdata.get("description", "")
            # Extract paper number: "Paper 27: ..."
            num_match = re.search(r"Paper\s+(\d+)", desc)
            if num_match:
                metadata["paper_num"] = num_match.group(1)
            metadata["codename"] = vdata.get("codename", metadata["codename"])
            metadata["version"] = vdata.get("version", metadata["version"]).lstrip("v")
            # Extract code from description or infer from title
            if "TEP-BBN" in desc:
                metadata["paper_code"] = "TEP-BBN"
            elif "TEP-HC" in desc:
                metadata["paper_code"] = "TEP-HC"
            elif "TEP-C0" in desc:
                metadata["paper_code"] = "TEP-C0"
            elif "TEP-BBN" in desc:
                metadata["paper_code"] = "TEP-BBN"
            else:
                # Fallback: extract from title in CITATION.cff
                pass
        except Exception as e:
            print(f"⚠️  Error parsing VERSION.json: {e}")

    # Try CITATION.cff for version/codename if VERSION.json didn't provide them
    if citation_file.exists():
        try:
            if yaml:
                with open(citation_file, "r") as f:
                    data = yaml.safe_load(f)
                version_str = data.get("version", "v0.1")
                title = data.get("title", "")
                # Infer paper code from title if not already set
                if metadata["paper_code"] == "TEP-BBN":
                    if "Dubai" in title or "Deuterium" in title:
                        metadata["paper_code"] = "TEP-BBN"
                        metadata["paper_num"] = "29"
            else:
                with open(citation_file, "r") as f:
                    content = f.read()
                version_match = re.search(r'version:\s*"?([^"\n]+)"?', content)
                version_str = (
                    version_match.group(1).strip() if version_match else "v0.1"
                )

            # Parse version string like 'v0.2 (Thika)'
            pattern = r"^(v?[\d.]+)(?:\s*\(([^)]+)\))?$"
            match = re.match(pattern, version_str.strip())
            if match:
                metadata["version"] = match.group(1).lstrip("v")
                metadata["codename"] = match.group(2) or metadata["codename"]
        except Exception as e:
            print(f"⚠️  Error parsing CITATION.cff: {e}")

    return metadata


def build_static_site():
    """Build the static site first."""
    print("🔨 Building static site...")
    site_dir = Path(__file__).parent.parent / "site"
    build_script = site_dir / "build.js"

    if not build_script.exists():
        print("❌ Build script not found:", build_script)
        return False

    try:
        result = subprocess.run(
            ["node", str(build_script)],
            cwd=site_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Site build failed:")
        print(e.stderr)
        return False


def copy_pdf_to_docs(source_pdf: Path, docs_dir: Path):
    """Copy PDF to the docs directory with proper naming."""
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Load metadata
    metadata = load_citation_metadata()
    version_str = f"v{metadata['version']}-{metadata['codename']}"
    paper_num = metadata.get("paper_num", "29")
    paper_code = metadata.get("paper_code", "TEP-BBN")

    # Primary PDF name (using new naming convention)
    target_name = f"{paper_num}-{paper_code}-{version_str}.pdf"
    target_path = docs_dir / target_name

    # Copy the file
    shutil.copy2(source_pdf, target_path)

    print(f"📄 Copied to: {target_path}")
    print(f"   Size: {target_path.stat().st_size / (1024*1024):.2f} MB")

    return target_path


def copy_pdf_to_root(source_pdf: Path, base_dir: Path):
    """Copy PDF to the project root directory."""
    # Load metadata
    metadata = load_citation_metadata()
    version_str = f"v{metadata['version']}-{metadata['codename']}"
    paper_num = metadata.get("paper_num", "29")
    paper_code = metadata.get("paper_code", "TEP-BBN")

    # Primary PDF name (using new naming convention)
    target_name = f"{paper_num}-{paper_code}-{version_str}.pdf"
    target_path = base_dir / target_name

    # Copy the file
    shutil.copy2(source_pdf, target_path)

    print(f"📄 Copied to root: {target_path}")
    print(f"   Size: {target_path.stat().st_size / (1024*1024):.2f} MB")

    return target_path


def process_pdf_with_metadata(pdf_path: Path):
    """Run the PDF processing script to add metadata and compress."""
    process_script = Path(__file__).parent / "utils" / "process_pdf.py"

    if not process_script.exists():
        print("⚠️  PDF processing script not found, skipping metadata embedding")
        return

    print("🔧 Processing PDF with metadata...")
    try:
        subprocess.run(
            [sys.executable, str(process_script), str(pdf_path), "--quality", "ebook"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"⚠️  PDF processing failed: {e}")


async def generate_pdf(
    quality: str = "high",
    wait_time: float = 5.0,
    skip_build: bool = False,
    scale: float = None,
):
    """Generate PDF from the TEP site."""

    # Build site first unless skipped
    if not skip_build:
        if not build_static_site():
            print("❌ Cannot generate PDF - site build failed")
            return False

    # Paths
    base_dir = Path(__file__).parent.parent
    dist_dir = base_dir / "site" / "dist"
    docs_dir = base_dir / "site" / "public" / "docs"

    if not dist_dir.exists():
        print(f"❌ Dist directory not found: {dist_dir}")
        print("   Run site build first: node site/build.js")
        return False

    html_file = dist_dir / "index.html"
    if not html_file.exists():
        print(f"❌ HTML file not found: {html_file}")
        return False

    # Create PDF-specific HTML with synchronous MathJax loading
    pdf_html_file = dist_dir / "index_pdf.html"
    html_content = html_file.read_text(encoding="utf8")
    html_content = html_content.replace(
        'id="MathJax-script" async', 'id="MathJax-script"'
    )
    pdf_html_file.write_text(html_content, encoding="utf8")
    html_file = pdf_html_file

    # Output path (temp, will be copied to docs)
    output_pdf = dist_dir / "manuscript.pdf"

    # Select preset based on quality
    # Note: scale controls content zoom (affects page count)
    # device_scale_factor controls pixel density (affects image/text sharpness)
    presets = create_preset_configs()
    if quality == "maximum":
        # Highest resolution for archival/print quality
        options = presets["high_quality"].copy()
        options["scale"] = 0.72  # Larger content, target <20 pages
        # High pixel density for sharpness
        options["device_scale_factor"] = 3.0
        options["viewport"] = {"width": 1920, "height": 1080}
        options["prefer_css_page_size"] = True
    elif quality == "high":
        options = presets["high_quality"].copy()
        options["scale"] = 0.72
        options["device_scale_factor"] = 2.5
        options["viewport"] = {"width": 1920, "height": 1080}
        options["prefer_css_page_size"] = True
    elif quality == "print":
        options = presets["print_ready"].copy()
        options["scale"] = 0.72
        options["device_scale_factor"] = 2.0
    else:
        options = presets["web_optimized"].copy()

    # Override scale if explicitly provided
    if scale is not None:
        options["scale"] = scale

    options["wait_time"] = wait_time
    options["format"] = "A4"
    options["margin_top"] = "1.2cm"
    options["margin_bottom"] = "1.5cm"  # Increased for footer
    options["margin_left"] = "1cm"
    options["margin_right"] = "1cm"

    # Add page numbers footer
    options["display_header_footer"] = True
    options["header_template"] = "<div></div>"  # Empty header
    options[
        "footer_template"
    ] = """
        <div style="font-size:9px; text-align:center; width:100%; color:#555555; font-family:system-ui,-apple-system,sans-serif; padding-bottom:5mm;">
            Page <span class="pageNumber"></span> of <span class="totalPages"></span>
        </div>
    """

    print(f"\n📄 Generating PDF from: {html_file}")
    print(f"   Quality: {quality}")
    print(f"   Wait time: {wait_time}s (for MathJax rendering)")

    async with HTMLToPDFConverter() as converter:
        success = await converter.convert_file(str(html_file), str(output_pdf), options)

        if not success:
            print("❌ PDF generation failed")
            return False

        print(f"✅ PDF generated: {output_pdf}")
        print(f"   Size: {output_pdf.stat().st_size / (1024*1024):.2f} MB")

        # Load metadata for display
        metadata = load_citation_metadata()
        version_str = f"v{metadata['version']}-{metadata['codename']}"
        print(f"   Version: {version_str}")

        # Copy to docs directory
        docs_pdf = copy_pdf_to_docs(output_pdf, docs_dir)

        # Process docs PDF with metadata (compresses in place)
        process_pdf_with_metadata(docs_pdf)

        # Copy compressed PDF to root directory
        copy_pdf_to_root(docs_pdf, base_dir)

        print("\n✅ Complete! PDF available at:")
        print(f"   {docs_pdf}")

        return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate PDF from TEP site",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with default settings
  python scripts/generate_site_pdf.py
  
  # Maximum quality (highest resolution)
  python scripts/generate_site_pdf.py --quality maximum --wait-time 10
  
  # High quality with longer wait for MathJax
  python scripts/generate_site_pdf.py --quality high --wait-time 10
  
  # Skip site build (use existing dist/)
  python scripts/generate_site_pdf.py --skip-build
        """,
    )

    parser.add_argument(
        "--quality",
        choices=["maximum", "high", "print", "web"],
        default="high",
        help="PDF quality preset (default: high, maximum for highest resolution)",
    )
    parser.add_argument(
        "--wait-time",
        type=float,
        default=5.0,
        help="Seconds to wait for dynamic content (MathJax) to render",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=None,
        help="Override PDF scale factor (default: 0.72, lower = more content per page)",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip site build and use existing dist/ directory",
    )

    args = parser.parse_args()

    try:
        success = asyncio.run(
            generate_pdf(
                quality=args.quality,
                wait_time=args.wait_time,
                skip_build=args.skip_build,
                scale=args.scale,
            )
        )
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
