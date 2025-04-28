import api from '../utils/api';
import { CartResponse as ExternalCartResponse } from '../types/cart';

// Define a more accurate CartResponse type to match backend
// Add the export for CartResponse if missing
export interface CartResponse {
  id: number;
  items: Array<{
    id: number;
    product: {
      id: number;
      name: string;
      final_price: number;
      stock: number;
      photo?: string;
    };
    quantity: number;
  }>;
  total_price: number;
  coupon_discount?: number;
  delivery_mode?: string;
}

export const getCart = async (): Promise<CartResponse> => {
  try {
    console.log('Calling /api/cart/');
    const response = await api.get('/cart/');
    console.log('Cart response:', response.data);
    // Ensure items is an array and provide defaults
    return {
      id: response.data.id || 0,
      items: Array.isArray(response.data.items) ? response.data.items : [],
      total_price: response.data.total_price || 0,
      coupon_discount: response.data.coupon_discount || null,
      delivery_mode: response.data.delivery_mode || null,
    };
  } catch (error: any) {
    console.error('Error fetching cart:', error.response?.status, error.message);
    throw error; // Let the caller handle the error
  }
};

export const addToCart = async (productId: number, quantity: number): Promise<CartResponse> => {
  try {
    console.log(`Adding to cart: product ${productId}, quantity ${quantity}`);
    const response = await api.post('/cart/add/', { product_id: productId, quantity });
    return {
      id: response.data.id || 0,
      items: Array.isArray(response.data.items) ? response.data.items : [],
      total_price: response.data.total_price || 0,
      coupon_discount: response.data.coupon_discount || null,
      delivery_mode: response.data.delivery_mode || null,
    };
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
    const response = await api.patch('/cart/update/', { product_id: productId, quantity });
    return {
      id: response.data.id || 0,
      items: Array.isArray(response.data.items) ? response.data.items : [],
      total_price: response.data.total_price || 0,
      coupon_discount: response.data.coupon_discount || null,
      delivery_mode: response.data.delivery_mode || null,
    };
  } catch (error) {
    console.error('Error updating cart item:', error);
    throw error;
  }
};

export const removeFromCart = async (productId: number): Promise<CartResponse> => {
  try {
    console.log(`Removing from cart: product ${productId}`);
    const response = await api.delete('/cart/remove/', {
      data: { product_id: productId }, // DELETE requests with body need 'data'
    });
    return {
      id: response.data.id || 0,
      items: Array.isArray(response.data.items) ? response.data.items : [],
      total_price: response.data.total_price || 0,
      coupon_discount: response.data.coupon_discount || null,
      delivery_mode: response.data.delivery_mode || null,
    };
  } catch (error) {
    console.error('Error removing from cart:', error);
    throw error;
  }
};

export const applyCoupon = async (data: { code: string }): Promise<CartResponse> => {
  try {
    console.log(`Applying coupon: ${data.code}`);
    // Backend expects PATCH to /cart/ with coupon_code
    const response = await api.patch('/cart/', { coupon_code: data.code });
    return {
      id: response.data.id || 0,
      items: Array.isArray(response.data.items) ? response.data.items : [],
      total_price: response.data.total_price || 0,
      coupon_discount: response.data.coupon_discount || null,
      delivery_mode: response.data.delivery_mode || null,
    };
  } catch (error) {
    console.error('Error applying coupon:', error);
    throw error;
  }
};

export const updateDeliveryMode = async (deliveryMode: string): Promise<CartResponse> => {
  try {
    console.log(`Updating delivery mode: ${deliveryMode}`);
    const response = await api.patch('/cart/', { delivery_mode: deliveryMode });
    return {
      id: response.data.id || 0,
      items: Array.isArray(response.data.items) ? response.data.items : [],
      total_price: response.data.total_price || 0,
      coupon_discount: response.data.coupon_discount || null,
      delivery_mode: response.data.delivery_mode || null,
    };
  } catch (error) {
    console.error('Error updating delivery mode:', error);
    throw error;
  }
};