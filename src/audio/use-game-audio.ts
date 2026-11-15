import { useCallback, useEffect, useMemo } from 'react'

export type SoundName =
  | 'card_pickup'
  | 'card_place'
  | 'event_alert'
  | 'launch_rumble'
  | 'success_jingle'
  | 'fail_sound'
  | 'ui_click'

type MusicName = 'build' | 'flight'

const soundFiles: Record<SoundName, string> = {
  card_pickup: '/assets/audio/sfx_card_pickup.wav',
  card_place: '/assets/audio/sfx_card_place.wav',
  event_alert: '/assets/audio/sfx_event_alert.wav',
  launch_rumble: '/assets/audio/sfx_launch_rumble.wav',
  success_jingle: '/assets/audio/sfx_success_jingle.wav',
  fail_sound: '/assets/audio/sfx_fail_sound.wav',
  ui_click: '/assets/audio/sfx_ui_click.wav',
}

const musicFiles: Record<MusicName, string> = {
  build: '/assets/audio/music_build_calm_loop.wav',
  flight: '/assets/audio/music_flight_tense_loop.wav',
}

function createAudio(src: string, loop = false): HTMLAudioElement {
  const audio = new Audio(src)
  audio.loop = loop
  audio.preload = 'auto'
  audio.volume = loop ? 0.18 : 0.35
  return audio
}

export function useGameAudio(screen: 'build' | 'flight' | 'report') {
  const music = useMemo(() => ({
    build: createAudio(musicFiles.build, true),
    flight: createAudio(musicFiles.flight, true),
  }), [])

  const playSound = useCallback((name: SoundName) => {
    const audio = createAudio(soundFiles[name])
    void audio.play().catch(() => {
      // Playback can be rejected until the user interacts with the page.
    })
  }, [])

  const playMusic = useCallback((name: MusicName) => {
    Object.entries(music).forEach(([key, audio]) => {
      if (key !== name) audio.pause()
    })
    void music[name].play().catch(() => {
      // Playback can be rejected until the user interacts with the page.
    })
  }, [music])

  useEffect(() => {
    if (screen === 'build') playMusic('build')
    if (screen === 'flight') playMusic('flight')
    if (screen === 'report') music.flight.pause()

    return () => {
      if (screen === 'report') {
        music.build.pause()
        music.flight.pause()
      }
    }
  }, [music, playMusic, screen])

  return { playSound, playMusic }
}
