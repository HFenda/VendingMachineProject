'use client';

import { useEffect, useState } from 'react';

type Item = {
  id: number;
  title: string;
  brand: string;
  price: number;
  quantity: number;
};

export default function HomePage() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);

  const [searchId, setSearchId] = useState('');
  const [searchResult, setSearchResult] = useState<Item | null>(null);
  const [searchError, setSearchError] = useState('');

  // Form for adding and updating an item
  const [newItem, setNewItem] = useState<Item>({
    id: 0,
    title: '',
    brand: '',
    price: 0,
    quantity: 0,
  });
  const [addItemError, setAddItemError] = useState('');
  const [addItemSuccess, setAddItemSuccess] = useState('');

  // Handle fetching items
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

  // Handle search item by ID
  const handleSearch = async () => {
    setSearchResult(null);
    setSearchError('');
    try {
      const res = await fetch(`http://localhost:8000/items/${searchId}`);
      if (!res.ok) {
        throw new Error('Item not found');
      }
      const data = await res.json();
      setSearchResult(data);
    } catch (error) {
      setSearchError('Item not found or invalid ID.');
    }
  };

  // Handle add new item
  const handleAddItem = async () => {
    setAddItemError('');
    setAddItemSuccess('');
    try {
      const res = await fetch('http://localhost:8000/items/add-item', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: newItem.title,
          brand: newItem.brand,
          price: newItem.price,
          quantity: newItem.quantity,
        }),
      });
      if (!res.ok) {
        throw new Error('Failed to add item.');
      }
      const added = await res.json();
      setItems([...items, added]);
      setNewItem({ id: 0, title: '', brand: '', price: 0, quantity: 0 });
      setAddItemSuccess('Item added successfully!');
    } catch (err) {
      setAddItemError('Error adding item. Please check the fields and try again.');
    }
  };

  // Handle update item
  const handleUpdateItem = async (updatedItem: Item) => {
    try {
      const res = await fetch(`http://localhost:8000/items/update-item/${updatedItem.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedItem),
      });
  
      if (!res.ok) {
        throw new Error('Failed to update item.');
      }
  
      const updated = await res.json();
  
      // Update the local state with the updated item
      setItems((prevItems) =>
        prevItems.map((item) =>
          item.id === updated.id ? { ...item, ...updated } : item
        )
      );
  
      // Reload the page after a successful update
      window.location.reload();
    } catch (err) {
      console.error('Error updating item:', err);
    }
  };

  // Handle delete item
  const handleDeleteItem = async (id: number) => {
    try {
      const res = await fetch(`http://localhost:8000/items/delete-item/${id}`, {
        method: 'DELETE',
      });
  
      if (!res.ok) {
        throw new Error('Failed to delete item.');
      }
  
      // Remove the deleted item from the state
      setItems((prevItems) => prevItems.filter((item) => item.id !== id));
    } catch (err) {
      console.error('Error deleting item:', err);
    }
  };

  return (
    <main className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Vending Machine</h1>

      {/* 🔍 Search section */}
      <div className="mb-6">
        <label className="block mb-2 font-semibold">Search Item by ID</label>
        <div className="flex gap-2">
          <input
            type="number"
            placeholder="Enter ID"
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            className="border px-3 py-1 rounded w-40"
          />
          <button
            onClick={handleSearch}
            className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
          >
            Search
          </button>
        </div>

        {searchError && <p className="text-red-500 mt-2">{searchError}</p>}

        {searchResult && (
          <div className="mt-4 p-4 border rounded bg-green-700">
            <h2 className="text-xl font-semibold mb-1">{searchResult.title}</h2>
            <p className="mb-1">Brand: {searchResult.brand}</p>
            <p className="mb-1">Price: ${searchResult.price}</p>
            <p className="mb-1">Quantity: {searchResult.quantity}</p>
          </div>
        )}
      </div>

      {/* ➕ Add/Update new item section */}
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
        {addItemError && <p className="text-red-500 mt-2">{addItemError}</p>}
        {addItemSuccess && <p className="text-green-600 mt-2">{addItemSuccess}</p>}
      </div>

      {/* 🧾 Item list */}
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {items.map((item) => (
            <div key={item.id} className="p-4 border rounded-xl shadow-md bg-white">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">{item.title}</h2>
              <p className="text-gray-600 mb-1"><span className="font-medium">Brand:</span> {item.brand}</p>
              <p className="text-gray-600 mb-1"><span className="font-medium">Price:</span> ${item.price ? item.price.toFixed(2) : 'N/A'}</p>
              <p className={`text-sm font-semibold mt-2 ${item.quantity > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {item.quantity > 0 ? `In Stock (${item.quantity})` : 'Out of Stock'}
              </p>
              <button
                className="mt-2 bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 disabled:bg-gray-300"
                disabled={item.quantity === 0}
              >
                {item.quantity === 0 ? 'Sold Out' : 'Buy'}
              </button>
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
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
