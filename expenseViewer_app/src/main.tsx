import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { PokemonProviderWrapper } from './context/pokemonContext.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <PokemonProviderWrapper>
      <App />
    </PokemonProviderWrapper>
  </StrictMode>,
)
