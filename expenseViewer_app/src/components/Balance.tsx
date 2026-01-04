import { useEffect, useState } from "react"
import "./Balance.css"

function Balance() {
    const [balance, setBalance] = useState("0000,00€")

    const fetchBalance = async () => {
        const response = await fetch("http://localhost:8000/api/v1/balance");
        const data = await response.json();
        console.log(data)
        let divisa_symb = "cacahuetes";
        if(data.divisa == "EUR"){
            divisa_symb = "€"
        }

        setBalance(data.saldo+" "+divisa_symb)
    }

    useEffect(() => {
        // setBalance("3.000,00€")
        fetchBalance();
    }, [])

    return (
        <div className="balance-block">
            <h2>Balance:</h2>
            <h2 className="money">{balance}</h2>
        </div>
    )
}

export default Balance