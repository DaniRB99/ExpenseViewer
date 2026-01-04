import { createContext, useState, type Dispatch, type SetStateAction } from "react";
import { defualtPokemon, type PokeList } from "../types/Pokemon";

interface IPokemonContext {
    pokemons: PokeList,
    setPokemons: Dispatch<SetStateAction<PokeList>>
}

const PokemonContext = createContext<IPokemonContext>({
    pokemons: [defualtPokemon],
    setPokemons: () => {}
});

interface props {
    children:React.ReactNode
}

function PokemonProviderWrapper({children}:props) {
    const [pokemons, setPokemons] = useState<PokeList>([defualtPokemon]);

    return (
        <PokemonContext.Provider value={{pokemons, setPokemons}}>
            {children}
        </PokemonContext.Provider>
    )
}

export {PokemonContext, PokemonProviderWrapper}