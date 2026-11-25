# Logging convention

Shared logging rules for every app in the hothsys org. Each repo keeps its own
`docs/logging.md` with the per-repo details (file name, how to read the log, and
any app-specific settings). This file is the convention those docs follow.

Agreed in [hothsys/.github#22](https://github.com/hothsys/.github/issues/22).

## Where logs live

Logs go in the operating system standard location, never in the project folder
or the app folder:

- macOS: `~/Library/Logs/<AppName>/app.log` (visible in Console.app)
- Other Unix: `$XDG_STATE_HOME/<AppName>/app.log`, or
  `~/.local/state/<AppName>/app.log` when `XDG_STATE_HOME` is unset

Windows paths are deferred until delta's Windows setup is checked (see #22).

## Line format

One line per entry: timestamp, level, module or area, message, then structured
fields.

```text
2026-11-24 12:00:00 INFO scan: finished path="/photos" files=120 ms=340
```

Errors carry their stack trace on the indented lines after the entry.

## Levels

Levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`. The default is `INFO` everywhere.
The console shows `INFO` and above; the file also gets `DEBUG`.

The level is set per app, plus an `<APP>_LOG_LEVEL` environment variable that
overrides the setting. Examples: `LOG_LEVEL` in fotonervic's `app.conf`, and
`DELTA_LOG_LEVEL` in delta (which also accepts a command line flag and a saved
setting).

## Rotation

Rotate as the log is written, when the file would pass 5 MB, keeping 3 backups
(20 MB at most). Do not rotate only at startup: a server that stays up for days
must still rotate while it runs.

## What is never logged

File contents, edited text, PII values, query values, or user text. Paths,
sizes, counts, and timings are fine.

Request paths are fine to log. The query string, and any user text in it, is not.

## Reading logs

Every app keeps a `logs` command that follows the log file. When the file moves,
the command is updated to point at the new location, so the user-facing command
stays the same.

## Where each repo stands today

| Repo | Status |
| --- | --- |
| fotonervic | Conforms. This is the model: OS-standard location, 5 MB rotation keeping 3 backups, `LOG_LEVEL` in `app.conf` with `INFO` as the default, console `INFO`, file `DEBUG`. |
| delta | Conforms. OS-standard location, 5 MB rotation keeping 3 backups, structured one-line entries, level from a setting, `DELTA_LOG_LEVEL`, or a command line flag. |
| sweepr | Outlier. `sweepr.log` sits in the project folder, rotates at 10 MB keeping 3 backups, and always logs at `DEBUG` with no level setting. |
| docucloak | Outlier. `server.log` sits in the app folder, rotates at 5 MB keeping 3 backups, and always logs at `DEBUG` with no level setting. |
| frayme | Outlier. `.frayme.log` sits in the app folder and is never rotated. |
| matrix | Outlier. `matrix-requests.log` sits in the app folder with a hand-rolled rotation that only runs at startup, and there are no log levels (everything is `INFO`). |

## Follow-up

One small PR per repo, starting with the outliers, each adding `docs/logging.md`
and moving the log file with the `logs` command updated. Tracked in #22.
