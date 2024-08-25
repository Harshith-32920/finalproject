import React, { useState, useEffect } from "react";
import axios from "axios";
import Card from "../components/card";

function CRUD() {
    const [items, setItems] = useState([]);
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    // const [Duedate, setDuedate] = useState("");
    const [editId, setEditId] = useState(null);

    const createItem = async () => {
        await axios.post("http://127.0.0.1:8000/items/", {
            title,
            description,
            // Duedate
        });
        setTitle("");
        setDescription("");
        // setDuedate("");
        fetchItems();
    };

    const fetchItems = async () => {
        const response = await axios.get("http://127.0.0.1:8000/items/");
        setItems(response.data);
    };

    const updateItem = async () => {
        await axios.put(`http://127.0.0.1:8000/items/${editId}`, {
            title,
            description,
            // Duedate
        });
        setTitle("");
        setDescription("");
        // setDuedate("");
        setEditId(null);
        fetchItems();
    };

    const deleteItem = async (id) => {
        await axios.delete(`http://127.0.0.1:8000/items/${id}`);
        fetchItems();
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (editId) {
            updateItem();
        } else {
            createItem();
        }
    };

    useEffect(() => {
        fetchItems();
    }, []);

    return (
        <div className="crud-container">
            <h1>TASK MANAGER</h1>
            <form onSubmit={handleSubmit} className="crud-form">
                <input
                    type="text"
                    placeholder="Task"
                    className="crud-input"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Description"
                    className="crud-input"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                {/* <input
                    type="date"
                    placeholder="Due Date"
                    className="crud-input"
                    value={Duedate}
                    onChange={(e) => setDuedate(e.target.value)}
                /> */}
                
                <button type="submit" className="crud-button">
                    {editId ? "Update" : "New Task"}
                </button>
            </form>
             <ul className="crud-list">
                {items.map((item) => (
                    <Card
                        key={item.id}
                        item={item}
                        onEdit={() => {
                            setEditId(item.id);
                            setTitle(item.title);
                            setDescription(item.description);
                            // setDuedate(item.Duedate);
                        }}
                        onDelete={() => deleteItem(item.id)}
                    />
                ))}
            </ul>
        </div>
    );
}

export default CRUD;
