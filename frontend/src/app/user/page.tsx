'use client';

import { useEffect, useState } from 'react';

type Item = {
  id: number;
  title: string;
  brand: string;
  price: number;
  quantity: number;
};

export default function UserPage() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchId, setSearchId] = useState('');
  const [searchResult, setSearchResult] = useState<Item | null>(null);
  const [searchError, setSearchError] = useState('');

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

  const handleBuy = async (item: Item) => {
    if (item.quantity > 0) {
      try {
        const response = await fetch(`http://localhost:8000/users/purchase/customer?admin=false`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: item.id,  // Make sure `item.id` is sent
            quantity: 1
          }),
        });
        
        if (response.ok) {
          const data = await response.json();
          alert(data.message);
        } else {
          const errorData = await response.json();
          alert(`Error: ${errorData.detail}`);
        }

        await fetchItems();
      } catch (error) {
        alert(`An error occurred: ${error}`);
      }
    } else {
      alert(`Sorry, ${item.title} is out of stock.`);
    }
  };

  return (
    <main className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">User - Vending Machine</h1>

      {/* 🔍 Search Section */}
      <div className="mb-6">
        <label className="block mb-2 font-semibold">Search Item by ID</label>
        <div className="flex gap-2">
          <input
            type="number"
            placeholder="Enter Item ID"
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            className="border px-3 py-1 rounded w-40"
          />
          <button
            onClick={handleSearch}
            type='submit'
            className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
          >
            Search
          </button>
        </div>

        {searchError && <p className="text-red-500 mt-2">{searchError}</p>}

        {searchResult && (
          <div className="mt-4 p-4 border rounded bg-green-700 text-white">
            <h2 className="text-xl font-semibold mb-1">{searchResult.title}</h2>
            <p className="mb-1">Brand: {searchResult.brand}</p>
            <p className="mb-1">Price: ${searchResult.price.toFixed(2)}</p>
            <p className="mb-1">Quantity: {searchResult.quantity}</p>
            <button
              onClick={() => handleBuy(searchResult)}
              className={`mt-2 px-4 py-1 rounded ${
                searchResult.quantity > 0 ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 cursor-not-allowed'
              } text-white`}
              disabled={searchResult.quantity === 0}
            >
              {searchResult.quantity > 0 ? 'Buy' : 'Out of Stock'}
            </button>
          </div>
        )}
      </div>

      {/* Item List Section */}
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
                onClick={() => handleBuy(item)}
                className={`mt-2 ml-2 px-4 py-1 rounded ${
                  item.quantity > 0 ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-600 cursor-not-allowed'
                } text-white`}
                disabled={item.quantity === 0}
              >
                {item.quantity > 0 ? 'Buy' : 'Out of Stock'}
              </button>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}