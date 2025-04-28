import Hero from '../app/components/ui/Hero';
import Footer from '../app/components/ui/Footer';
import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <Hero />
      <section className="container mx-auto py-12 px-4">
        <h2 className="text-3xl font-bold text-center mb-8">
          Our Scented Candles
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Placeholder for product cards */}
          <div className="bg-white shadow-md rounded-lg p-4">
            <img
              src="/assets/candle-placeholder.jpg"
              alt="Scented Candle"
              className="w-full h-48 object-cover rounded"
            />
            <h3 className="text-lg font-semibold mt-4">Lavender Glow</h3>
            <p className="text-gray-600 mt-2">KES 500</p>
            <Link
              href="/products"
              className="mt-4 inline-block bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
            >
              View Details
            </Link>
          </div>
          <div className="bg-white shadow-md rounded-lg p-4">
            <img
              src="/assets/candle-placeholder.jpg"
              alt="Scented Candle"
              className="w-full h-48 object-cover rounded"
            />
            <h3 className="text-lg font-semibold mt-4">Rose Bliss</h3>
            <p className="text-gray-600 mt-2">KES 1000</p>
            <Link
              href="/products"
              className="mt-4 inline-block bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
            >
              View Details
            </Link>
          </div>
          <div className="bg-white shadow-md rounded-lg p-4">
            <img
              src="/assets/candle-placeholder.jpg"
              alt="Scented Candle"
              className="w-full h-48 object-cover rounded"
            />
            <h3 className="text-lg font-semibold mt-4">Vanilla Dream</h3>
            <p className="text-gray-600 mt-2">KES 750</p>
            <Link
              href="/products"
              className="mt-4 inline-block bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
            >
              View Details
            </Link>
          </div>
        </div>
        <div className="text-center mt-8">
          <Link
            href="/products"
            className="inline-block bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700"
          >
            Explore All Candles
          </Link>
        </div>
      </section>
      <Footer />
    </div>
  );
}