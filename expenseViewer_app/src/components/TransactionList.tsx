import { useContext, useEffect, useState } from "react"
import "./TransactionList.css";
import { TransactionContext, type TransactionContextType } from "../context/TransactionContexts";

function TransactionList() {
    const spentClass = "spent-amount";
    const incomeClass = "income-amount";

    const getTransacType = (amount: number):string => {
        return amount > 0 ? incomeClass : spentClass
    }

    const transaction_context: TransactionContextType = useContext(TransactionContext)

    const transactions_li = transaction_context.transactions.map((transac) => {
        return <li key={transac._id} className="transac-card">
            <p className={getTransacType(transac.amount) + " text"}>{transaction_context.toMoneyFormat(transac.amount, transac.currency)}</p>
            <p className="text">{transac.description}</p>
            <p className="text">Ref: {transac.reference}</p>
            <p className="text">{transac.transac_date}</p>
        </li>
    });

    return (<ul className="transac-list">
        <h2 className='subtitle'>Transactions</h2>
        
        {transactions_li}
    </ul>)
}

export default TransactionList