import type { Build } from './types.ts';

export const LUNAR_BUILD: Build = {
  missionId: 'mission_lunar_ice_hunter',
  orbitId: 'orbit_lunar_polar',
  rocketId: 'rocket_medium',
  busId: 'bus_medium',
  powerId: 'power_solar_l',
  commsId: 'comms_medium',
  propulsionId: 'prop_chem_large',
  instrumentIds: [
    'instr_radar_sounder',
    'instr_neutron_detector',
    'instr_spectrometer',
  ],
  supportIds: ['support_rad_shield'],
};

export function withOverrides(base: Build, partial: Partial<Build>): Build {
  return {
    ...base,
    ...partial,
  };
}
