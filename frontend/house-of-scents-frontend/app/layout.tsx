'use client';

import { useEffect } from 'react';
import { Poppins } from 'next/font/google';
import './globals.css';
import { ToastProvider } from './components/ui/ToastProvider';
import { AuthProvider } from './auth/AuthContext';
import Navbar from './components/ui/Navbar';
import Sidebar from './components/ui/Sidebar';
import BottomNav from './components/ui/BottomNav';
import { useCartStore } from './store/cart';

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-poppins',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const { initializeCart } = useCartStore();

  useEffect(() => {
    initializeCart();
  }, [initializeCart]);

  return (
    <html lang="en">
      <body className={`${poppins.variable} bg-gray-50 font-poppins`}>
        <AuthProvider>
          <ToastProvider>
            <Navbar />
            <div className="flex">
              <Sidebar />
              <main className="flex-1 p-4 md:p-6 lg:p-8 pb-16 md:pb-8">
                {children}
              </main>
            </div>
            <BottomNav />
          </ToastProvider>
        </AuthProvider>
      </body>
    </html>
  );
}