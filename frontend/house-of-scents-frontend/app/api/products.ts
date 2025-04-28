import api from '../utils/api';
import { Product, Review } from '../types/products';

export const fetchProducts = async (
  params: Record<string, string> = {}
): Promise<Product[]> => {
  try {
    const query = new URLSearchParams(params).toString();
    const response = await api.get(`/products/${query ? `?${query}` : ''}`);
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
};

export const fetchProduct = async (id: number): Promise<Product> => {
  try {
    const response = await api.get(`/products/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product:', error);
    throw error;
  }
};

export const fetchProductReviews = async (productId: number): Promise<Review[]> => {
  try {
    const response = await api.get(`/products/${productId}/reviews/`);
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching reviews:', error);
    return [];
  }
};

export const submitReview = async (
  productId: number,
  review: { rating: number; comment: string }
): Promise<void> => {
  try {
    await api.post('/products/reviews/', { product_id: productId, ...review });
  } catch (error) {
    console.error('Error submitting review:', error);
    throw error;
  }
};