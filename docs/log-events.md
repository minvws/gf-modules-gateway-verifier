# Log events

<!-- markdownlint-disable MD013 -->

Generated from `app.logging.events:Log` by `gfmodules.logging.event_overview`.
Do not edit by hand.

Each stream lists the events that reach it and the fields they carry there besides the context fields.
*any* means the event has no allow-list, so every field it is logged with reaches the stream.
*none* means the event carries only the context fields there.

## Context fields

Every event carries these on every stream, whenever the request context holds a value for them.

- `request_id`
- `ip`
- `user_agent`
- `client_trace_id`
- `correlation_id`
- `endpoint`
- `method`
- `scope`

## Stream `app`

| Event | Id | Level | Fields |
| --- | --- | --- | --- |
| `JWT_VERIFICATION_FAILED` | 200400 | WARNING | `error_reason`, `token_present` |
| `MALFORMED_AUTHORIZATION_HEADER` | 200409 | WARNING | `error_reason`, `token_present` |
| `ORGANIZATION_AUTHORIZATION_MISMATCH` | 200407 | WARNING | `certificate_organization_identifier`, `resource_organization_identifier`, `resource_id`, `client_id` |
| `MISSING_ORGANIZATION_CLAIM` | 200408 | WARNING | `certificate_organization_identifier`, `client_id` |
| `MISSING_ACT_CLAIM` | 200410 | WARNING | `certificate_organization_identifier`, `client_id` |
| `COMMON_NAME_AUTHORIZATION_MISMATCH` | 200411 | WARNING | `certificate_organization_identifier`, `client_id` |
| `AUTHENTICATION_SUCCESS` | 200403 | INFO | `certificate_organization_identifier`, `represented_organization_identifier` |
| `MISSING_AUTHORIZATION_HEADER` | 200404 | WARNING | `token_present`, `client_id`, `certificate_organization_identifier` |
| `SYS_APP_STARTED` | 200601 | INFO | `version`, `config_path` |
| `SYS_APP_STOPPED` | 200602 | INFO | `shutdown_reason`, `last_exception_type` |
| `SYS_APP_CRASHED` | 200602 | CRITICAL | `shutdown_reason`, `last_exception_type` |
| `SYS_UNHANDLED_EXCEPTION` | 200604 | ERROR | `exception_type`, `endpoint`, `method` |
| `SYS_MISSING_CORRELATION_ID` | 200606 | ERROR | `endpoint`, `method` |
| `ACCESS_REQUEST` | 100 | INFO | `endpoint`, `method`, `status_code`, `status_code_missing`, `duration_ms`, `body`, `body_truncated` |

## Stream `siem`

| Event | Id | Level | Fields |
| --- | --- | --- | --- |
| `JWT_VERIFICATION_FAILED` | 200400 | WARNING | `error_reason`, `token_present` |
| `MALFORMED_AUTHORIZATION_HEADER` | 200409 | WARNING | `error_reason`, `token_present` |
| `ORGANIZATION_AUTHORIZATION_MISMATCH` | 200407 | WARNING | `certificate_organization_identifier`, `resource_organization_identifier`, `client_id` |
| `MISSING_ORGANIZATION_CLAIM` | 200408 | WARNING | `certificate_organization_identifier`, `client_id` |
| `MISSING_ACT_CLAIM` | 200410 | WARNING | `certificate_organization_identifier`, `client_id` |
| `COMMON_NAME_AUTHORIZATION_MISMATCH` | 200411 | WARNING | `certificate_organization_identifier`, `client_id` |
| `AUTHENTICATION_SUCCESS` | 200403 | INFO | `certificate_organization_identifier`, `represented_organization_identifier` |
| `MISSING_AUTHORIZATION_HEADER` | 200404 | WARNING | `client_id`, `certificate_organization_identifier` |
| `SYS_APP_STOPPED` | 200602 | INFO | `shutdown_reason` |
| `SYS_APP_CRASHED` | 200602 | CRITICAL | `shutdown_reason` |
| `SYS_UNHANDLED_EXCEPTION` | 200604 | ERROR | `exception_type`, `endpoint`, `method` |
