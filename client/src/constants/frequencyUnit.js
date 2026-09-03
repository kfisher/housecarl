// Copyright 2026 Kevin Fisher. All rights reserved.
// SPDX-License-Identifier: AGPL-3.0-only

// Approximate day counts used to convert between a value/unit pair and the
// ISO 8601 duration string stored by the server, matching how the server's
// timedelta parsing treats each designator.
export const frequencyUnitDays = {
  D: 1,
  W: 7,
  M: 30,
  Y: 365,
}

export const frequencyUnitOptions = [
  { value: 'D', label: 'Days' },
  { value: 'W', label: 'Weeks' },
  { value: 'M', label: 'Months' },
  { value: 'Y', label: 'Years' },
]

export const defaultFrequencyUnit = 'W'
