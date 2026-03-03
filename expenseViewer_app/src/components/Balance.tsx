import { useContext, useEffect, useState } from "react"
import "./Balance.css"
import { TransactionContext, type TransactionContextType } from "../context/TransactionContexts"

function Balance() {
    const [balance, setBalance] = useState("0000,00€")
    const transac_context:TransactionContextType = useContext(TransactionContext)

    const fetchBalance = async () => {
        const response = await fetch("http://localhost:8000/api/v1/balance");
        const data = await response.json();
        console.log(data)
        setBalance(transac_context.toMoneyFormat(data.money, data.currency));
    }

    useEffect(() => {
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