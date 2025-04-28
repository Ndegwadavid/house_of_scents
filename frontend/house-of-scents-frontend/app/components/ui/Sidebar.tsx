'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '../../auth/AuthContext';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';

export default function Sidebar() {
  const { user, isAuthenticated, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/auth/login');
    } catch (error) {
      toast.error('Logout failed');
    }
  };

  const toggleSidebar = () => setIsOpen(!isOpen);

  return (
    <>
      <button
        className="md:hidden fixed top-4 left-4 z-50"
        onClick={toggleSidebar}
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d={isOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16m-7 6h7'}
          />
        </svg>
      </button>
      <aside
        className={`fixed md:static top-0 left-0 h-full bg-white shadow-md w-64 transform transition-transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } md:translate-x-0 z-40`}
      >
        <div className="p-4">
          <Link href="/" onClick={() => setIsOpen(false)}>
            <img
              src="/assets/logo.png"
              alt="House of Scents Logo"
              className="h-10 w-auto"
            />
          </Link>
        </div>
        <nav className="mt-4">
          <Link
            href="/products"
            className="block py-2 px-4 text-gray-700 hover:bg-blue-100"
            onClick={() => setIsOpen(false)}
          >
            Products
          </Link>
          <Link
            href="/cart"
            className="block py-2 px-4 text-gray-700 hover:bg-blue-100"
            onClick={() => setIsOpen(false)}
          >
            Cart
          </Link>
          <Link
            href="/orders"
            className="block py-2 px-4 text-gray-700 hover:bg-blue-100"
            onClick={() => setIsOpen(false)}
          >
            Orders
          </Link>
          {isAuthenticated ? (
            <>
              <Link
                href="/profile"
                className="block py-2 px-4 text-gray-700 hover:bg-blue-100"
                onClick={() => setIsOpen(false)}
              >
                Profile
              </Link>
              <button
                onClick={handleLogout}
                className="block w-full text-left py-2 px-4 text-gray-700 hover:bg-blue-100"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/auth/login"
                className="block py-2 px-4 text-gray-700 hover:bg-blue-100"
                onClick={() => setIsOpen(false)}
              >
                Login
              </Link>
              <Link
                href="/auth/register"
                className="block py-2 px-4 text-gray-700 hover:bg-blue-100"
                onClick={() => setIsOpen(false)}
              >
                Register
              </Link>
            </>
          )}
        </nav>
      </aside>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 md:hidden z-30"
          onClick={toggleSidebar}
        />
      )}
    </>
  );
}