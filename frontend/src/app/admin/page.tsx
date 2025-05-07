'use client';

import { useEffect, useState } from 'react';

type Item = {
    id: number;
    title: string;
    brand: string;
    price: number;
    quantity: number;
  };

export default function AdminPage() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [newItem, setNewItem] = useState<Item>({
    id: 0,
    title: '',
    brand: '',
    price: 0,
    quantity: 0,
  });
  const [addItemError, setAddItemError] = useState('');
  const [addItemSuccess, setAddItemSuccess] = useState('');
  const [updateItemError, setUpdateItemError] = useState('');
  const [updateItemSuccess, setUpdateItemSuccess] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/items/all-items')
      .then((res) => res.json())
      .then((data) => {
        setItems(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching items:', err);
        setLoading(false);
      });
  }, []);

  const fetchItems = async () => {
    try {
      setLoading(true);
      const res = await fetch('http://localhost:8000/items/all-items');
      const data = await res.json();
      setItems(data);
    } catch (err) {
      console.error('Error fetching items:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddItem = async () => {
    // Clear everything else first
    setAddItemError('');
    setAddItemSuccess('');
    setUpdateItemError('');
    setUpdateItemSuccess('');
  
    try {
      const res = await fetch('http://localhost:8000/items/add-item', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newItem),
      });
      if (!res.ok) {
        throw new Error('Failed to add item.');
      }
      const added = await res.json();
      setItems([...items, added]);
      setNewItem({ id: 0, title: '', brand: '', price: 0, quantity: 0 });
      setAddItemSuccess('Item added successfully!');
    } catch (err) {
      setAddItemError(`${err} Please check the fields and try again.`);
    }
  };
  
  const handleUpdateItem = async (updatedItem: Item) => {
    setUpdateItemError('');
    setUpdateItemSuccess('');
    setAddItemError('');
    setAddItemSuccess('');
  
    try {
      const res = await fetch(`http://localhost:8000/items/update-item/${updatedItem.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedItem),
      });
      if (!res.ok) {
        const errorDetails = await res.json();
        throw new Error(`Failed to update item.`);
      }
      const updated = await res.json();
      setItems((prevItems) =>
        prevItems.map((item) => (item.id === updated.id ? { ...item, ...updated } : item))
      );
      setNewItem({ id: 0, title: '', brand: '', price: 0, quantity: 0 });
      setUpdateItemSuccess('Item updated successfully!');
      await fetchItems();
    } catch (err) {
      setUpdateItemError(`${err} Please try again.`);
    }
  };

  const handleDeleteItem = async (id: number) => {
    try {
      const res = await fetch(`http://localhost:8000/items/delete-item/${id}`, {
        method: 'DELETE',
      });
      if (!res.ok) {
        throw new Error('Failed to delete item.');
      }
      setItems((prevItems) => prevItems.filter((item) => item.id !== id));
    } catch (err) {
      console.error(`Error deleting item.`);
    }
  };

  const handleViewRevenue = async (brand: string) => {
    try {
      const res = await fetch(`http://localhost:8000/users/total-revenue/${brand}?admin=true`);
      if (!res.ok) {
        throw new Error('Failed to fetch revenue.');
      }
      const data = await res.json();
      alert(data.message);
    } catch (err) {
      alert(`${err} Error fetching revenue.`);
    }
  };

  const handleResetForm = () => {
    setNewItem({
      id: 0,
      title: '',
      brand: '',
      price: 0,
      quantity: 0,
    });
    setUpdateItemError('');
    setUpdateItemSuccess('');
    setAddItemError('');
    setAddItemSuccess('');
  };

  return (
    <main className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Admin - Vending Machine</h1>

      {/* Add/Update Item */}
      <div className="mb-10 mt-6">
        <h2 className="text-2xl font-bold mb-4">Add/Update Item</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Title"
            value={newItem.title}
            onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
            className="border px-3 py-2 rounded"
          />
          <input
            type="text"
            placeholder="Brand"
            value={newItem.brand}
            onChange={(e) => setNewItem({ ...newItem, brand: e.target.value })}
            className="border px-3 py-2 rounded"
          />
          <input
            type="number"
            step="0.01"
            placeholder="Price"
            value={newItem.price}
            onChange={(e) => setNewItem({ ...newItem, price: parseFloat(e.target.value) })}
            className="border px-3 py-2 rounded"
          />
          <input
            type="number"
            placeholder="Quantity"
            value={newItem.quantity}
            onChange={(e) => setNewItem({ ...newItem, quantity: parseInt(e.target.value) })}
            className="border px-3 py-2 rounded"
          />
        </div>
        <button
          onClick={newItem.id > 0 ? () => handleUpdateItem(newItem) : handleAddItem}
          className="mt-4 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          {newItem.id ? 'Update Item' : 'Add Item'}
        </button>
        {newItem.id > 0 && (
          <button
            onClick={handleResetForm}
            className="mt-4 ml-2 bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          >
            Cancel
          </button>
        )}

        {/* Add Item Messages */}
        {addItemError && <p className="text-red-500 mt-2">{addItemError}</p>}
        {addItemSuccess && <p className="text-green-600 mt-2">{addItemSuccess}</p>}

        {/* Update Item Messages */}
        {updateItemError && <p className="text-red-500 mt-2">{updateItemError}</p>}
        {updateItemSuccess && <p className="text-green-600 mt-2">{updateItemSuccess}</p>}
      </div>

      {/* Item List */}
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {items.map((item) => (
            <div key={item.id} className="p-4 border rounded-xl shadow-md bg-white">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">{item.title}</h2>
              <p className="text-gray-600 mb-1"><span className="font-medium">Brand:</span> {item.brand}</p>
              <p className="text-gray-600 mb-1"><span className="font-medium">Price:</span> ${item.price.toFixed(2)}</p>
              <p className={`text-sm font-semibold mt-2 ${item.quantity > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {item.quantity > 0 ? `In Stock (${item.quantity})` : 'Out of Stock'}
              </p>
              <button
                onClick={() => handleDeleteItem(item.id)}
                className="mt-2 ml-2 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
              >
                Delete
              </button>
              <button
                onClick={() => setNewItem(item)}
                className="mt-2 ml-2 bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600"
              >
                Edit
              </button>
              <button
                onClick={() => handleViewRevenue(item.brand)}
                className="mt-2 ml-2 bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
              >
                See Revenue
              </button>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}