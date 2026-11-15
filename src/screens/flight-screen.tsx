import { useMemo } from 'react'
import type { MissionState, PlayerResponse } from '../engine/types.ts'
import { drawEvent, getEventPreview } from '../engine/engine.ts'

type FlightScreenProps = {
  state: MissionState
  onAdvance: (responses: PlayerResponse[]) => void
}

const stages = ['LAUNCH', 'CRUISE', 'INSERTION', 'SCIENCE 1', 'SCIENCE 2', 'SCIENCE 3']

function stageNeedsEvent(stage: number): boolean {
  return stage === 2 || stage >= 4
}

export function FlightScreen({ state, onAdvance }: FlightScreenProps) {
  const pendingEvent = useMemo(() => {
    if (!stageNeedsEvent(state.stage) || state.status !== 'active') return null
    const event = drawEvent(state).event
    return { event, preview: getEventPreview(state, event) }
  }, [state])

  const activeInstrument = state.instruments.find((instrument) => instrument.status === 'active')
  const lastResult = state.stageLog[state.stageLog.length - 1]

  return (
    <main className="game-shell">
      <section className="game-stage flight-stage" aria-label="Mission flight simulation">
        <header className="game-header">
          <div>
            <p className="eyebrow">MISSION CONTROL // LIVE TELEMETRY</p>
            <h1>FLIGHT SIMULATION</h1>
          </div>
          <div className="header-status"><span className="status-dot" /> LEARNING MODE</div>
        </header>

        <div className="stage-tracker">
          {stages.map((label, index) => (
            <div className={`stage-marker${index + 1 < state.stage ? ' stage-marker--done' : ''}${index + 1 === state.stage ? ' stage-marker--active' : ''}`} key={label}>
              <span>{index + 1}</span>{label}
            </div>
          ))}
        </div>

        <div className="flight-layout">
          <section className="flight-view">
            <div className="flight-view__scene">
              <img src="/assets/flight/mission_control_portrait_3f.png" alt="" className="control-portrait" />
              <img src="/assets/flight/sprite_rocket_medium.png" alt="Mission spacecraft" className="flight-rocket" />
              <div className="flight-view__scanline" />
              <div className="flight-view__caption">AUTONOMOUS MISSION FEED</div>
            </div>
            <div className="flight-readouts">
              <span>SCIENCE <b>{state.scienceCollected.toFixed(1)}</b></span>
              <span>CONTINGENCY <b>${state.contingencyFund.toFixed(0)}M</b></span>
              <span>ΔV <b>{state.remainingDeltaV ?? state.currentDeltaV} m/s</b></span>
            </div>
            {lastResult && <p className="stage-log">{lastResult.explanation}</p>}
          </section>

          <section className="event-panel">
            <div className="panel-title">STAGE {state.stage} // {stages[state.stage - 1]}</div>
            {pendingEvent ? (
              <>
                <div className="event-card">
                  <img src="/assets/build/launch_check_panel.png" alt="" />
                  <div>
                    <p className="event-card__eyebrow">EVENT DETECTED</p>
                    <h2>{pendingEvent.event.name}</h2>
                    <p>Checks <strong>{pendingEvent.event.checks.toUpperCase()}</strong> margin · difficulty <strong>{pendingEvent.preview.finalDifficulty}</strong></p>
                  </div>
                </div>
                <p className="event-explanation">{pendingEvent.preview.explanation}</p>
                <div className="odds-row">
                  <span className="odds-success">SUCCESS {pendingEvent.preview.outcomeRanges.success || '—'}</span>
                  <span className="odds-partial">PARTIAL {pendingEvent.preview.outcomeRanges.partial || '—'}</span>
                  <span className="odds-fail">FAIL {pendingEvent.preview.outcomeRanges.fail || '—'}</span>
                </div>
                <p className="learning-hint">
                  {state.stage === 2 ? 'FREE PRACTICE: Cruise collects no science.' : 'Choose a response, or continue without one.'}
                </p>
                <div className="response-list">
                  <button type="button" className="response-button response-button--primary" onClick={() => onAdvance([])}>NO RESPONSE</button>
                  {pendingEvent.preview.legalResponses.includes('spend_contingency') && (
                    <button type="button" className="response-button" onClick={() => onAdvance([{ kind: 'spend_contingency' }])}>SPEND CONTINGENCY<br /><small>+1 · $10M</small></button>
                  )}
                  {pendingEvent.preview.legalResponses.includes('throttle_data') && (
                    <button type="button" className="response-button" onClick={() => onAdvance([{ kind: 'throttle_data' }])}>THROTTLE DATA<br /><small>+1 · science ×0.5</small></button>
                  )}
                  {pendingEvent.preview.legalResponses.includes('safe_mode') && activeInstrument && (
                    <button type="button" className="response-button" onClick={() => onAdvance([{ kind: 'safe_mode', instrumentId: activeInstrument.id }])}>SAFE MODE<br /><small>+1 · {activeInstrument.id.replace('instr_', '')}</small></button>
                  )}
                </div>
              </>
            ) : (
              <>
                <div className="stage-brief">
                  <p className="event-card__eyebrow">NO EVENT RESPONSE REQUIRED</p>
                  <h2>{state.stage === 1 ? 'Launch sequence' : 'Orbit insertion'}</h2>
                  <p>{state.stage === 1 ? 'Learning mode launch proceeds. Watch the mission enter its first stage.' : 'The spacecraft will burn its required ΔV and attempt to enter the target orbit.'}</p>
                </div>
                <button type="button" className="response-button response-button--primary response-button--wide" onClick={() => onAdvance([])}>
                  {state.stage === 1 ? 'BEGIN FLIGHT' : 'PERFORM INSERTION'}
                </button>
              </>
            )}
          </section>
        </div>
      </section>
    </main>
  )
}
