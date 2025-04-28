'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { verifyEmail } from '../../api/auth';
import toast from 'react-hot-toast';

export default function VerifyEmailPage() {
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  useEffect(() => {
    if (!token) {
      setMessage('Invalid verification token');
      setLoading(false);
      return;
    }

    const verify = async () => {
      try {
        const response = await verifyEmail(token);
        setMessage(response.message);
        toast.success('Email verified successfully');
        setTimeout(() => router.push('/auth/login'), 2000);
      } catch (error: any) {
        setMessage(error.response?.data?.detail || 'Verification failed');
        toast.error('Verification failed');
      } finally {
        setLoading(false);
      }
    };

    verify();
  }, [token, router]);

  return (
    <div className="container mx-auto p-4 max-w-md text-center">
      <h1 className="text-2xl font-bold mb-4">Email Verification</h1>
      {loading ? (
        <p>Verifying your email...</p>
      ) : (
        <p>{message}</p>
      )}
    </div>
  );
}