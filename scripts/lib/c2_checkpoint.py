"""Validate C2 partial draws before reusing them after interruption."""
import json
import math


def validate_record(row, expected_seeds):
    seed = row.get('seed')
    if type(seed) is not int or seed not in expected_seeds:
        raise ValueError('Unexpected simulation seed')
    if not all(math.isfinite(row[k]) for k in ['T', 'LL_D', 'LL_H']):
        raise ValueError('Nonfinite simulation likelihood')
    expected = 2 * (row['LL_H'] - row['LL_D'])
    if not math.isclose(row['T'], expected, rel_tol=1e-10, abs_tol=1e-8):
        raise ValueError('Simulation statistic disagrees with its likelihoods')
    for key in ['converged_D', 'converged_H']:
        if type(row.get(key)) is not bool:
            raise ValueError('Missing optimizer status')
    for key in ['params_D', 'params_H']:
        if not row.get(key) or not all(math.isfinite(v) for v in row[key]):
            raise ValueError('Invalid fitted parameters')


def prepare_checkpoint(path, provenance, resume=False, legacy_verified=False):
    metadata = path.with_suffix('.provenance.json')
    expected = set(range(provenance['seed_base'], provenance['seed_base'] + provenance['n_sims']))
    if path.exists() and not resume:
        raise FileExistsError('Partial ledger exists: validate it with --resume; it will not be overwritten')
    rows = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    seeds = set()
    for row in rows:
        validate_record(row, expected)
        if row['seed'] in seeds:
            raise ValueError('Duplicate saved simulation seed')
        seeds.add(row['seed'])
    if metadata.exists():
        old = json.loads(metadata.read_text())
        if old['provenance'] != provenance:
            raise ValueError('Checkpoint inputs or simulation kernel changed')
    elif rows and not legacy_verified:
        raise ValueError('Legacy partial ledger requires a matching archived simulation kernel')
    else:
        metadata.write_text(json.dumps({'provenance': provenance,
            'legacy_adoption': bool(rows),
            'legacy_scope': 'Archived kernel matched; input hashes recorded at recovery, not retroactively certified'}, indent=2) + '\n')
    return rows
