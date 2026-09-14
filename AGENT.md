# NORVAULT Agent Architecture

The NORVAULT agent pipeline operates completely differently from a standard RAG or LLM chatbot. It relies heavily on strict, typed adapters and a multi-stage deterministic pipeline.

## 1. Identity Firewall
The first stage of any query. If the organization number does not perfectly match a live BRREG Enhetsregisteret entry, the pipeline halts immediately. This prevents the agent from processing partial or misspelled company requests and retrieving the wrong company's data.

## 2. Temporal Truth Engine
Tracks the freshness of every retrieved fact. BRREG financial facts are only valid for the fiscal year they describe, while role facts are current unless marked resigned. The engine stamps facts as \CURRENT\, \RECENT\, or \STALE\.

## 3. Contradiction Engine
Groups facts by subject and predicate to find internal clashes. If two sources disagree on the CEO's name, the engine detects this and escalates it to the Adversarial Auditor for conflict resolution based on source authority level and timestamp.

## 4. Adversarial Auditor
Before any fact is permitted to enter the \ProofPassport\ output, it must pass a rigorous audit loop. It requires absolute traceability to a recognized source. Facts without a clear extraction lineage are dropped to prevent hallucinated numbers from entering the competition output.
