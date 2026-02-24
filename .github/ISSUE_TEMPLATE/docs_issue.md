---
name: Documentation 📚
about: Improve or add documentation
title: "[Docs] "
labels: documentation
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
    id: description
    attributes:
      label: What needs documentation?
      description: "README, docstrings, comments, templates..."
      placeholder: "Add API endpoint docs to README.md"
      required: true
  - type: textarea
    id: location
    attributes:
      label: Location
      description: "Where to add/update docs? (e.g. core/models.py docstrings, .github/templates)"
---

**Priority:** Low/Medium/High

**What:** Documentation needed

**Where:** File/Location (e.g. README.md, docstrings)
