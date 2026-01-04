import { useState, type ChangeEvent, type FormEvent} from "react";
import "./GetForm.css";

interface props{
    getPokemons:(from: number, to: number) => Promise<void>,
    defaultFrom:number,
    defaultTo:number
}

function GetForm({getPokemons, defaultFrom, defaultTo}:props) {
    const [from, setFrom] = useState<number>(defaultFrom);
    const [to, setTo] = useState<number>(defaultTo);

    const handleFromInput = (e:ChangeEvent<HTMLInputElement>) => {
        setFrom(Number(e.target.value));
    }

    const handleToInput = (e:ChangeEvent<HTMLInputElement>) => {
        setTo(Number(e.target.value));
    }

    const handleSubmit = (e:FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        getPokemons(from, to)
    }

    return (
        <form className="form-input" onSubmit={handleSubmit}>
            <fieldset>
                <label htmlFor="from-pokemon">From: </label>
                <input type="number" id="from-pokemon" min={1} onChange={handleFromInput} defaultValue={from}/>
            </fieldset>
            <fieldset>
                <label htmlFor="to-pokemon">To: </label>
                <input type="number" id="to-pokemon" min={1} onChange={handleToInput} defaultValue={to} />
            </fieldset>
            <button>Get Pokemons!</button>
        </form>
    )
}

export default GetForm