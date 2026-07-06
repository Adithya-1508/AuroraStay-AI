# Decision Process

To maintain architectural integrity, HospitalityAI requires a formal decision-making and documenting process for all structural changes.

## 1. Architectural Changes (ADRs)
Every major architectural decision (e.g. database choice, framework selection, messaging protocol) must be documented as an **Architecture Decision Record (ADR)**.
- **Location**: `.adr/`
- **Format**: Use the [ADR Template](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.templates/adr.md).
- **Status Lifecycle**:
  - `Draft`: Proposed change, under review.
  - `Approved`: Accepted by the engineering lead/user; ready for implementation.
  - `Rejected`: Proposed change rejected with documented rationale.
  - `Superseded`: Replaced by a newer ADR.

## 2. Feature Architecture (RFCs)
Before implementing a new platform, system service, or significant module, write a **Request for Comments (RFC)** to specify system boundaries, data flow, and APIs.
- **Location**: `.rfc/`
- **Format**: Use the [RFC Template](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.templates/rfc.md).
- **Process**: Submit the RFC to the user for review. Coding cannot begin until the RFC is approved.

## 3. Specifications (Specs)
Specifications contain the granular technical design for individual entities, components, or tasks.
- **Location**: `.specs/`
- **Format**: Use the [Specification Template](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.templates/specification.md).
- **Gate**: Specs must satisfy the [Definition of Ready](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.foundation/definition_of_ready.md) before starting coding.
