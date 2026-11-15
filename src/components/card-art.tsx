import type { CardType } from '../engine/types.ts'

const frameByType: Partial<Record<CardType, string>> = {
  mission: 'card_frame_mission.png',
  orbit: 'card_frame_orbit.png',
  rocket: 'card_frame_rocket.png',
  bus: 'card_frame_spacecraft.png',
  power: 'card_frame_spacecraft.png',
  comms: 'card_frame_spacecraft.png',
  propulsion: 'card_frame_spacecraft.png',
  instrument: 'card_frame_instrument.png',
  support: 'card_frame_spacecraft.png',
}

const iconByCardId: Record<string, string> = {
  instr_wide_camera: 'instr_wide_camera.png',
  instr_hires_imager: 'instr_hires_imager.png',
  instr_thermal_ir: 'instr_thermal_ir.png',
  instr_spectrometer: 'instr_spectrometer.png',
  instr_radar_sounder: 'instr_radar_sounder.png',
  instr_neutron_detector: 'instr_neutron_detector.png',
  instr_laser_altimeter: 'instr_laser_altimeter.png',
  instr_magnetometer: 'instr_magnetometer.png',
}

const colorByType: Record<CardType, string> = {
  mission: 'var(--c-mission)',
  orbit: 'var(--c-orbit)',
  rocket: 'var(--c-rocket)',
  bus: 'var(--c-spacecraft)',
  power: 'var(--c-spacecraft)',
  comms: 'var(--c-spacecraft)',
  propulsion: 'var(--c-spacecraft)',
  instrument: 'var(--c-instrument)',
  support: 'var(--c-spacecraft)',
  event: 'var(--c-event)',
}

type CardArtProps = {
  cardId: string
  cardType: CardType
  alt: string
}

export function CardArt({ cardId, cardType, alt }: CardArtProps) {
  const frame = frameByType[cardType]
  const icon = iconByCardId[cardId]

  return (
    <div className="card-art" style={{ '--art-color': colorByType[cardType] } as React.CSSProperties}>
      {icon ? (
        <img
          className="card-art__illustration"
          src={`/assets/icons/${icon}`}
          alt={alt}
        />
      ) : (
        <div className="card-art__fallback" aria-label={`${alt} placeholder`} />
      )}
      {frame && (
        <img
          className="card-art__frame"
          src={`/assets/cards/${frame}`}
          alt=""
          aria-hidden="true"
        />
      )}
    </div>
  )
}
