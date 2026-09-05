# 02 — Tenant-Safe Event Service

Build the deterministic service around the model: validate the request, derive
scope from trusted context, preserve a source version, and reject a stale write.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Challenge

Implement the three TODOs in `starter.py`. An event ID is not authorization.
The final write must compare the version that was read with the current version.

## Extension

Add a typed error response for `not_found`, `not_authorized`, and
`version_conflict`. Test that no event data appears in the authorization error.
