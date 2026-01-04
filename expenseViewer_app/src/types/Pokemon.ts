export interface Pokemon {
    id: number,
    name: string,
    sprites: { front_default: string },
    stats: [{ base_stat: number, effort: number }]
};

export type PokeList = Pokemon[];

export const defualtPokemon:Pokemon = {
    id: -1,
    name: " ",
    sprites: { front_default: " " },
    stats: [{ base_stat: 0, effort: 0}]
}
