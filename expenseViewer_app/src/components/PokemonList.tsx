import { useContext, useEffect, useState } from "react";
import PokemonCard from "./PokemonCard"
import { defualtPokemon, type PokeList, type Pokemon } from "../types/Pokemon";
import "./PokemonList.css"
import GetForm from "./GetForm";
import { PokemonContext } from "../context/pokemonContext";

interface props {
    selectPokemon: React.Dispatch<React.SetStateAction<Pokemon>>,
    selectPokemon2: React.Dispatch<React.SetStateAction<Pokemon>>
}

function PokemonList({ selectPokemon , selectPokemon2}: props) {
    const {pokemons, setPokemons} = useContext(PokemonContext)

    const defaultFrom = 1;
    const defualtTo = 20;

    useEffect(() => {
        getPokemons(defaultFrom, defualtTo);
    }, [])

    const fetchPokemon = async (index: number) => {
        const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${index}`);
        const data = await response.json();
        return data;
    }

    const getPokemons = async (from: number, to: number) => {
        const pokemonList: PokeList = [];
        for (let i = from; i <= to; i++) {
            const pokemon = await fetchPokemon(i);
            pokemonList.push(pokemon);
        }

        setPokemons(pokemonList)
    }

    const pokemonsCards = pokemons.map((pokemonObj => {
        return <PokemonCard key={pokemonObj.id} pokemon={pokemonObj} selectPokemon={selectPokemon} selectedPokemon2={selectPokemon2}></PokemonCard>
    }))

    return (
        <div>
            <GetForm getPokemons={getPokemons} defaultFrom={defaultFrom} defaultTo={defualtTo}></GetForm>
            <ul className="pokemon-list">
                {pokemonsCards}
            </ul>
        </div>
    )
}

export default PokemonList