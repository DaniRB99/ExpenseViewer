import { useState } from 'react'
import './App.css'
import PokemonList from './components/PokemonList'
import { type Pokemon, defualtPokemon } from './types/Pokemon'
import DetailsWrapper from './hoc/DetailsWrapper'
import PokemonDetails from './components/PokemonDetails'
import PokemonDetails2 from './components/PokemonDetails2'
import Balance from './components/balance'

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
				{/* {selectedPokemon.id != -1 && (
					<DetailsWrapper render={getDetails1}></DetailsWrapper>
				)}
				{selectedPokemon2.id != -1 && (
					<DetailsWrapper render={getDetails2}></DetailsWrapper>
				)} */}
				<h2 className='subtitle'>Transactions</h2>
				<PokemonList selectPokemon={setSelectedPokemon} selectPokemon2={setSelectedPokemon2}></PokemonList>
			</main>
		</>
	)
}

export default App
