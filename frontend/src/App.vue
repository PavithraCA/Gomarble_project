<!-- App.vue -->
<template>
  <div class="min-h-screen bg-black">
    <!-- Grid Background -->
    <div class="fixed inset-0 opacity-20" 
         :style="{
           backgroundImage: 'linear-gradient(#00ff9580 1px, transparent 1px), linear-gradient(90deg, #00ff9580 1px, transparent 1px)',
           backgroundSize: '50px 50px'
         }">
    </div>

    <!-- Main Content -->
    <div class="relative">
      <!-- Header -->
      <header class="border-b border-cyan-500 bg-black bg-opacity-90">
        <div class="container mx-auto px-4">
          <nav class="flex items-center justify-between py-6">
            <div class="flex items-center space-x-3">
              <div class="relative">
                <div class="w-12 h-12 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-lg animate-pulse" />
                <svg class="w-6 h-6 text-black absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <span class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500">
                StarScraper
              </span>
            </div>
          </nav>
        </div>
      </header>

      <main class="container mx-auto px-4 py-16">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <!-- Left Column -->
          <div class="space-y-8">
            <div class="space-y-4">
              <h1 class="text-5xl md:text-6xl font-bold">
                <span class="text-white">AUTOMATED</span>
                <br />
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-500">
                  REVIEW COLLECTOR
                </span>
              </h1>
              <p class="text-xl text-cyan-400">
                Intelligent web scraping system for product reviews_
              </p>
            </div>

            <!-- Features -->
            <div class="grid grid-cols-1 gap-4">
              <div class="border border-cyan-500 p-4 bg-black bg-opacity-50">
                <div class="flex items-center space-x-2">
                  <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span class="text-cyan-400">Dynamic content handling</span>
                </div>
              </div>
              <div class="border border-purple-500 p-4 bg-black bg-opacity-50">
                <div class="flex items-center space-x-2">
                  <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span class="text-purple-400">Intelligent pagination detection</span>
                </div>
              </div>
              <div class="border border-pink-500 p-4 bg-black bg-opacity-50">
                <div class="flex items-center space-x-2">
                  <svg class="w-5 h-5 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span class="text-pink-400">Advanced error handling</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column - Input Form -->
          <div class="border border-cyan-500 bg-black bg-opacity-80 p-8 relative group">
            <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
              <div class="absolute inset-0 bg-gradient-to-r from-cyan-500 to-purple-500 opacity-20" />
            </div>
            
            <form @submit.prevent="handleSubmit" class="space-y-6 relative">
              <div>
                <label class="block text-cyan-400 text-lg font-medium mb-2">
                  Target URL_
                </label>
                <input
                  type="url"
                  v-model="url"
                  class="w-full bg-black border-2 border-cyan-500 rounded-none px-4 py-3 text-cyan-400 placeholder-cyan-700 focus:outline-none focus:border-purple-500 focus:ring-0"
                  placeholder="https://target-domain.com"
                  required
                />
              </div>

              <div>
                <label class="block text-purple-400 text-lg font-medium mb-2">
                  Maximum Reviews_
                </label>
                <input
                  type="number"
                  v-model="maxReviews"
                  class="w-full bg-black border-2 border-purple-500 rounded-none px-4 py-3 text-purple-400 focus:outline-none focus:border-cyan-500 focus:ring-0"
                  min="1"
                  max="1000"
                  required
                />
                <p class="mt-2 text-sm text-purple-400 opacity-80">Maximum limit: 1000 reviews</p>
              </div>

              <button
                type="submit"
                :disabled="isLoading"
                class="w-full bg-gradient-to-r from-cyan-500 to-purple-500 text-black py-4 font-bold text-lg hover:from-purple-500 hover:to-cyan-500 transition-all duration-500 focus:outline-none disabled:opacity-50"
              >
                <span v-if="isLoading" class="flex items-center justify-center">
                  <svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  EXECUTING...
                </span>
                <span v-else>INITIATE_SCRAPING</span>
              </button>

              <div v-if="error" class="text-red-400 text-sm mt-2">
                {{ error }}
              </div>
            </form>
          </div>
        </div>

        <!-- Results Section -->
        <div v-if="results" class="mt-16 space-y-8">
          <!-- Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="border border-cyan-500 bg-black bg-opacity-80 p-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xl font-medium text-cyan-400">Total Reviews</h3>
                <span class="p-2 bg-cyan-500 bg-opacity-20">
                  <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </span>
              </div>
              <p class="text-4xl font-bold text-cyan-400">{{ results.reviews_count }}</p>
            </div>

            <div class="border border-purple-500 bg-black bg-opacity-80 p-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xl font-medium text-purple-400">Total Pages Scraped</h3>
                <span class="p-2 bg-purple-500 bg-opacity-20">
                  <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5z" />
                  </svg>
                </span>
              </div>
              <p class="text-4xl font-bold text-purple-400">{{ results.pages_with_unique_reviews }}</p>
            </div>

            <div class="border border-pink-500 bg-black bg-opacity-80 p-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xl font-medium text-pink-400">Last Visit</h3>
                <span class="p-2 bg-pink-500 bg-opacity-20">
                  <svg class="w-6 h-6 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </span>
              </div>
              <p class="text-xl font-medium text-pink-400">{{ results.scrape_date }}</p>
            </div>
          </div>

          <!-- Reviews Table -->
          <div class="border border-cyan-500 bg-black bg-opacity-80">
            <div class="p-6 border-b border-cyan-500">
              <h3 class="text-2xl font-medium text-cyan-400">Extracted Reviews_</h3>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead class="border-b border-cyan-500">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-cyan-400 uppercase">Rating</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-cyan-400 uppercase">Title</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-cyan-400 uppercase">Review</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-cyan-400 uppercase">Author</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-cyan-500">
                  <tr v-for="(review, index) in results.reviews" :key="index" class="hover:bg-cyan-500 hover:bg-opacity-10 transition-colors">
                    <td class="px-6 py-4">
                      <div class="text-cyan-400">{{ review.rating }} ★</div>
                    </td>
                    <td class="px-6 py-4">
                      <div class="text-purple-400">{{ review.title }}</div>
                    </td>
                    <td class="px-6 py-4">
                      <div class="text-pink-400">{{ review.body }}</div>
                    </td>
                    <td class="px-6 py-4">
                      <div class="text-cyan-400">{{ review.reviewer }}</div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>

      <!-- Footer -->
      <footer class="border-t border-cyan-500 mt-16 bg-black bg-opacity-90">
        <div class="container mx-auto px-4 py-6">
          <div class="flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="text-cyan-400 font-mono order-2 md:order-1">
              <span class="opacity-70">&lt;/</span>
              <span class="text-purple-400">code</span>
              <span class="opacity-70">&gt;</span>
            </div>
            <div class="order-1 md:order-2">
              <p class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500 font-mono">
                Developed by_
                <span class="font-bold"> Pavithra C</span>
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      url: '',
      maxReviews: 500,
      isLoading: false,
      error: null,
      results: null
    }
  },
  methods: {
    async handleSubmit() {
      this.isLoading = true;
      this.error = null;
      
      try {
        // Create URL with parameters
        const queryParams = new URLSearchParams({
          url: this.url,
          max_reviews: this.maxReviews
        });

        const response = await fetch(`http://localhost:5000/api/reviews?${queryParams}`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });

        // Check if response is ok before trying to parse JSON
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        this.results = data;
        console.log('Scraped data:', data);

      } catch (err) {
        this.error = err.message;
        console.error('Error:', err);
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>