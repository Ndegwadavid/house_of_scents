export interface Review {
    id: number;
    rating: number;
    comment: string;
    user_name: string;
    masked_email: string;
    created_at: string;
  }
  
  export interface ProductImage {
    id: number;
    image: string;
    created_at: string;
  }
  
  export interface Category {
    id: number;
    name: string;
  }
  
  export interface Product {
    id: number;
    name: string;
    description: string;
    scent?: string;
    final_price: number;
    stock: number;
    photo?: string;
    is_new: boolean;
    is_featured: boolean;
    category: Category;
    reviews: Review[];
    images: ProductImage[];
  }
  
  export interface PaginatedResponse {
    count: number;
    next: string | null;
    previous: string | null;
    results: Product[];
  }