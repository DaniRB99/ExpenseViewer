import { useState, type ChangeEvent, type FormEvent } from 'react'

interface props {
    handleNewCategory: (e:ChangeEvent<HTMLInputElement>) => void,
    handleSubmit: (e:FormEvent<HTMLFormElement>) => void
}

function CategoryForm({handleNewCategory, handleSubmit}:props) {


    return (
        <>
            <li className='category-element'>
                <form onSubmit={handleSubmit}>
                    <fieldset>
                        <input type="string" onChange={handleNewCategory}></input>
                    </fieldset>
                </form>
            </li>
        </>
    )
    // return (
    //     <li>Buenas tardes</li>
    // )
}

export default CategoryForm