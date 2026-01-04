import type { Pokemon } from "../types/Pokemon";
import "./PokemonCard.css"
// type Pokemon = {name:string, sprites:{front_default:string}} | null;

interface props {
    pokemon:Pokemon,
    selectPokemon:React.Dispatch<React.SetStateAction<Pokemon>>,
    selectedPokemon2:React.Dispatch<React.SetStateAction<Pokemon>>
}

function PokemonCard({pokemon, selectPokemon, selectedPokemon2}:props) {
    return (
        <li className="pokemon-card" onClick={() => selectPokemon(pokemon)} onAuxClick={() => selectedPokemon2(pokemon)}>
            <h2 className="pokemon-name">{pokemon.name}</h2>
            <img src={pokemon.sprites.front_default} alt="pokemon-img" className="pokemon-img" />
            <h3 className="text">HP: {pokemon.stats[0].base_stat}</h3>
        </li>
    );
}

export default PokemonCard