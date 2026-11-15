import type { ResourceKey } from '../engine/types.ts'

const iconByResource: Record<ResourceKey, string> = {
  cost: 'icon_cost.png',
  mass: 'icon_mass.png',
  power: 'icon_power.png',
  data: 'icon_data.png',
  deltaV: 'icon_delta_v.png',
}

type IconProps = {
  name: ResourceKey
  label?: string
}

export function Icon({ name, label }: IconProps) {
  return (
    <img
      className="resource-icon"
      src={`/assets/icons/${iconByResource[name]}`}
      alt={label ?? name}
      title={label ?? name}
    />
  )
}
