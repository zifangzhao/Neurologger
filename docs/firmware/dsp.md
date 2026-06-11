# DSP and Closed-loop Control

WILD supports online filtering and stimulation logic for closed-loop experiments.

## DSP Modes

- Disabled.
- Single channel.
- Single channel with Hilbert transform.
- Double channel.
- Double channel with Hilbert transform.
- Cascade filtering.
- Gated detection.
- Random triggering.

## Filters

![Closed-loop filter parameters](../images/WIrelessEphys_Github_3_filterParams.jpg)

Current filter families include delta, theta, alpha, beta, gamma, epsilon, and ripple.

## Referencing

- Direct: `x = A`.
- Differential: `x = A - B`.
- Current source density style: `x = 2A - B - C`.

## Stimulation Parameters

Document pulse width, delay, frequency, train length, random delay, intensity, and channel mapping with the firmware version used for validation.

!!! important
    Closed-loop detection and stimulation should be validated on the bench before in vivo experiments. This page should eventually include reproducible test waveforms and expected trigger timing.
