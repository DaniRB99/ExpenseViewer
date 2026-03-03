import "./Categories.css"

function Categories() {
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

                    <button className="add">➕</button>
                </ul>
            </div>
        </>
    )
}

export default Categories