// Copyright 2026 Kevin Fisher. All rights reserved.
// SPDX-License-Identifier: AGPL-3.0-only

const allTaskStates = [
  { value: 0, label: 'Unknown' },
  { value: 1, label: 'Critical' },
  { value: 2, label: 'Fair' },
  { value: 3, label: 'Good' },
]

export const taskStateLabels = Object.fromEntries(
  allTaskStates.map((option) => [option.value, option.label]),
)

// Unknown is excluded: it isn't a selectable state, only a possible legacy value.
export const taskStateOptions = allTaskStates.filter((option) => option.value !== 0)
