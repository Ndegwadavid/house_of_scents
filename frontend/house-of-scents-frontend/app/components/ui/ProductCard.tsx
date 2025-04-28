'use client';

import Image from 'next/image';
import Link from 'next/link';
import { useCartStore } from '../../store/cart';
import { addToCart } from '../../api/cart';
import toast from 'react-hot-toast';
import StarRating from '../../components/ui/StarRating';
import { Product } from '../../types/products';

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const { addItem } = useCartStore();

  const handleAddToCart = async () => {
    try {
      await addToCart(product.id, 1);
      addItem({
        productId: product.id,
        name: product.name,
        quantity: 1,
        price: product.final_price,
      });
      toast.success(`${product.name} added to cart`);
    } catch (error) {
      toast.error('Failed to add to cart');
    }
  };

  const averageRating =
    product.reviews.length > 0
      ? product.reviews.reduce((sum, review) => sum + review.rating, 0) /
        product.reviews.length
      : 0;

  return (
    <div className="bg-white shadow-md rounded-lg p-4 transition-transform transform hover:scale-105 relative">
      {product.photo ? (
        <Image
          src={product.photo}
          alt={product.name}
          width={200}
          height={200}
          className="w-full h-48 object-cover rounded"
          onError={() => (
            <div className="w-full h-48 bg-gray-200 rounded flex items-center justify-center">
              <span>No Image</span>
            </div>
          )}
        />
      ) : (
        <div className="w-full h-48 bg-gray-200 rounded flex items-center justify-center">
          <span>No Image</span>
        </div>
      )}
      <Link href={`/products/${product.id}`} className="absolute top-4 right-4">
        <svg
          className="w-6 h-6 text-gray-600 hover:text-blue-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
          />
        </svg>
      </Link>
      <div className="mt-4">
        <div className="flex justify-between items-start">
          <h3 className="text-lg font-semibold">{product.name}</h3>
          {product.is_new && (
            <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded">
              New
            </span>
          )}
        </div>
        <p className="text-gray-600 mt-2 line-clamp-2">{product.description}</p>
        <p className="text-gray-600 mt-2">
          <span className="font-medium">Scent:</span> {product.scent || 'N/A'}
        </p>
        <p className="text-gray-600 mt-2">
          <span className="font-medium">Category:</span>{' '}
          <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
            {product.category.name}
          </span>
        </p>
        <p className="text-gray-900 font-bold mt-2">KES {product.final_price}</p>
        {product.reviews.length > 0 && (
          <div className="mt-2 flex items-center">
            <StarRating rating={Math.round(averageRating)} />
            <span className="ml-2 text-gray-600 text-sm">
              ({product.reviews.length} reviews)
            </span>
          </div>
        )}
        <button
          onClick={handleAddToCart}
          disabled={product.stock === 0}
          className="mt-4 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
        </button>
      </div>
    </div>
  );
}