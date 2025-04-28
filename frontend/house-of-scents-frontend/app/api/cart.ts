import api from '../utils/api';
import { CartResponse } from '../types/cart';

export const getCart = async (): Promise<CartResponse> => {
  try {
    console.log('Calling /api/cart/');
    const response = await api.get('/cart/');
    console.log('Cart response:', response.data);
    return {
      items: Array.isArray(response.data?.items) ? response.data.items : [],
      total_price: response.data?.total_price || 0,
    };
  } catch (error: any) {
    console.error('Error fetching cart:', error.response?.status, error.message);
    return { items: [], total_price: 0 };
  }
};

export const addToCart = async (productId: number, quantity: number): Promise<void> => {
  try {
    console.log(`Adding to cart: product ${productId}, quantity ${quantity}`);
    await api.post('/cart/add/', { product_id: productId, quantity });
  } catch (error) {
    console.error('Error adding to cart:', error);
    throw error;
  }
};

export const updateCartItem = async (
  productId: number,
  quantity: number
): Promise<CartResponse> => {
  try {
    console.log(`Updating cart item: product ${productId}, quantity ${quantity}`);
    const response = await api.put(`/cart/update/${productId}/`, { quantity });
    return {
      items: Array.isArray(response.data?.items) ? response.data.items : [],
      total_price: response.data?.total_price || 0,
    };
  } catch (error) {
    console.error('Error updating cart item:', error);
    throw error;
  }
};

export const removeFromCart = async (productId: number): Promise<CartResponse> => {
  try {
    console.log(`Removing from cart: product ${productId}`);
    const response = await api.delete(`/cart/remove/${productId}/`);
    return {
      items: Array.isArray(response.data?.items) ? response.data.items : [],
      total_price: response.data?.total_price || 0,
    };
  } catch (error) {
    console.error('Error removing from cart:', error);
    throw error;
  }
};

export const applyCoupon = async (data: { code: string }): Promise<CartResponse> => {
  try {
    console.log(`Applying coupon: ${data.code}`);
    const response = await api.post('/cart/apply-coupon/', data);
    return {
      items: Array.isArray(response.data?.items) ? response.data.items : [],
      total_price: response.data?.total_price || 0,
    };
  } catch (error) {
    console.error('Error applying coupon:', error);
    throw error;
  }
};