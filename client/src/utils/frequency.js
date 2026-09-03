// Copyright 2026 Kevin Fisher. All rights reserved.
// SPDX-License-Identifier: AGPL-3.0-only

import { frequencyUnitDays, frequencyUnitOptions } from '@/constants/frequencyUnit'

function parseFrequencyToDays(iso) {
  const match = /^P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)W)?(?:(\d+)D)?/.exec(iso)
  const [, years, months, weeks, days] = match ?? []
  return (
    Number(years || 0) * frequencyUnitDays.Y +
    Number(months || 0) * frequencyUnitDays.M +
    Number(weeks || 0) * frequencyUnitDays.W +
    Number(days || 0)
  )
}

// Chooses the largest unit that evenly reconstructs the stored duration, since
// the server always round-trips frequency as a plain day (or year) count.
export function parseFrequency(iso) {
  const totalDays = Math.max(1, parseFrequencyToDays(iso))

  for (const unit of ['Y', 'M', 'W']) {
    const unitDays = frequencyUnitDays[unit]
    if (totalDays % unitDays === 0) {
      return { value: totalDays / unitDays, unit }
    }
  }
  return { value: totalDays, unit: 'D' }
}

export function formatFrequency(iso) {
  const { value, unit } = parseFrequency(iso)
  const label = frequencyUnitOptions.find((option) => option.value === unit).label
  return `${value} ${value === 1 ? label.replace(/s$/, '') : label}`
}
