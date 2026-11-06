import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => ({
  theme: 'base',
  themeVariables: {
    background: 'transparent',
    primaryColor: '#0f1a15',
    primaryTextColor: '#e8fff3',
    primaryBorderColor: '#7fffb5',
    lineColor: '#7fffb5',
    secondaryColor: '#14100c',
    tertiaryColor: '#0b0f0d',
    fontFamily: 'IBM Plex Mono, monospace',
    fontSize: '15px',
  },
}))
