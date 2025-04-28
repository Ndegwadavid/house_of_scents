'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useCartStore } from '../../store/cart';
import { Menu, X, ShoppingBag, Home, User } from 'lucide-react';

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
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
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/">
          <Image
            src="/assets/logo.png"
            alt="House of Scents"
            width={120}
            height={40}
            className="h-10 w-auto"
          />
        </Link>
        <div className="hidden md:flex space-x-6">
          <Link href="/" className="text-gray-600 hover:text-purple-600">
            Home
          </Link>
          <Link href="/products" className="text-gray-600 hover:text-purple-600">
            Products
          </Link>
          <Link href="/cart" className="text-gray-600 hover:text-purple-600 relative">
            Cart
            {totalItems > 0 && (
              <span className="absolute -top-2 -right-2 bg-purple-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {totalItems}
              </span>
            )}
          </Link>
          <Link href="/profile" className="text-gray-600 hover:text-purple-600">
            Profile
          </Link>
        </div>
        <div className="md:hidden">
          <button onClick={() => setIsMenuOpen(!isMenuOpen)}>
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>
      {isMenuOpen && (
        <div className="md:hidden bg-white border-t">
          <Link
            href="/"
            className="block px-4 py-2 text-gray-600 hover:bg-purple-100"
            onClick={() => setIsMenuOpen(false)}
          >
            <Home className="w-5 h-5 inline mr-2" /> Home
          </Link>
          <Link
            href="/products"
            className="block px-4 py-2 text-gray-600 hover:bg-purple-100"
            onClick={() => setIsMenuOpen(false)}
          >
            <ShoppingBag className="w-5 h-5 inline mr-2" /> Products
          </Link>
          <Link
            href="/cart"
            className="block px-4 py-2 text-gray-600 hover:bg-purple-100 relative"
            onClick={() => setIsMenuOpen(false)}
          >
            <ShoppingBag className="w-5 h-5 inline mr-2" /> Cart
            {totalItems > 0 && (
              <span className="absolute top-2 right-4 bg-purple-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {totalItems}
              </span>
            )}
          </Link>
          <Link
            href="/profile"
            className="block px-4 py-2 text-gray-600 hover:bg-purple-100"
            onClick={() => setIsMenuOpen(false)}
          >
            <User className="w-5 h-5 inline mr-2" /> Profile
          </Link>
        </div>
      )}
    </nav>
  );
}