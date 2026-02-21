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

export interface Transaction {
    _id: string,
    account:string,
    balance: string,
    amount: string,
    transac_date:string,
    concept: string,
    reference:string,
    issuer:string,
    dest:string,
    description:string
};

export type TransacList = Transaction[];

export const defaultTransaction:Transaction = {
    _id: "-1",
    account:"2100 0000 00 0000000000",
    balance: "1.005.000,00 €",
    amount: "5.000,00 €",
    transac_date: "01/05/2024",
    concept:"ABONARES - ENTREGAS - INGRESOS (TRANSFERENCIA)",
    reference:"000000000000",
    issuer:"Pedrito",
    dest:"Amancio Ortega",
    description: "Cheques varios"
}