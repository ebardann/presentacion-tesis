import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => ({
  theme: 'base',
  themeVariables: {
    background: 'transparent',
    primaryColor: '#0e1f18',
    primaryTextColor: '#f1ecd8',
    primaryBorderColor: '#3fd9c7',
    lineColor: '#8fe36a',
    secondaryColor: '#1a1a0c',
    tertiaryColor: '#08130f',
    fontFamily: 'IBM Plex Mono, monospace',
    fontSize: '15px',
  },
}))
