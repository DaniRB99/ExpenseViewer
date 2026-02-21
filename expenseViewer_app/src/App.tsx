import { useState } from 'react'
import './App.css'
import PokemonList from './components/PokemonList'
import { type Pokemon, defualtPokemon } from './types/Pokemon'
import PokemonDetails from './components/PokemonDetails'
import PokemonDetails2 from './components/PokemonDetails2'
import Balance from './components/Balance'
import TransactionList from './components/TransactionList'
import { TransactionProviderWrapper } from './context/TransactionContexts'

function App() {
	const [selectedPokemon, setSelectedPokemon] = useState<Pokemon>(defualtPokemon)
	const [selectedPokemon2, setSelectedPokemon2] = useState<Pokemon>(defualtPokemon)
	const getDetails1 = (likes:number, increaseLikes:()=>void) => {
		return (
			<PokemonDetails pokemon={selectedPokemon}
				likes={likes}
				increaseLikes={increaseLikes}>
			</PokemonDetails>
		);
	};

	const getDetails2 = (likes:number, increaseLikes:()=>void) => {
		return (
			<PokemonDetails2 pokemon={selectedPokemon2}
				likes={likes}
				increaseLikes={increaseLikes}>
			</PokemonDetails2>
		);
	};


	return (
		<>
			<main className='main'>
				<header className="main-menu">
					<h1 className="Header-title">Expense Viewer</h1>
					<ul>
						<li>Home</li>
						<li>Categories</li>
						<li>Transactions</li>
					</ul>
				</header>
				<Balance></Balance>

				<h2 className='subtitle'>Transactions</h2>
				<TransactionProviderWrapper>
					<TransactionList></TransactionList>
				</TransactionProviderWrapper>
			</main>
		</>
	)
}

export default App
