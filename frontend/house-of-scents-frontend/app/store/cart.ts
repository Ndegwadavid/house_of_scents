import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { getCart } from '../api/cart';

interface CartItem {
  productId: number;
  name: string;
  quantity: number;
  price: number;
  photo?: string | null; // Added to match backend
  stock: number; // Added for stock validation
}

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  updateQuantity: (productId: number, quantity: number) => void;
  removeItem: (productId: number) => void;
  clearCart: () => void;
  initializeCart: () => Promise<void>;
  getTotalItems: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      addItem: (item) =>
        set((state) => {
          const existingItem = state.items.find((i) => i.productId === item.productId);
          if (existingItem) {
            const newQuantity = existingItem.quantity + item.quantity;
            if (newQuantity > item.stock) {
              return state; // Prevent adding beyond stock
            }
            return {
              items: state.items.map((i) =>
                i.productId === item.productId ? { ...i, quantity: newQuantity } : i
              ),
            };
          }
          return { items: [...state.items, item] };
        }),
      updateQuantity: (productId, quantity) =>
        set((state) => {
          const item = state.items.find((i) => i.productId === productId);
          if (item && quantity > item.stock) {
            return state; // Prevent updating beyond stock
          }
          return {
            items: state.items.map((item) =>
              item.productId === productId ? { ...item, quantity } : item
            ),
          };
        }),
      removeItem: (productId) =>
        set((state) => ({
          items: state.items.filter((item) => item.productId !== productId),
        })),
      clearCart: () => set({ items: [] }),
      initializeCart: async () => {
        try {
          const cart = await getCart();
          const items = Array.isArray(cart.items)
            ? cart.items.map((item) => ({
                productId: item.product.id,
                name: item.product.name,
                quantity: item.quantity,
                price: item.product.final_price,
                photo: item.product.photo,
                stock: item.product.stock,
              }))
            : [];
          set({ items });
        } catch (error) {
          console.error('Failed to initialize cart:', error);
          set({ items: [] });
        }
      },
      getTotalItems: () =>
        get().items.reduce((total, item) => total + item.quantity, 0),
    }),
    {
      name: 'cart-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
);