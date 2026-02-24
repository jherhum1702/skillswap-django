---
name: Bug report 🐛
about: Report a bug
title: "[Bug] "
labels: bug
body:
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Low
        - Medium  
        - High
      default: 1
      required: true
  - type: textarea
    id: problem
    attributes:
      label: "**Problem:**"
  - type: textarea
    id: actual
    attributes:
      label: "**What happens:**"
  - type: textarea
    id: expected
    attributes:
      label: "**Expected:**"
---

**Priority:** Low/Medium/High

**Problem:**

**What happens:**

**Expected:**