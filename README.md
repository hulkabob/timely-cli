---
# Timely CLI

A tool for lowering the burden of Timely App time tracking. Very alpha. Hai mucho room for improvement.

---

![Doodle Time](docs/timely-doodle.png)

At teh time of writing, Timely has no support for any interface other than Memory or the Webapp.
And the fact they made UI so painful is to force people into installing Memory. Mmmm, the sweet scent of telemetry.

_Anyway, if you're here, you already know that yourself._

---

## Auththentication/Authorization
You'll need Memory plugin for Chrome. Install it, login, snoop the Bearer token from one of the API requests with developer tools.

Yes, it is a pain, but that's the only feasible way I've managed to get this piece of software to cooperate.

Token Lifetime: TBA, still counting.

## Usage
```
usage: timely [-h] [--note NOTE] [--duration DURATION] [--day DAY] [--iso-from ISO_FROM] [--iso-to ISO_TO] [--time-from TIME_FROM]
              [--time-to TIME_TO] [--plain] [--json]
              {me,log,fix,cover,tags,projects,ping,show}

Timely CLI

positional arguments:
  {me,log,fix,cover,tags,projects,ping,show}

options:
  -h, --help            show this help message and exit
  --note NOTE           Log note
  --duration DURATION   Duration in h(ours) or m(minutes)
  --day DAY             Day in ISO format (2024-12-31)
  --iso-from ISO_FROM   Day in ISO format, from which show hours
  --iso-to ISO_TO       Day in ISO format, to which show hours
  --time-from TIME_FROM
                        Starting time of record, 24h format (9:30, 15:45, 16:20)
  --time-to TIME_TO     Ending time of record, 24h format
  --plain               Dump the goods to STDOUT, no curses
  --json                JSON output
```

## Examples

Show data about current user (dumps JSON from timely)
```bash
./timely me
```

Show filled-in days (placeholder data temporarily)
```bash
./timely show --iso-from 2025-02-10 --iso-to 2025-02-20
```

Add a memory of you working for one hour on some specific task:
```bash
./timely log --day 2025-02-20 --note "Doing some very specific task" --time-from 10:00 --duration 1h
```


## Configs


~/.timely/bearer
```yaml
Bearer fHtw0BX4n4jlqV3WrBvvPX_IsN5f82J4VhRARqoYPO1
```


~/.timely/config
```yaml
org:
  id: 7654321
  name: MicroManagementCorp
user:
  email: spongebob.squarepants@kk.bb
  id: 1231231 
  weeklyCapacity: 40 # Hours
prefs:
  tags: # These tags can be retrieved via `timely tags` coommand
   - 1234567 
   - 1234568
  staringHour: 10 # Your preference, if not set defaults to 10:00 in your local TZ
  projectId: 7657650 # Same as with tags
```

## Necessary configs

0. Bearer. Without it this tool is useless. 
1. Labels/tags. Made preview of them, no picking mechanism.
2. ProjectId. Projects have a tree-like structure, so traversal is tricky.
3. (Optional) Starting hour, for defaults

## Planned functionality

* Viewing hours
* Adding hours
* Adding hours, but with precision (set the bloody time)
* Init with inquiries
* Editing hours
* Covering/Pruning hours
* TUI (for giggles)


## Disclaimers

This tool is provided AS IS. Double-check correct input via browser.
I'm not responsible for anybody not doing due diligence in testing their automations in a controlled way.
And no, if you've created over9000 records for the same day, 8 hours each - you're the one cleaning it.
Hopefully also in an automated way, check the ""Planned Functionality" -> "Covering hours".
