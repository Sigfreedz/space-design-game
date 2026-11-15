import { useMemo, useState } from 'react'
import type { Card, Build, CardType, MissionState, PlayerResponse, ResourceKey } from './engine/types.ts'
import { createMissionState, runStage, validateBuild } from './engine/engine.ts'
import {
  buses,
  comms,
  instruments,
  missions,
  orbits,
  power,
  propulsion,
  rockets,
  supports,
} from './data/index.ts'
import { LUNAR_BUILD } from './engine/fixtures.ts'
import { CardView } from './components/card-view.tsx'
import { Gauge } from './components/gauge.tsx'
import { FlightScreen } from './screens/flight-screen.tsx'
import { ReportScreen } from './screens/report-screen.tsx'

type Tab = 'mission' | 'spacecraft' | 'payload'
type SingleSlot = Exclude<keyof Build, 'instrumentIds' | 'supportIds'>

const tabs: Array<{ id: Tab; label: string; slots: string }> = [
  { id: 'mission', label: 'MISSION', slots: 'Mission · Orbit · Rocket' },
  { id: 'spacecraft', label: 'SPACECRAFT', slots: 'Bus · Power · Communications · Propulsion' },
  { id: 'payload', label: 'PAYLOAD', slots: 'Instruments · Supports' },
]

const catalogByTab: Record<Tab, Card[]> = {
  mission: [...missions, ...orbits, ...rockets],
  spacecraft: [...buses, ...power, ...comms, ...propulsion],
  payload: [...instruments, ...supports],
}

const slotForType: Partial<Record<CardType, SingleSlot>> = {
  mission: 'missionId',
  orbit: 'orbitId',
  rocket: 'rocketId',
  bus: 'busId',
  power: 'powerId',
  comms: 'commsId',
  propulsion: 'propulsionId',
}

function cardIsSelected(build: Build, card: Card): boolean {
  const slot = slotForType[card.type]
  if (slot) return build[slot] === card.id
  if (card.type === 'instrument') return build.instrumentIds.includes(card.id)
  if (card.type === 'support') return build.supportIds.includes(card.id)
  return false
}

function emptyBuild(): Build {
  return {
    missionId: null,
    orbitId: null,
    rocketId: null,
    busId: null,
    powerId: null,
    commsId: null,
    propulsionId: null,
    instrumentIds: [],
    supportIds: [],
  }
}

