'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { requestPasswordReset } from '../../api/auth';
import toast from 'react-hot-toast';

export default function PasswordResetPage() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await requestPasswordReset({ email });
      toast.success('Password reset email sent. Check your inbox.');
      router.push('/auth/login');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Request failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-md">
      <h1 className="text-2xl font-bold mb-4">Reset Password</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Sending...' : 'Send Reset Email'}
        </button>
      </form>
      <p className="mt-4">
        Back to{' '}
        <a href="/auth/login" className="text-blue-600 hover:underline">
          Login
        </a>
      </p>
    </div>
  );
}