import type { MarginTier, ResourceKey } from '../engine/types.ts'
import { Icon } from './icon.tsx'

type GaugeProps = {
  resource: ResourceKey
  value: number
  limit: number
  tier: MarginTier
}

const labels: Record<ResourceKey, string> = {
  cost: 'Cost',
  mass: 'Mass',
  power: 'Power',
  data: 'Data',
  deltaV: 'ΔV',
}

const units: Record<ResourceKey, string> = {
  cost: 'M',
  mass: 'kg',
  power: 'W',
  data: 'Mbps',
  deltaV: 'm/s',
}

function display(value: number): string {
  return Number.isInteger(value) ? String(value) : value.toFixed(1)
}

export function Gauge({ resource, value, limit, tier }: GaugeProps) {
  const ratio = limit > 0 ? Math.min(value / limit, 1) : 0
  return (
    <div className={`gauge gauge--${tier}`}>
      <div className="gauge__heading">
        <span><Icon name={resource} label={labels[resource]} />{labels[resource]}</span>
        <span className="gauge__tier" aria-label={`${tier} margin`}>{tier === 'green' ? '◆' : tier === 'yellow' ? '◇' : '×'}</span>
      </div>
      <div className="gauge__track"><span style={{ width: `${ratio * 100}%` }} /></div>
      <div className="gauge__value">{display(value)} / {display(limit)} {units[resource]}</div>
    </div>
  )
}
