The script:
  - Fetches all issues with label `Repo Mapping Update`
  - Validates prefix + cutoff date
  - Creates missing child issues based on config
  - Links each child to its parent
  - Updates `processed.json` to avoid duplicates

## Requirements
- Token with `api` scope (project support repo) 

