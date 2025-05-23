'use client';

import { Toaster } from 'react-hot-toast';

export const ToastProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <Toaster position="top-right" />
      {children}
    </>
  );
};