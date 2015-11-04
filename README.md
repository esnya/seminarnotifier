# SeminarNotifier

Automated notification sender.

## Usage

```
pytohn2 seminarnotifier.py --config=<path to config JSON>
```

Run once per day day with scheduler system (e.g. crontab).

### Optional Arguments

`-c`
:   Short alias for `--config`.

`--log-level|-l`
:   Logging level (e.g. ERROR, INFO, DEBUG).

`--log-file|-f`
:   Path to file to append logs.


## Configuration

See `config.example.json`. Configuration JSON has four sections. 

`defaults`
:   Object of default values when used which is not specified in source.

`source`
:   Get source of data. See `seminarnotifier.source.WebSource.__init__()`

`parser`
:   Parser for parse the soruce data into seminars. See `seminarnotifier.seminarparser.DOMParser.__init__()`

`notifier`
:   Sends the notify of seminar. See `seminarnotifier.notifier.SMTPNotifier.__init__()`


## Bug, Issue, Pull Requests

[GitHub](https://github.com/ukatama/seminarnotifier/issues)


## License

MIT License
