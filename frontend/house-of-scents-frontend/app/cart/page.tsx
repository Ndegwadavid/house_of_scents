'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { getCart, updateCartItem, removeFromCart, applyCoupon } from '../api/cart';
import { useCartStore } from '../store/cart';
import toast from 'react-hot-toast';
import { CartResponse } from '../types/cart';
import { Minus, Plus, Trash2, Tag, ArrowRight } from 'lucide-react';

export default function CartPage() {
  const [cart, setCart] = useState<CartResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [couponCode, setCouponCode] = useState('');
  const [deliveryMode, setDeliveryMode] = useState<'pickup' | 'delivery'>('delivery');
  const { items, updateQuantity, removeItem } = useCartStore();
  const router = useRouter();

  useEffect(() => {
    const loadCart = async () => {
      try {
        const data = await getCart();
        setCart(data);
      } catch (error) {
        console.error('Error loading cart:', error);
        toast.error('Failed to load cart');
        setCart({ items: [], total_price: 0 });
      } finally {
        setLoading(false);
      }
    };
    loadCart();
  }, []);

  const handleUpdateQuantity = async (productId: number, quantity: number) => {
    if (quantity < 1 || quantity > 100) return;
    try {
      const updatedCart = await updateCartItem(productId, quantity);
      setCart(updatedCart);
      updateQuantity(productId, quantity);
      toast.success('Cart updated');
    } catch (error) {
      console.error('Error updating quantity:', error);
      toast.error('Failed to update cart');
    }
  };

  const handleRemoveItem = async (productId: number) => {
    try {
      const updatedCart = await removeFromCart(productId);
      setCart(updatedCart);
      removeItem(productId);
      toast.success('Item removed from cart');
    } catch (error) {
      console.error('Error removing item:', error);
      toast.error('Failed to remove item');
    }
  };

  const handleApplyCoupon = async () => {
    if (!couponCode) {
      toast.error('Please enter a coupon code');
      return;
    }
    try {
      const response = await applyCoupon({ code: couponCode });
      setCart(response);
      toast.success('Coupon applied successfully');
      setCouponCode('');
    } catch (error) {
      console.error('Error applying coupon:', error);
      toast.error('Invalid or expired coupon');
    }
  };

  const handleCheckout = () => {
    router.push('/checkout');
  };

  if (loading) return <div className="container mx-auto p-4">Loading...</div>;
  if (!cart || !cart.items || cart.items.length === 0) {
    return (
      <div className="container mx-auto p-4 text-center">
        <h2 className="text-2xl font-semibold mb-4">Your Cart is Empty</h2>
        <button
          onClick={() => router.push('/products')}
          className="bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700"
        >
          Shop Now
        </button>
      </div>
    );
  }

  const subtotal = cart.items.reduce(
    (sum, item) => sum + item.product.final_price * item.quantity,
    0
  );
  const discount = subtotal - cart.total_price; // Assuming total_price reflects coupon
  const deliveryCost = deliveryMode === 'delivery' ? 200 : 0; // Example delivery cost
  const total = cart.total_price + deliveryCost;

  return (
    <div className="container mx-auto py-12 px-4">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Your Cart</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          {cart.items.map((item) => (
            <div key={item.id} className="flex items-center border-b py-4">
              <Image
                src={item.product.photo || '/assets/placeholder.jpg'}
                alt={item.product.name}
                width={80}
                height={80}
                className="w-20 h-20 object-cover rounded"
              />
              <div className="flex-1 ml-4">
                <h3 className="text-lg font-semibold text-gray-800">{item.product.name}</h3>
                <p className="text-gray-600">KES {item.product.final_price}</p>
                <div className="flex items-center mt-2 space-x-2">
                  <button
                    onClick={() => handleUpdateQuantity(item.product.id, item.quantity - 1)}
                    className="bg-gray-200 text-gray-700 p-1 rounded hover:bg-gray-300"
                    disabled={item.quantity <= 1}
                  >
                    <Minus className="w-5 h-5" />
                  </button>
                  <span className="mx-2 text-gray-700">{item.quantity}</span>
                  <button
                    onClick={() => handleUpdateQuantity(item.product.id, item.quantity + 1)}
                    className="bg-gray-200 text-gray-700 p-1 rounded hover:bg-gray-300"
                    disabled={item.quantity >= item.product.stock}
                  >
                    <Plus className="w-5 h-5" />
                  </button>
                </div>
              </div>
              <div className="text-right">
                <p className="text-gray-800 font-semibold">
                  KES {item.product.final_price * item.quantity}
                </p>
                <button
                  onClick={() => handleRemoveItem(item.product.id)}
                  className="text-red-600 hover:text-red-800 mt-2"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
        </div>
        <div className="lg:col-span-1">
          <div className="bg-white shadow-md rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Order Summary</h2>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Subtotal</span>
                <span className="text-gray-800">KES {subtotal}</span>
              </div>
              {discount > 0 && (
                <div className="flex justify-between text-green-600">
                  <span>Discount</span>
                  <span>-KES {discount}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-gray-600">Delivery ({deliveryMode})</span>
                <span className="text-gray-800">KES {deliveryCost}</span>
              </div>
              <div className="flex justify-between font-bold text-gray-800">
                <span>Total</span>
                <span>KES {total}</span>
              </div>
            </div>
            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-600">Delivery Mode</label>
              <select
                value={deliveryMode}
                onChange={(e) => setDeliveryMode(e.target.value as 'pickup' | 'delivery')}
                className="w-full p-2 border rounded focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="delivery">Delivery (KES 200)</option>
                <option value="pickup">Pickup (Free)</option>
              </select>
            </div>
            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-600">Coupon Code</label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={couponCode}
                  onChange={(e) => setCouponCode(e.target.value)}
                  className="w-full p-2 border rounded focus:ring-purple-500 focus:border-purple-500"
                  placeholder="Enter coupon code"
                />
                <button
                  onClick={handleApplyCoupon}
                  className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 flex items-center"
                >
                  <Tag className="w-5 h-5 mr-2" />
                  Apply
                </button>
              </div>
            </div>
            <button
              onClick={handleCheckout}
              className="mt-6 w-full bg-purple-600 text-white py-3 rounded hover:bg-purple-700 flex items-center justify-center"
            >
              Proceed to Checkout
              <ArrowRight className="w-5 h-5 ml-2" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}