import type { Card } from '../engine/types.ts'
import { CardArt } from './card-art.tsx'

type CardViewProps = {
  card: Card
  selected?: boolean
  disabled?: boolean
  onClick: () => void
}

function cardDetail(card: Card): string {
  if (card.type === 'mission') return `$${card.budgetCap}M · target ${card.scienceTarget}`
  if (card.type === 'orbit') return `${card.minDeltaV} ΔV · reach ${card.reachFactor}`
  if (card.type === 'rocket') return `${card.capacityLEO.toLocaleString()} kg · ${Math.round(card.reliability * 100)}%`
  if (card.type === 'bus') return `${card.instrumentSlots}I · ${card.supportSlots}S · ${card.power}W`
  if (card.type === 'power') return `${card.output}W output`
  if (card.type === 'comms') return `${card.downlink} Mbps · ${card.power}W`
  if (card.type === 'propulsion') return `${card.deltaV} ΔV`
  if (card.type === 'instrument') return `${card.science} science · ${card.power}W`
  return card.tags.join(' · ') || 'support system'
}

export function CardView({ card, selected = false, disabled = false, onClick }: CardViewProps) {
  return (
    <button
      type="button"
      className={`card-view${selected ? ' card-view--selected' : ''}${disabled ? ' card-view--disabled' : ''}`}
      disabled={disabled}
      onClick={onClick}
      aria-pressed={selected}
    >
      <CardArt cardId={card.id} cardType={card.type} alt={card.name} />
      <span className="card-view__name">{card.name}</span>
      <span className="card-view__detail">{cardDetail(card)}</span>
      <span className="card-view__cost">{card.cost > 0 ? `$${card.cost}M` : card.type}</span>
    </button>
  )
}
