---
name: Bug Report
description: Create a report to help us improve.
labels: [bug]
assignees: ItsNeil17
body:
  - type: markdown
    attributes:
      value: |
        **Thanks for taking a minute to file a bug report!**

        ⚠
        Verify first that your issue is not [already reported on
        GitHub][issue search].

        _Please fill out the form below with as many precise
        details as possible._

        [issue search]: ../search?q=is%3Aissue&type=issues

  - type: textarea
    attributes:
      label: Describe the bug
      description: >-
        A clear and concise description of what the bug is.
    validations:
      required: true

  - type: textarea
    attributes:
      label: To Reproduce
      description: >-
        Describe the steps to reproduce this bug.
      placeholder: |
        1. Implement the following server or a client '...'
        2. Then run '...'
        3. An error occurs.
    validations:
      required: true

  - type: textarea
    attributes:
      label: Expected behavior
      description: >-
        A clear and concise description of what you expected to happen.
    validations:
      required: true

  - type: textarea
    attributes:
      label: Logs/tracebacks
      description: |
        If applicable, add logs/tracebacks to help explain your problem.
        Paste the output of the steps above, including the commands
        themselves and their output/traceback etc.
      render: python-traceback
    validations:
      required: true

  - type: textarea
    attributes:
      label: Python Version
      description: Attach your version of Python.
      render: console
      value: |
        $ python --version
    validations:
      required: true
  - type: textarea
    attributes:
      label: axterdb Version
      description: Attach your version of axterdb.
      render: console
      value: |
        $ python -m pip show axterdb
    validations:
      required: true

  - type: textarea
    attributes:
      label: OS
      placeholder: >-
        For example, Arch Linux, Windows, macOS, etc.
    validations:
      required: true

  - type: textarea
    attributes: 
      label: Additional context
      description: |
        Add any other context about the problem here.

        Describe the environment you have that lead to your issue.
        This includes proxy server and other bits that are related to your case.
