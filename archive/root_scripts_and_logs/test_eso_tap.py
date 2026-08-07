import pyvo as vo
tap_url = "http://archive.eso.org/tap_obs"
tap_service = vo.dal.TAPService(tap_url)
query = "SELECT top 10 target_name, access_url FROM ivoa.ObsCore WHERE instrument_name LIKE '%UVES%' AND dataproduct_type='spectrum' AND target_name LIKE '%1937-100%'"
try:
    results = tap_service.search(query)
    print("Found:")
    for row in results:
        print(row['target_name'])
except Exception as e:
    print(f"Error: {e}")
