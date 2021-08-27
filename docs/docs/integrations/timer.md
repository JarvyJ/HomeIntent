# Timer
A basic timer component for setting, and one day managing timers. 

Home Intent currently does not keep track of state on its own, so if Home Intent restarts, all set timers will be lost.


## Configuration

Add the following to your `config.yaml` to enable the timer:
```yaml
timer:

```

This component has the following options: 

| Option        | Description                                   | Required/Default |
|:--------------|:----------------------------------------------|:-----------------|
| max_time_days | The maximum number of days to set a timer for | 1                |

!!! note "Maximum Number of Days"
    It is currently set to 1 as Home Intent restarts daily. Once auto reloading of configuration is in, we will change the default to 30 days.

## Example Sentences

 * Set timer 90 seconds
 * set timer one and half minutes
 * set timer one hour and thirty minutes

!!! quote "Note"
    We did try allowing "set timer *for* 30 seconds", but found that the "for" would routintely get confused with a "four" and the timer would be set incorrectly. So it's been removed for now.

## Advaned Customization
The timer components can be customized using the [customization json](/getting-started/advanced-features/component-customization/) with the filename `/config/customizations/timer.md`. The alarm sound can be changed by placing a wav file at `/config/timer/alarm.wav`.
