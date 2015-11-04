# SeminarNotifier

Automated notification sender.

## Usage

```
pytohn2 seminarnotifier.py --config=<path to config JSON>
```

Run once per day day with scheduler system (e.g. crontab).

### Optional Arguments

`-c<path>`
:   Short alias for `--config`.

`--log-level=<level>` or `-l<level>`
:   Logging level (e.g. ERROR, INFO, DEBUG).

`--log-file=<path>` or `-f<path>`
:   Path of file to output logs.

`--advance=<n>` or `-a<n>`
:   Notify n days in advance.


## Configuration

See `config.example.json` for example.

`defaults`
:   Object of default values when used which is not specified in source.

`source`
:   Get source of data. See `seminarnotifier.source.WebSource.__init__()`

`parser`
:   Parser for parse the soruce data into seminars. See `seminarnotifier.seminarparser.DOMParser.__init__()`

`notifier`
:   Sends the notify of seminar. See `seminarnotifier.notifier.SMTPNotifier.__init__()`


## Bug, Issue, Pull Requests

[https://github.com/ukatama/seminarnotifier/issues](https://github.com/ukatama/seminarnotifier/issues)


## License

MIT License
