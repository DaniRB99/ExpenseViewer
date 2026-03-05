import { useEffect, useState, type ChangeEvent, type ChangeEventHandler, type FormEvent } from "react"
import "./Categories.css"
import CategoryForm from "./CategoryForm";

//TODO: onClick del button -> form de nueva categoría (incluido en el UL)
//TODO: envío del form -> envío al back y crear nuevo LI
//          Para ello los elementos LI tienen que ser una lista renderizada
//          


function Categories() {
    const [newCategory, setNewCategory] = useState<String>("");
    const [categories, setCategories] = useState<String[]>([]);
    const [showForm, setShowForm] = useState<boolean>(false);

    const toggleForm = () => {
        setShowForm(!showForm)
    }

    const categories_li = categories.map((category) => {
        return (<li className="category-element">{category}</li>)
    });

    useEffect(() => {
        const defualtCategories = [
            "Necesarios",
            "Comida",
            "Restaurante",
            "Caprichos",
            "Almuerzos",
            "Psicólogo"
        ];
        setCategories(defualtCategories);
    }, [])



    const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("Buena categoría ahí " + newCategory);
        //TODO: llamada al back con el POST y generar nueva línea
        //TODO: los <li> tienen que ser una lista renderizada
        
        const newCategories = categories;
        newCategories.push(newCategory);
        setCategories(newCategories);

        toggleForm();
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
                    {categories_li}
                    {showForm && CategoryForm({ handleNewCategory, handleSubmit })}

                    <button className="add" onClick={toggleForm}>➕</button>
                </ul>
            </div>
        </>
    )
}

export default Categories