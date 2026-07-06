LOOP 12 — Hotel Operations Platform

Version: 1.0

Project: HospitalityAI

Status: Mandatory

Prerequisites

Loop 00 – Constitution
Loop 01 – Product Requirements
Loop 02 – Architecture
Loop 03 – Domain Modeling
Loop 04 – Repository Bootstrap
Loop 05 – Backend Core Platform
Loop 06 – Data Platform
Loop 07 – AI Platform
Loop 08 – Multi-Agent Platform
Loop 09 – Knowledge Platform
Loop 10 – Reservation Platform
Loop 11 – Guest Experience Platform
Purpose

Build HospitalityAI's Hotel Operations Platform.

This platform manages everything that happens behind the scenes after a guest interacts with the hotel.

The goal is to automate and optimize hotel operations using AI-powered workflows.

This loop introduces operational intelligence for staff, not guests.

Philosophy

Every guest action should trigger operational workflows.

For example:

Guest checks out

↓

Reservation Platform

↓

Room becomes dirty

↓

Housekeeping Task Created

↓

AI Prioritizes Cleaning

↓

Staff Assigned

↓

Room Ready

↓

Reservation Platform Updated

Every workflow should be event-driven.

Objectives

Develop an Operations Platform capable of:

Housekeeping Management
Maintenance Management
Staff Task Assignment
Room Status Tracking
Operational Workflows
AI Task Prioritization
SLA Monitoring
Operational Notifications
Workforce Optimization
Operational Analytics
Deliverables

Create

business/

operations/

├── domain/
├── application/
├── infrastructure/
├── api/
├── services/
├── workflows/
├── agents/
├── housekeeping/
├── maintenance/
├── tasks/
├── scheduling/
├── notifications/
├── sla/
├── analytics/
├── events/
└── tests/
Domain Models

Implement

HousekeepingTask

MaintenanceTask

StaffMember

Shift

TaskAssignment

RoomStatus

CleaningChecklist

MaintenanceRequest

WorkOrder

OperationalAlert

SLA

OperationalMetric

Equipment

Inspection
Room Lifecycle

Support

Available

↓

Reserved

↓

Occupied

↓

Checkout

↓

Dirty

↓

Cleaning

↓

Inspection

↓

Available

The room state machine must be enforced.

Invalid transitions are rejected.

Housekeeping Platform

Implement

Task creation

Task assignment

Task completion

Priority calculation

Cleaning checklist

Room inspection

Task history

Every checkout should automatically create a housekeeping task.

Maintenance Platform

Support

Equipment issues

Room issues

Preventive maintenance

Emergency maintenance

Work order management

Task escalation

Asset tracking

Maintenance history

Operational Scheduler

Develop an AI-powered scheduling engine.

Responsibilities

Assign staff

Balance workload

Optimize routes

Prioritize urgent work

Reduce idle time

Support manual overrides.

AI Operations Agent

Create Operations Agent.

Responsibilities

Prioritize tasks

Assign staff

Recommend optimizations

Detect bottlenecks

Predict delays

Generate daily operational summaries

This agent must use:

AI Platform
Multi-Agent Platform
Knowledge Platform
Operations Services
Workflow Engine

Implement workflows

Guest Checkout

↓

Create Cleaning Task

↓

Assign Staff

↓

Complete Cleaning

↓

Inspect Room

↓

Room Available

Another workflow

Maintenance Request

↓

Priority Classification

↓

Assign Technician

↓

Repair

↓

Inspection

↓

Close Work Order

Use LangGraph.

Task Prioritization

Prioritize based on

VIP guests

Upcoming reservations

Task urgency

Room category

Maintenance severity

Staff availability

SLA deadlines

SLA Management

Track

Task creation time

Assignment time

Completion time

Inspection time

Escalation

Breaches

Generate alerts automatically.

Notifications

Support

Staff notifications

Task reminders

Escalation alerts

Inspection reminders

Operational incidents

Internal only.

APIs

Create

GET /operations/tasks

POST /operations/tasks

PUT /operations/tasks/{id}

GET /operations/housekeeping

GET /operations/maintenance

POST /operations/work-orders

POST /operations/assign

GET /operations/room-status

GET /operations/metrics
Events

Generate

HousekeepingTaskCreated

HousekeepingCompleted

MaintenanceRequested

MaintenanceCompleted

RoomStatusChanged

TaskAssigned

TaskEscalated

SLABreached

InspectionPassed

InspectionFailed

Events should be reusable by future modules.

AI Tools

Create

AssignTaskTool

RoomStatusTool

HousekeepingTool

MaintenanceTool

StaffAvailabilityTool

PriorityCalculatorTool

InspectionTool

SLATool

Each tool declares

Input Schema

Output Schema

Permissions

Timeout

Retry Policy

Analytics

Track

Cleaning time

Maintenance time

SLA compliance

Average response time

Staff utilization

Room turnaround time

Task completion rate

Escalation rate

Operational efficiency

Specifications

Generate

.specs/business/operations/

housekeeping.md

maintenance.md

operations-agent.md

task-scheduler.md

sla.md

room-lifecycle.md

operations-events.md

work-orders.md
Documentation

Generate

docs/business/operations/

README.md

housekeeping.md

maintenance.md

task-prioritization.md

operations-agent.md

room-lifecycle.md

sla-management.md

operational-workflows.md
Testing

Create

Unit tests

Integration tests

Workflow tests

Scheduler tests

Agent tests

Task assignment tests

Coverage

≥95%

Quality Gates

Loop fails if

❌ Revenue forecasting implemented

❌ Dynamic pricing implemented

❌ Executive dashboard implemented

❌ ML forecasting models implemented

Those belong to future loops.

Acceptance Criteria

The platform should

Automatically create housekeeping tasks

Manage maintenance requests

Assign staff intelligently

Track room lifecycle

Execute operational workflows

Monitor SLA compliance

Generate operational alerts

Support AI-driven task prioritization

Expose documented APIs

Pass all tests

Definition of Done

Loop 12 is complete only if

Housekeeping Platform implemented

Maintenance Platform implemented

Operations Agent operational

Task Scheduler functional

Room Lifecycle enforced

Operational workflows implemented

SLA monitoring active

Notifications operational

APIs documented

Specifications complete

Tests passing

Documentation complete

Exit Criteria

At the end of Loop 12, HospitalityAI contains a fully functional Hotel Operations Platform.

Guest actions from the Reservation and Guest Experience platforms automatically trigger operational workflows such as housekeeping, maintenance, inspections, and staff assignments.

The Operations Agent continuously optimizes task execution, monitors service-level agreements, and improves operational efficiency.

Engineering Notes for Antigravity

Before implementation:

Read all previous loops and execution-rules.md.
Generate or update .specs/business/operations/ before writing code.
Reuse the AI Platform, Multi-Agent Platform, Data Platform, and Reservation Platform rather than duplicating functionality.
Model room states as a finite state machine with validated transitions.
Implement all operational workflows as LangGraph graphs with checkpointing and recovery.
Use realistic seeded hotel operational data for testing.
Ensure every event emitted by the Operations Platform is documented and available for downstream consumers.
Verify all quality gates, update documentation, and ensure CI passes before marking the loop complete.
Deliverables Summary

By the end of Loop 12, Antigravity should have produced:

business/operations/
.specs/business/operations/
docs/business/operations/

Housekeeping Platform
Maintenance Platform
Operations Agent
Task Scheduling Engine
Room Lifecycle Manager
SLA Monitoring
Operational Analytics
LangGraph Workflows
REST APIs
Events
Tests
Documentation