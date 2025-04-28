export default function Footer() {
    return (
      <footer className="bg-gray-800 text-white py-6">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <img
                src="/assets/logo.png"
                alt="House of Scents Logo"
                className="h-8 w-auto"
              />
              <p className="mt-2 text-sm">
                Premium scented candles for every occasion.
              </p>
            </div>
            <div className="flex space-x-6">
              <a href="/products" className="hover:text-blue-400">
                Products
              </a>
              <a href="/cart" className="hover:text-blue-400">
                Cart
              </a>
              <a href="/orders" className="hover:text-blue-400">
                Orders
              </a>
              <a href="/profile" className="hover:text-blue-400">
                Profile
              </a>
            </div>
          </div>
          <div className="mt-4 text-center text-sm">
            &copy; {new Date().getFullYear()} House of Scents. All rights reserved.
          </div>
        </div>
      </footer>
    );
  }