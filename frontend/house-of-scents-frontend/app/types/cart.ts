// Existing content of the file

// Define and export the CartResponse type
export interface CartResponse {
    items: Array<{
      id: number;
      product: {
        id: number;
        name: string;
        photo: string | null;
        final_price: number;
        stock: number;
      };
      quantity: number;
    }>;
    total_price: number;
  }

  export interface CartItem {
    id: number;
    product: {
      id: number;
      name: string;
      photo: string | null; // Ensure photo is string | null
      final_price: number;
      stock: number;
    };
    quantity: number;
  }