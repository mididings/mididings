# Mididings Governance Model

## Purpose

This document defines a minimal and practical governance model
to ensure the long-term stability, security, and continuity of
the mididings project.

The goal is to avoid any single point of failure while keeping
the project lightweight and maintainable.

---

## Maintainers

The project is maintained by a group of core maintainers.

Responsibilities include:

- Reviewing and merging pull requests
- Managing releases
- Maintaining infrastructure
- Ensuring project continuity

There is no single "project owner".
Decisions are made collaboratively.

---

## GitHub Organization

The project is hosted under the GitHub organization:

mididings

Rules:

- At least two maintainers must have the Owner role.
- Two-factor authentication (2FA) is strongly required for all maintainers.
- No critical repository must depend on a personal GitHub account.

This ensures continuity if one maintainer becomes unavailable.

---

## Infrastructure & Credentials

All shared credentials are stored in a shared password manager
organization.

Rules:

- No credentials are shared via email or chat.
- At least two maintainers are Owners of the password vault.
- Recovery codes (Google, hosting, etc.) are stored securely.

The goal is to eliminate single points of failure.

---

## Financial Model

Donations, if enabled, are used strictly to cover
project-related infrastructure costs:

- Hosting
- Domain name
- Security tools
- Development infrastructure

The project does not operate as a legal entity.
Funds are handled by a designated financial contact
among the maintainers.

A simple annual cost summary may be published for transparency.

---

## Maintainer Changes

If a maintainer leaves:

- Access to GitHub organization is revoked.
- Access to shared password manager is revoked.
- No infrastructure should depend solely on that person.

If a new maintainer joins:

- Access is granted progressively.
- Owner roles are assigned carefully.

---

## Bus Factor Policy

The project aims to maintain a bus factor of at least 2.

No critical access, infrastructure, or knowledge
should depend on a single individual.
