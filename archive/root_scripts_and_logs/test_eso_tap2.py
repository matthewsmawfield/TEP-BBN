import pyvo as vo
tap_url = "http://archive.eso.org/tap_obs"
tap_service = vo.dal.TAPService(tap_url)
queries = [
    "1558-00",
    "1358+65",
    "0105+16",
    "1937-10"
]
for q in queries:
    print(f"--- Querying {q} ---")
    query = f"SELECT top 10 target_name FROM ivoa.ObsCore WHERE instrument_name LIKE '%UVES%' AND dataproduct_type='spectrum' AND target_name LIKE '%{q}%'"
    try:
        results = tap_service.search(query)
        for row in results:
            print(row['target_name'])
    except Exception as e:
        print(f"Error: {e}")