function App() {
  const [build, setBuild] = useState<Build>(LUNAR_BUILD)
  const [activeTab, setActiveTab] = useState<Tab>('mission')
  const [notice, setNotice] = useState('')
  const [missionState, setMissionState] = useState<MissionState | null>(null)
  const [screen, setScreen] = useState<'build' | 'flight' | 'report'>('build')

  const validation = useMemo(() => validateBuild(build), [build])
  const calculated = validation.calculatedBuild
  const selectedBus = buses.find((card) => card.id === build.busId)

  function chooseCard(card: Card) {
    setNotice('')
    const slot = slotForType[card.type]
    if (slot) {
      setBuild((current) => ({ ...current, [slot]: current[slot] === card.id ? null : card.id }))
      return
    }

    if (card.type === 'instrument') {
      setBuild((current) => {
        const selected = current.instrumentIds.includes(card.id)
        if (selected) return { ...current, instrumentIds: current.instrumentIds.filter((id) => id !== card.id) }
        if (selectedBus && current.instrumentIds.length >= selectedBus.instrumentSlots) return current
        return { ...current, instrumentIds: [...current.instrumentIds, card.id] }
      })
    }

    if (card.type === 'support') {
      setBuild((current) => {
        const selected = current.supportIds.includes(card.id)
        if (selected) return { ...current, supportIds: current.supportIds.filter((id) => id !== card.id) }
        if (selectedBus && current.supportIds.length >= selectedBus.supportSlots) return current
        return { ...current, supportIds: [...current.supportIds, card.id] }
      })
    }
  }

  function resetBuild() {
    setBuild(emptyBuild())
    setNotice('Build cleared. Select cards to begin.')
  }

  function startMission() {
    try {
      const state = createMissionState(build, 'learning', Date.now())
      setMissionState(state)
      setScreen('flight')
    } catch (error) {
      setNotice(error instanceof Error ? error.message : 'Unable to start the mission.')
    }
  }

  function advanceMission(responses: PlayerResponse[]) {
    if (!missionState) return
    try {
      const next = runStage(missionState, responses).state
      setMissionState(next)
      if (next.status !== 'active') setScreen('report')
    } catch (error) {
      setNotice(error instanceof Error ? error.message : 'The flight simulation could not advance.')
    }
  }

  function replayMission() {
    try {
      setMissionState(createMissionState(build, 'learning', Date.now()))
      setScreen('flight')
    } catch (error) {
      setNotice(error instanceof Error ? error.message : 'Unable to replay the mission.')
    }
  }

  if (screen === 'flight' && missionState) {
    return <FlightScreen state={missionState} onAdvance={advanceMission} />
  }

  if (screen === 'report' && missionState) {
    return <ReportScreen state={missionState} onReplay={replayMission} onBackToBuild={() => setScreen('build')} />
  }

  return (
    <main className="game-shell">
      <section className="game-stage" aria-label="Mission build screen">
        <header className="game-header">
          <div>
            <p className="eyebrow">NASA SPACE APPS 2026</p>
            <h1>MISSION DESIGN LAB</h1>
          </div>
          <div className="header-status"><span className="status-dot" /> LEARNING MODE</div>
        </header>

        <div className="build-layout">
          <section className="catalog-panel">
            <div className="panel-title">
              <span>BUILD CATALOG</span>
              <button type="button" className="text-button" onClick={resetBuild}>CLEAR</button>
            </div>
            <div className="tab-row" role="tablist" aria-label="Build card groups">
              {tabs.map((tab) => (
                <button
                  type="button"
                  role="tab"
                  aria-selected={activeTab === tab.id}
                  className={`tab-button${activeTab === tab.id ? ' tab-button--active' : ''}`}
                  onClick={() => setActiveTab(tab.id)}
                  key={tab.id}
                >
                  {tab.label}
                  <small>{tab.slots}</small>
                </button>
              ))}
            </div>
            <div className="catalog-grid">
              {catalogByTab[activeTab].map((card) => {
                const selected = cardIsSelected(build, card)
                const overCapacity =
                  (card.type === 'instrument' && !selected && !!selectedBus && build.instrumentIds.length >= selectedBus.instrumentSlots) ||
                  (card.type === 'support' && !selected && !!selectedBus && build.supportIds.length >= selectedBus.supportSlots)
                return (
                  <CardView
                    key={card.id}
                    card={card}
                    selected={selected}
                    disabled={overCapacity}
                    onClick={() => chooseCard(card)}
                  />
                )
              })}
            </div>
          </section>

          <aside className="side-panel">
            <div className="panel-title">LIVE TELEMETRY</div>
            <div className="gauge-list">
              {(['cost', 'mass', 'power', 'data'] as ResourceKey[]).map((resource) => {
                const value = resource === 'cost'
                  ? calculated.totals.cost
                  : resource === 'mass'
                    ? calculated.totals.mass
                    : resource === 'power'
                      ? calculated.totals.powerDraw
                      : calculated.totals.dataGenerated
                const limit = resource === 'cost'
                  ? calculated.limits.cost
                  : resource === 'mass'
                    ? calculated.limits.mass
                    : resource === 'power'
                      ? calculated.limits.power
                      : calculated.limits.data
                return <Gauge key={resource} resource={resource} value={value} limit={limit} tier={calculated.tiers[resource]} />
              })}
            </div>
            <div className="science-readout">
              <span>POTENTIAL SCIENCE</span>
              <strong>{calculated.totals.potentialScience.toFixed(1)}</strong>
            </div>
            <div className="launch-panel">
              <div className="panel-title">LAUNCH CHECK</div>
              <p className={validation.valid ? 'check-success' : 'check-failure'}>
                {validation.valid ? '◆ READY FOR LAUNCH' : '× BUILD NEEDS ATTENTION'}
              </p>
              <div className="issue-list">
                {[...validation.errors, ...validation.warnings].map((issue) => (
                  <p className={issue.code.startsWith('DATA') ? 'issue-warning' : 'issue-error'} key={`${issue.code}-${issue.message}`}>
                    <b>{issue.code}</b> {issue.message}
                  </p>
                ))}
                {validation.valid && validation.warnings.length === 0 && <p className="issue-muted">All hard limits are satisfied.</p>}
              </div>
              <button
                type="button"
                className="launch-button"
                disabled={!validation.valid}
                onClick={startMission}
              >
                START MISSION
              </button>
              {notice && <p className="launch-notice">{notice}</p>}
            </div>
          </aside>
        </div>
      </section>
    </main>
  )
}

export default App
