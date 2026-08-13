# Security and Data Handling

## Current development rule

ClaimLens development uses synthetic or deliberately de-identified fixtures. Real patient/PHI data must not be committed to GitHub.

## Data classes

### Public project data
Architecture documents, synthetic cases, non-secret configuration examples, tests, and rule metadata appropriate for source control.

### Sensitive local data
Any real clinical data, credentials, API keys, contract documents, proprietary payer files, or operational exports. These remain outside the repository unless a later approved secure workflow explicitly governs them.

### Generated output
Generated results may contain source-derived information. Production outputs must eventually inherit the sensitivity of their inputs.

## Repository controls

- `.env` and secrets are ignored.
- Local/private/PHI data directories are ignored.
- Generated `output/` contents are ignored except the placeholder.
- Synthetic fixtures must not accidentally contain copied real patient identifiers.

## Future production questions

Before ClaimLens handles production PHI, explicitly design and document:

- Hosting/deployment model.
- Encryption at rest/in transit.
- Authentication and authorization.
- Audit logging.
- Retention/deletion policy.
- Backup/recovery.
- Vendor/model data handling.
- Organization agreements and compliance obligations.
- Incident response.

These are prerequisites for production PHI handling, not tasks to bolt on afterward.
