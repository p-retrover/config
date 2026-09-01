# Cron and `crontab`

Go back to the [main readme](./README.md)

Cron jobs are scheduled tasks that run automatically according to a time-based schedule.

## View your cron jobs

```bash
crontab -l
```

The notes describe this as listing the cron jobs defined for the current user.

## Edit your cron jobs

```bash
crontab -e
```

This opens the user's crontab in an editor so entries can be added or changed.

The notes mention that `crontab -e` normally opens the default editor, and that the editor can be changed through the environment/configuration.

## Cron syntax

A standard user crontab entry has five time fields followed by the command:

```text
* * * * * <command>
│ │ │ │ │
│ │ │ │ └── day of week
│ │ │ └──── month
│ │ └────── day of month
│ └──────── hour
└────────── minute
```

Example:

```cron
0 8 * * * /path/to/script.sh
```

runs the command at 08:00 every day.

## Cron resources

The handwritten notes recommend **crontab.guru** for generating and checking cron expressions.

