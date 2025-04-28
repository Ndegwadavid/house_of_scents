// types/cart.ts

// Interface for individual cart items, matching CartItemSerializer in the backend
export interface CartItem {
  id: number; // Unique ID of the cart item
  product: {
    id: number; // Product ID
    name: string; // Product name
    photo: string | null; // Product image URL or null if not available
    final_price: number; // Price after any discounts
    stock: number; // Available stock for the product
  };
  quantity: number; // Quantity of the product in the cart
  product_name?: string; // Optional field for product name (from CartItemSerializer's product_name)
}

// Interface for the full cart response, matching CartSerializer in the backend
export interface CartResponse {
  id: number; // Unique ID of the cart
  items: CartItem[]; // Array of cart items
  total_price: number; // Total price after applying coupon (if any)
  coupon: {
    id: number; // Coupon ID
    code: string; // Coupon code
    discount: number; // Discount amount or percentage (depending on backend implementation)
    minimum_order_value?: number; // Minimum order value for coupon validity
    active: boolean; // Whether the coupon is active
  } | null; // Coupon applied to the cart, or null if none
  coupon_discount: number; // Discount amount from the coupon (from get_coupon_discount)
  delivery_mode: 'pay_on_delivery' | 'collect_at_shop' | 'pay_now' | null; // Delivery mode selected
  created_at: string; // ISO timestamp of cart creation (e.g., "2025-04-28T12:00:00Z")
  updated_at: string; // ISO timestamp of last cart update
  user: {
    id: number; // User ID
    email: string; // User email
  } | null; // User associated with the cart, or null for guest
  session_key: string | null; // Session key for guest carts
}

// Interface for the cart item as stored in Zustand (simplified for local storage)
export interface CartStoreItem {
  productId: number; // Product ID
  name: string; // Product name
  quantity: number; // Quantity in the cart
  price: number; // Final price of the product
  photo: string | null; // Product image URL or null
  stock: number; // Available stock
}