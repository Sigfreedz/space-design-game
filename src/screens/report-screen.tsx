import { useEffect } from 'react'
import type { MissionState } from '../engine/types.ts'
import type { SoundName } from '../audio/use-game-audio.ts'

type ReportScreenProps = {
  state: MissionState
  onReplay: () => void
  onBackToBuild: () => void
  onSound: (name: SoundName) => void
}

const outcomeLabels = {
  mission_lost: 'MISSION LOST',
  failed: 'MISSION FAILED',
  partial_success: 'PARTIAL SUCCESS',
  success: 'MISSION SUCCESS',
  outstanding: 'OUTSTANDING MISSION',
}

export function ReportScreen({ state, onReplay, onBackToBuild, onSound }: ReportScreenProps) {
  const score = state.score
  const report = state.report

  useEffect(() => {
    if (score) {
      onSound(score.outcome === 'mission_lost' || score.outcome === 'failed' ? 'fail_sound' : 'success_jingle')
    }
  }, [onSound, score])

  if (!score || !report) return null

  return (
    <main className="game-shell">
      <section className="game-stage report-stage" aria-label="Mission report">
        <header className="game-header">
          <div>
            <p className="eyebrow">MISSION CONTROL // FINAL TRANSMISSION</p>
            <h1>TRADE-OFF REPORT</h1>
          </div>
          <div className={`report-outcome report-outcome--${score.outcome}`}>{outcomeLabels[score.outcome]}</div>
        </header>
        <div className="report-layout">
          <section className="score-card">
            <p className="event-card__eyebrow">MISSION SCORE</p>
            <strong className="score-total">{score.total.toFixed(1)}</strong><span className="score-max"> / 100</span>
            <div className="score-breakdown">
              <span>SCIENCE <b>{score.breakdown.science.toFixed(1)}</b></span>
              <span>RESILIENCE <b>{score.breakdown.resilience.toFixed(1)}</b></span>
              <span>BUDGET <b>{score.breakdown.budget.toFixed(1)}</b></span>
              <span>MARGINS <b>{score.breakdown.margin.toFixed(1)}</b></span>
            </div>
            <p className="report-summary">Science collected: <b>{state.scienceCollected.toFixed(1)}</b> · Events resolved: <b>{state.eventResults.length}</b></p>
            <div className="report-actions">
              <button type="button" className="launch-button" onClick={onReplay}>REPLAY MISSION</button>
              <button type="button" className="secondary-button" onClick={onBackToBuild}>RETURN TO BUILD</button>
            </div>
          </section>
          <section className="report-list">
            <div className="report-column">
              <h2>WHAT HELPED</h2>
              {report.helped.length === 0 ? <p className="issue-muted">No strong advantage recorded.</p> : report.helped.map((item) => <article key={item.title}><b>{item.title}</b><p>{item.detail}</p></article>)}
            </div>
            <div className="report-column report-column--hurt">
              <h2>WHAT HURT</h2>
              {report.hurt.length === 0 ? <p className="issue-muted">No major trade-off recorded.</p> : report.hurt.map((item) => <article key={item.title}><b>{item.title}</b><p>{item.detail}</p>{item.whatIf && <small>WHAT-IF: {item.whatIf}</small>}</article>)}
            </div>
          </section>
        </div>
      </section>
    </main>
  )
}
