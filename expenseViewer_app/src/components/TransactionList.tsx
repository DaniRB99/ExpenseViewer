import { useContext, useEffect, useState } from "react"
import "./TransactionList.css";
import { TransactionContext, type TransactionContextType } from "../context/TransactionContexts";

function TransactionList() {
    const spentClass = "spent-amount";
    const incomeClass = "income-amount";

    const getTransacClass = (amount: string) => {
        let amount_double: number = Number(amount.substring(0, amount.length - 2))
        console.log(amount.substring(0, amount.length - 2))
        if (amount_double > 0)
            return incomeClass;
        else
            return spentClass
    }

    const transaction_context: TransactionContextType = useContext(TransactionContext)

    const transactions_li = transaction_context.transactions.map((transac) => {
        return <li key={transac._id} className="transac-card">
            <p className={getTransacClass(transac.amount) + " text"}>{transac.amount}</p>
            <p className="text">{transac.description}</p>
            <p className="text">Ref: {transac.reference}</p>
            <p className="text">{transac.transac_date}</p>
        </li>
    });

    return (<ul className="transac-list">
        {transactions_li}
    </ul>)
}

export default TransactionList