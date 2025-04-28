'use client';

import { useEffect, useState } from 'react';
import { fetchProducts } from '../api/products';
import ProductCard from '../components/ui/ProductCard';
import { Product } from '../types/products';
import toast from 'react-hot-toast';

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const data = await fetchProducts();
        setProducts(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error('Error loading products:', error);
        toast.error('Failed to load products');
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };
    loadProducts();
  }, []);

  return (
    <div className="container mx-auto py-12 px-4">
      <h1 className="text-3xl font-bold mb-8">Our Scented Candles</h1>
      {loading ? (
        <p>Loading...</p>
      ) : products.length === 0 ? (
        <p>No products available</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
}