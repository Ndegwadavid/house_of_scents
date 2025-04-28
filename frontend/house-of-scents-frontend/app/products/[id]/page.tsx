'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { fetchProduct, submitReview } from '../../api/products';
import Link from 'next/link';
import StarRating from '../../components/ui/StarRating';
import { useCartStore } from '../../store/cart';
import { useAuth } from '../../auth/AuthContext';
import { addToCart } from '../../api/cart';
import toast from 'react-hot-toast';
import { Product } from '../../types/products';
import { use } from 'react';
import { Star, Send } from 'lucide-react';

export default function ProductDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [reviewRating, setReviewRating] = useState<number>(0);
  const [reviewComment, setReviewComment] = useState<string>('');
  const [reviewSubmitting, setReviewSubmitting] = useState(false);
  const router = useRouter();
  const { addItem } = useCartStore();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const loadProduct = async () => {
      try {
        const data = await fetchProduct(Number(id));
        setProduct(data);
        setSelectedImage(data.photo || data.images[0]?.image || null);
      } catch (error) {
        toast.error('Failed to load product');
        router.push('/products');
      } finally {
        setLoading(false);
      }
    };
    loadProduct();
  }, [id, router]);

  const handleAddToCart = async () => {
    if (!product) return;
    try {
      await addToCart(product.id, 1);
      addItem({
        productId: product.id,
        name: product.name,
        quantity: 1,
        price: product.final_price,
        stock: product.stock,
      });
      toast.success(`${product.name} added to cart`);
    } catch (error) {
      toast.error('Failed to add to cart');
    }
  };

  const handleSubmitReview = async () => {
    if (!isAuthenticated) {
      toast.error('Please log in to submit a review');
      router.push('/auth/login');
      return;
    }
    if (reviewRating < 1 || reviewRating > 5) {
      toast.error('Please select a rating between 1 and 5');
      return;
    }
    if (!reviewComment.trim()) {
      toast.error('Please enter a review comment');
      return;
    }
    setReviewSubmitting(true);
    try {
      await submitReview(Number(id), { rating: reviewRating, comment: reviewComment });
      toast.success('Review submitted successfully');
      setReviewRating(0);
      setReviewComment('');
      const data = await fetchProduct(Number(id));
      setProduct(data);
    } catch (error) {
      toast.error('Failed to submit review');
    } finally {
      setReviewSubmitting(false);
    }
  };

  const averageRating =
    product && product.reviews.length > 0
      ? product.reviews.reduce((sum, review) => sum + review.rating, 0) /
        product.reviews.length
      : 0;

  if (loading) return <div className="container mx-auto p-4">Loading...</div>;
  if (!product) return <div className="container mx-auto p-4">Product not found</div>;

  return (
    <div className="container mx-auto py-12 px-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <Image
            src={selectedImage || '/assets/placeholder.jpg'}
            alt={product.name}
            width={400}
            height={400}
            className="w-full h-96 object-cover rounded-lg"
          />
          <div className="flex space-x-2 mt-4">
            {[product.photo, ...product.images.map((img) => img.image)]
              .filter(Boolean)
              .map((img, index) => (
                <Image
                  key={index}
                  src={img!}
                  alt={`${product.name} ${index + 1}`}
                  width={80}
                  height={80}
                  className={`w-20 h-20 object-cover rounded cursor-pointer ${
                    selectedImage === img ? 'border-2 border-blue-600' : ''
                  }`}
                  onClick={() => setSelectedImage(img!)}
                />
              ))}
          </div>
        </div>
        <div>
          <h1 className="text-3xl font-semibold">{product.name}</h1>
          {product.is_new && (
            <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded ml-2">
              New
            </span>
          )}
          <p className="text-gray-900 font-bold mt-2">KES {product.final_price}</p>
          <p className="text-gray-600 mt-2">
            <span className="font-medium">Scent:</span> {product.scent || 'N/A'}
          </p>
          <p className="text-gray-600 mt-2">
            <span className="font-medium">Category:</span>{' '}
            <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
              {product.category.name}
            </span>
          </p>
          <p className="text-gray-600 mt-4">{product.description}</p>
          {product.reviews.length > 0 && (
            <div className="mt-4">
              <StarRating rating={Math.round(averageRating)} />
              <span className="ml-2 text-gray-600 text-sm">
                ({product.reviews.length} reviews)
              </span>
            </div>
          )}
          <button
            onClick={handleAddToCart}
            disabled={product.stock === 0}
            className="mt-6 w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
          </button>
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">Write a Review</h2>
            {isAuthenticated ? (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Rating</label>
                  <div className="flex space-x-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star
                        key={star}
                        className={`w-6 h-6 cursor-pointer ${
                          star <= reviewRating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'
                        }`}
                        onClick={() => setReviewRating(star)}
                      />
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Comment</label>
                  <textarea
                    value={reviewComment}
                    onChange={(e) => setReviewComment(e.target.value)}
                    className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
                    rows={4}
                    placeholder="Share your thoughts about this product..."
                  />
                </div>
                <button
                  onClick={handleSubmitReview}
                  disabled={reviewSubmitting}
                  className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400 flex items-center"
                >
                  <Send className="w-5 h-5 mr-2" />
                  Submit Review
                </button>
              </div>
            ) : (
              <p className="text-gray-600">
                Please <Link href="/auth/login" className="text-blue-600 hover:underline">log in</Link> to write a review.
              </p>
            )}
          </div>
          {product.reviews.length > 0 && (
            <div className="mt-8">
              <h2 className="text-xl font-semibold mb-4">Reviews</h2>
              {product.reviews.map((review) => (
                <div key={review.id} className="mt-4 border-t pt-4">
                  <div className="flex items-center">
                    <StarRating rating={review.rating} />
                    <span className="ml-2 text-gray-600 text-sm">
                      by {review.user_name} ({review.masked_email})
                    </span>
                  </div>
                  <p className="text-gray-600 mt-2">{review.comment}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}