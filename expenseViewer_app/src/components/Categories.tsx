import { useState, type ChangeEvent, type ChangeEventHandler, type FormEvent } from "react"
import "./Categories.css"
import CategoryForm from "./CategoryForm";

//TODO: onClick del button -> form de nueva categoría (incluido en el UL)
//TODO: envío del form -> envío al back y crear nuevo LI
//          Para ello los elementos LI tienen que ser una lista renderizada
//          


function Categories() {
    const [toggleForm, setToggleForm] = useState<boolean>(true);

    const showForm = () => {
        setToggleForm(!toggleForm)
    }

    const [newCategory, setNewCategory] = useState<String>("");

    const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("Buena categoría ahí " + newCategory);

        //TODO: llamada al back con el POST y generar nueva línea
        //TODO: los <li> tienen que ser una lista renderizada

        showForm()
    }

    const handleNewCategory = (e: ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        setNewCategory(e.target.value)
    }

    return (
        <>
            <div className="sub-panel">
                <ul className="category-list">
                    <h2>Categories</h2>

                    <li>Necesarios</li>
                    <li>Comida</li>
                    <li>Restaurante</li>
                    <li>Caprichos</li>
                    <li>Almuerzos</li>
                    <li>Psicólogo</li>
                    {toggleForm && CategoryForm({ handleNewCategory, handleSubmit })}

                    <button className="add" onClick={showForm}>➕</button>
                </ul>
            </div>
        </>
    )
}

export default Categories