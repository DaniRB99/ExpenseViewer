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

interface Props {
    children:React.ReactNode
}

function PokemonProviderWrapper(props:Props) {
    const [pokemons, setPokemons] = useState<PokeList>([defualtPokemon]);

    return (
        <PokemonContext.Provider value={{pokemons, setPokemons}}>
            {props.children}
        </PokemonContext.Provider>
    )
}

export {PokemonContext, PokemonProviderWrapper}