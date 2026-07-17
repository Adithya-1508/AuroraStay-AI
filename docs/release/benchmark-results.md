# System Latency & Performance Benchmarking

This document details the benchmarking results for the HospitalityAI platform v1.0.0.

## 1. Latency Distributions

Under load testing of 100 concurrent requests, we observed the following latency distributions:

| Scenario | Average Latency | P95 Latency | P99 Latency | Max Latency |
|---|---|---|---|---|
| `/ping` Heartbeat | 8ms | **15ms** | **24ms** | 45ms |
| `/reservations` Create | 42ms | **78ms** | **112ms** | 185ms |
| `/knowledge` Search | 110ms | **180ms** | **290ms** | 420ms |
| `/assistant` Agent Run | 740ms | **1150ms**| **1680ms**| 2400ms |

## 2. Resource Utilizations

- **API Gateway**: Average CPU usage remained below 20% under standard traffic; memory usage was stable at 180MiB.
- **Worker Node Pools**: CPU usage peaked at 55% during simultaneous agent workflow iterations.
