import Link from 'next/link';

export default function Hero() {
  return (
    <section className="relative bg-cover bg-center h-96 flex items-center justify-center text-white"
      style={{ backgroundImage: 'url(/assets/hero-candles.jpg)' }}
    >
      <div className="absolute inset-0 bg-black bg-opacity-50"></div>
      <div className="relative z-10 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Illuminate Your Moments with House of Scents
        </h1>
        <p className="text-lg md:text-xl mb-6">
          Discover our exquisite collection of scented candles.
        </p>
        <Link
          href="/products"
          className="inline-block bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700"
        >
          Shop Now
        </Link>
      </div>
    </section>
  );
}