import { describe, it, expect } from 'vitest';
import {
  calculateBuild,
  validateBuild,
  createMissionState,
  getEventPreview,
  drawEvent,
  resolveEvent,
  runStage,
  computeScore,
} from './engine.ts';
import { LUNAR_BUILD, withOverrides } from './fixtures.ts';
import { eventById, missions } from '../data/index.ts';

describe('engine contract acceptance tests', () => {
  it('1. calculateBuild(LUNAR_BUILD): totals, limits, margins, tiers, and potential science match Section 14 exactly', () => {
    const result = calculateBuild(LUNAR_BUILD);
    expect(result.totals.cost).toBe(452);
    expect(result.limits.cost).toBe(480);
    expect(result.totals.mass).toBe(725);
    expect(result.limits.mass).toBe(1050);
    expect(result.totals.powerDraw).toBe(370);
    expect(result.totals.powerOutput).toBe(600);
    expect(result.totals.dataGenerated).toBe(15);
    expect(result.totals.downlink).toBe(20);
    expect(result.totals.deltaV).toBe(2000);
    expect(result.limits.deltaV).toBe(1500);
    expect(result.totals.potentialScience).toBe(66);
    expect(result.dataThrottle).toBe(1);
    expect(result.contingencyAtLaunch).toBe(28);
    expect(result.margins.cost).toBeCloseTo(0.0583, 3);
    expect(result.margins.mass).toBeCloseTo(0.3095, 3);
    expect(result.margins.power).toBeCloseTo(0.3833, 3);
    expect(result.margins.data).toBeCloseTo(0.25, 3);

    expect(result.tiers.cost).toBe('red');
    expect(result.tiers.mass).toBe('green');
    expect(result.tiers.power).toBe('green');
    expect(result.tiers.data).toBe('green');
  });

  it('2. validateBuild with rocket_light blocks launch with mass overrun LV-06', () => {
    const result = validateBuild(withOverrides(LUNAR_BUILD, { rocketId: 'rocket_light' }));
    expect(result.valid).toBe(false);
    expect(result.calculatedBuild.limits.mass).toBe(525);
    expect(result.errors.some((e) => e.code === 'LV-06')).toBe(true);
  });

  it('3. validateBuild with comms_small allows launch with soft warning and throttled data', () => {
    const result = validateBuild(withOverrides(LUNAR_BUILD, { commsId: 'comms_small' }));
    expect(result.valid).toBe(true);
    expect(result.warnings.length).toBeGreaterThan(0);
    expect(result.calculatedBuild.dataThrottle).toBeCloseTo(0.2667, 3);
  });

  it('4. validateBuild with power_solar_s blocks launch with power deficit LV-07', () => {
    const result = validateBuild(withOverrides(LUNAR_BUILD, { powerId: 'power_solar_s' }));
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.code === 'LV-07')).toBe(true);
  });

  it('5. validateBuild without mission priority instrument tags blocks launch with LV-03', () => {
    const result = validateBuild(
      withOverrides(LUNAR_BUILD, {
        instrumentIds: ['instr_wide_camera', 'instr_magnetometer'],
      })
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.code === 'LV-03')).toBe(true);
  });

  it('6. Learning-mode launch proceeds regardless of launch roll', () => {
    const state = createMissionState(LUNAR_BUILD, 'learning', 1);
    const next = runStage(state, []);
    expect(next.state.status).toBe('active');
  });

  it('7. getEventPreview calculates Radiation Shield tag bonus and Lunar Polar radiation difficulty', () => {
    const state = createMissionState(LUNAR_BUILD, 'learning', 1);
    const solarStorm = eventById['event_solar_storm'];
    const preview = getEventPreview(state, solarStorm);
    expect(preview.tagBonus).toBe(2);
    expect(preview.finalDifficulty).toBe(5); // base 4 + Lunar Polar radiation (2 => +1)
  });

  it('8. resolveEvent comms_blackout applies science multipliers on partial and fail', () => {
    // A Red data margin is needed for Comms Blackout to have both
    // partial and fail outcomes on an unmodified d6. Small Antenna gives
    // Lunar Ice Hunter 4 Mbps downlink vs 15 Mbps generated: Red margin (+0).
    const weakCommsBuild = withOverrides(LUNAR_BUILD, { commsId: 'comms_small' });
    const commsBlackout = eventById['event_comms_blackout'];

    // Independent deterministic seeds force different d6 outcomes.
    // Seeds are for the current seeded engine implementation at Stage 4:
    // 8 -> d6=3 (Partial), 1 -> d6=2 (Fail).
    const partialState = createMissionState(weakCommsBuild, 'learning', 8);
    partialState.stage = 4;
    const failState = createMissionState(weakCommsBuild, 'learning', 1);
    failState.stage = 4;

    const partialRes = resolveEvent(partialState, commsBlackout, []);
    const failRes = resolveEvent(failState, commsBlackout, []);

    expect(partialRes.result.outcome).toBe('partial');
    expect(partialRes.result.effects).toEqual(
      expect.arrayContaining([expect.objectContaining({ type: 'science_multiplier', value: 0.5 })])
    );
    expect(failRes.result.outcome).toBe('fail');
    expect(failRes.result.effects).toEqual(
      expect.arrayContaining([expect.objectContaining({ type: 'science_multiplier', value: 0 })])
    );

    // Deterministic replay must still produce the same outcome.
    const replay = resolveEvent(partialState, commsBlackout, []);
    expect(replay.result).toEqual(partialRes.result);
  });

  it('9. Insertion loss when delta-v is below requirement causes mission lost', () => {
    const state = createMissionState(LUNAR_BUILD, 'learning', 1);
    state.stage = 2; // Cruise stage transitioning to insertion
    state.currentDeltaV = 1300; // 1300 < 1500 required for Lunar Polar
    const next = runStage(state, []);
    expect(next.state.status).toBe('lost');
  });

  it('10. Determinism: identical seed produces identical events drawn order and score total', () => {
    const stateA = createMissionState(LUNAR_BUILD, 'learning', 12345);
    const stateB = createMissionState(LUNAR_BUILD, 'learning', 12345);
    expect(stateA.eventDeck).toEqual(stateB.eventDeck);

    const runA = runStage(stateA, []);
    const runB = runStage(stateB, []);
    const scoreA = computeScore(runA.state);
    const scoreB = computeScore(runB.state);
    expect(runA.state.eventsDrawn).toEqual(runB.state.eventsDrawn);
    expect(scoreA.total).toBe(scoreB.total);
  });

  it('11. Margin-discipline curve: 9.9%->4.95, 10%->5, 25%->5, 26%->4.9, 50%->2.5, 75%->0, negative->0', () => {
    // Expected curve values per Section 15.16 & Amendment A1:
    // < 0% => 0
    // 0% to < 10% => 5 * (margin / 0.10) e.g. 9.9% -> 4.95
    // 10% to 25% => 5.0
    // > 25% => max(0, 5 * (1 - (margin - 0.25) / 0.50)) e.g. 26% -> 4.9, 50% -> 2.5, 75% -> 0
    const state = createMissionState(LUNAR_BUILD, 'learning', 1);
    state.initialMargins.cost = 0.099;
    state.initialMargins.mass = 0.26;
    state.initialMargins.power = 0.5;
    const score = computeScore(state);
    expect(score.marginByResource.cost).toBeCloseTo(4.95, 2);
    expect(score.marginByResource.mass).toBeCloseTo(4.9, 2);
    expect(score.marginByResource.power).toBeCloseTo(2.5, 2);
  });

  it('12. Deck: createMissionState builds eventDeck of exactly 8 unique ids; 4 draws never repeat', () => {
    const state = createMissionState(LUNAR_BUILD, 'learning', 42);
    expect(state.eventDeck).toHaveLength(8);
    expect(new Set(state.eventDeck).size).toBe(8);

    const draw1 = drawEvent(state);
    const draw2 = drawEvent(draw1.state);
    const draw3 = drawEvent(draw2.state);
    const draw4 = drawEvent(draw3.state);
    const drawnIds = [draw1.event.id, draw2.event.id, draw3.event.id, draw4.event.id];
    expect(new Set(drawnIds).size).toBe(4);
  });

  // Approved v7.3 (P7 G1-G2) Launch Check regression tests.
  it('13. LV-02 blocks a build with only one instrument', () => {
    const result = validateBuild(withOverrides(LUNAR_BUILD, {
      instrumentIds: ['instr_radar_sounder'],
    }));
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.code === 'LV-02')).toBe(true);
  });

  it('14. LV-02 blocks a build without supports', () => {
    const result = validateBuild(withOverrides(LUNAR_BUILD, { supportIds: [] }));
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.code === 'LV-02')).toBe(true);
  });

  it('15. LV-02 blocks a duplicate instrument card', () => {
    const result = validateBuild(withOverrides(LUNAR_BUILD, {
      instrumentIds: ['instr_radar_sounder', 'instr_radar_sounder'],
    }));
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.code === 'LV-02')).toBe(true);
  });

  it('16. LV-02 blocks a duplicate support card', () => {
    const result = validateBuild(withOverrides(LUNAR_BUILD, {
      supportIds: ['support_rad_shield', 'support_rad_shield'],
    }));
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.code === 'LV-02')).toBe(true);
  });

  it('17. Wildfire Watch science target is 32 (P7 G4)', () => {
    const wildfire = missions.find((mission) => mission.id === 'mission_wildfire_watch');
    expect(wildfire).toBeDefined();
    expect(wildfire?.scienceTarget).toBe(32);
  });
});
