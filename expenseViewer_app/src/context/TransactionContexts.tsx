import { createContext, useEffect, useState } from "react";

export interface Transaction {
    _id: string,
    account: string,
    balance: number,
    amount: number,
    currency:string,
    transac_date: string,
    concept: string,
    reference: string,
    issuer: string,
    dest: string,
    description: string
};

const defaultTransaction1: Transaction = {
    _id: "-1",
    account: "2100 0000 00 0000000000",
    balance: 1005000.00,
    amount: 5000.00,
    currency:"EUR",
    transac_date: "01/05/2024",
    concept: "ABONARES - ENTREGAS - INGRESOS (TRANSFERENCIA)",
    reference: "000000000000",
    issuer: "Pedrito",
    dest: "Amancio Ortega",
    description: "Cheques varios"
}

const defaultTransaction2: Transaction = {
    _id: "-2",
    account: "2100 0000 00 0000000000",
    balance: 1004900.00,
    amount: -100.00,
    currency:"EUR",
    transac_date: "05/05/2024",
    concept: "ABONARES - ENTREGAS - INGRESOS (TRANSFERENCIA)",
    reference: "000000000000",
    issuer: "Amancio Ortega",
    dest: "Heladería Jijonenca",
    description: "Horchata"
}

const defaultTransaction3: Transaction = {
    _id: "-3",
    account: "2100 0000 00 0000000000",
    balance: 100400000,
    amount: -90000,
    currency:"EUR",
    transac_date: "10/05/2024",
    concept: "ABONARES - ENTREGAS - INGRESOS (TRANSFERENCIA)",
    reference: "000000000000",
    issuer: "Amancio Ortega",
    dest: "Pepe",
    description: "Donación"
}

export interface TransactionContextType {
    transactions: Transaction[],
    addTransac: (transac: Transaction) => void,
    updateTransac: (transac: Transaction) => void,
    deleteTransac: (id: string) => Transaction | null,
    toMoneyFormat: (amount:number, currency:string) => string
}

const defaultTransacContext = {
    transactions: [],
    addTransac: () => null,
    updateTransac: () => null,
    deleteTransac: () => null,
    toMoneyFormat: () => ""
}

export const TransactionContext = createContext<TransactionContextType>(defaultTransacContext);

interface Props {
    children: React.ReactNode
}

export function TransactionProviderWrapper(props: Props) {
    const [transactions, setTransacs] = useState<Transaction[]>([])

    const fetchTransac = async () => {
        const response = await fetch("http://localhost:8000/api/v1/get_last_transacs");
        const data = await response.json();
        console.log(data[0])
        console.log(typeof(data[0].transac_date))
        setTransacs(data)
    }

    useEffect(() => {
        fetchTransac();
        // setTransacs(
        //     [defaultTransaction1, defaultTransaction2, defaultTransaction3]
        // )
    }, [])

    const addTransac = (transac: Transaction) => null;
    const updateTransac = (transac: Transaction) => null;
    const deleteTransac = (id: string) => null;

    const toMoneyFormat = (amount: number, currency:string) => {
        return new Intl.NumberFormat("es-ES", {
            style:"currency",
            currency: currency,
            currencySign:"accounting"
        }).format(amount)
    } 

    return (
        <TransactionContext.Provider value={{ transactions, addTransac, updateTransac, deleteTransac, toMoneyFormat}}>
            {props.children}
        </TransactionContext.Provider>
    )
}

