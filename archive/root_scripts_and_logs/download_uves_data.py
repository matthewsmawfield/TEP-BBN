"""
Download UVES spectra from ESO archive using astroquery.eso

Note: This downloads UVES (VLT) data, not HIRES (Keck) data.
Cooke et al. (2016) used both instruments for different systems.
"""

import sys
sys.path.insert(0, '/Users/matthewsmawfield/www/Temporal Equivalence Principle/TEP-BBN')

print("=" * 60)
print("Downloading UVES Spectra from ESO Archive")
print("=" * 60)
print()

# Check if astroquery is available
try:
    from astroquery.eso import Eso
    print("✓ astroquery.eso is available")
except ImportError:
    print("✗ astroquery.eso is not available")
    print("Install with: pip install astroquery")
    sys.exit(1)

# Create ESO instance
eso = Eso()

# Query for Q0913+072 (program 68.B-0115)
print("Querying ESO archive for Q0913+072 (program 68.B-0115)...")
try:
    # Query by program ID
    table = eso.query_main(column_filters={'prog_id': '68.B-0115'})
    print(f"✓ Found {len(table)} observations")
    
    if len(table) > 0:
        print(f"Columns: {table.colnames}")
        print(f"First observation: {table[0]}")
        
        # Get dataset IDs
        dataset_ids = table['Dataset ID']
        print(f"Dataset IDs: {dataset_ids[:5]}...")  # Show first 5
        
        # Try to retrieve data
        print()
        print("Attempting to retrieve data...")
        print("Note: This may require ESO authentication for some datasets")
        
        # For public data, we can try without authentication
        # For proprietary data, we would need: eso.login(username, password)
        
        # Try to retrieve first dataset
        if len(dataset_ids) > 0:
            first_dataset = dataset_ids[0]
            print(f"Retrieving dataset: {first_dataset}")
            
            try:
                # This will attempt to download the data
                # Note: This may fail if authentication is required
                eso.retrieve_data([first_dataset])
                print(f"✓ Successfully retrieved {first_dataset}")
            except Exception as e:
                print(f"✗ Retrieval failed: {e}")
                print()
                print("Authentication may be required:")
                print("  eso.login(username, password)")
                print()
                print("Or the data may need to be requested manually from:")
                print("  https://archive.eso.org/wdb/wdb/eso/eso_archive_main/query?prog_id=68.B-0115")
        
except Exception as e:
    print(f"✗ Query failed: {e}")
    print()
    print("Manual access:")
    print("  https://archive.eso.org/wdb/wdb/eso/eso_archive_main/query?prog_id=68.B-0115")

print()
print("=" * 60)
print("ESO Archive Access Summary")
print("=" * 60)
print()
print("ESO has programmatic access via astroquery.eso")
print("Public data can be downloaded without authentication")
print("Proprietary data requires ESO account and authentication")
print()
print("Note: This is UVES (VLT) data, not HIRES (Keck) data")
print("Cooke et al. (2016) used both instruments for different systems")
print("=" * 60)
