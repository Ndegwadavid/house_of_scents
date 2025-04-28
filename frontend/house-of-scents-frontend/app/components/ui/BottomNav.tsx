'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useCartStore } from '../../store/cart';
import { Home, ShoppingBag, User, ShoppingCart } from 'lucide-react';

export default function BottomNav() {
  const [totalItems, setTotalItems] = useState(0);
  const getTotalItems = useCartStore((state) => state.getTotalItems);

  useEffect(() => {
    // Initialize cart and set totalItems on client
    useCartStore.getState().initializeCart().then(() => {
      setTotalItems(getTotalItems());
    });

    // Subscribe to cart changes
    const unsubscribe = useCartStore.subscribe((state) => {
      setTotalItems(state.getTotalItems());
    });

    return () => unsubscribe();
  }, [getTotalItems]);

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white shadow-md md:hidden z-50">
      <div className="flex justify-around py-2">
        <Link href="/" className="flex flex-col items-center text-gray-600 hover:text-purple-600">
          <Home className="w-6 h-6" />
          <span className="text-xs">Home</span>
        </Link>
        <Link href="/products" className="flex flex-col items-center text-gray-600 hover:text-purple-600">
          <ShoppingBag className="w-6 h-6" />
          <span className="text-xs">Products</span>
        </Link>
        <Link href="/cart" className="flex flex-col items-center text-gray-600 hover:text-purple-600 relative">
          <ShoppingCart className="w-6 h-6" />
          {totalItems > 0 && (
            <span className="absolute top-0 right-0 bg-purple-600 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
              {totalItems}
            </span>
          )}
          <span className="text-xs">Cart</span>
        </Link>
        <Link href="/profile" className="flex flex-col items-center text-gray-600 hover:text-purple-600">
          <User className="w-6 h-6" />
          <span className="text-xs">Profile</span>
        </Link>
      </div>
    </nav>
  );
}