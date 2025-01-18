from flask import Flask, jsonify, request
import asyncio
from playwright.async_api import async_playwright
import json
import time
from typing import Dict, List, Tuple
import re
import os
import openai
from collections import defaultdict
import logging
from bs4 import BeautifulSoup

from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
from playwright.async_api import async_playwright
import json
import time
import logging
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def detect_pagination_type(page) -> str:
    """Detect the type of pagination used on the page."""
    patterns = {
        'infinite_scroll': [
            'window.addEventListener("scroll"',
            'IntersectionObserver',
            'infinite',
            'loadMore'
        ],
        'button': [
            '.next',
            '.Next',
            '[class*="pagination"] button',
            'button[class*="next"]',
            'a[class*="next"]'
        ],
        'numbered': [
            '.pagination',
            '[class*="pagination"]',
            'nav[role="navigation"]'
        ],
        'url': [
            'a[href*="page="]',
            'a[href*="/page/"]',
            'link[rel="next"]'
        ]
    }
    
    for ptype, selectors in patterns.items():
        for selector in selectors:
            try:
                if selector.startswith('.') or selector.startswith('['):
                    elements = await page.query_selector_all(selector)
                    if elements:
                        return ptype
                else:
                    content = await page.content()
                    if selector in content.lower():
                        return ptype
            except:
                continue
    
    return 'unknown'

async def handle_dynamic_loading(page):
    """Handle dynamic content loading through scrolling and button clicks."""
    try:
        # Scroll to bottom in increments
        current_height = 0
        for _ in range(3):
            try:
                await page.evaluate('''() => {
                    window.scrollTo({
                        top: document.body.scrollHeight,
                        behavior: 'smooth'
                    });
                }''')
                await page.wait_for_timeout(1000)
                
                new_height = await page.evaluate('document.body.scrollHeight')
                if new_height == current_height:
                    break
                current_height = new_height
            except Exception as scroll_error:
                logger.error(f"Scroll error: {str(scroll_error)}")
                break
        
        # Try to scroll to pagination area
        try:
            await page.evaluate('''() => {
                const paginationElements = document.querySelectorAll('[class*="pagination"], .next, [aria-label="Next page"]');
                if (paginationElements.length > 0) {
                    paginationElements[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }''')
            await page.wait_for_timeout(1000)
        except Exception as scroll_error:
            logger.error(f"Pagination scroll error: {str(scroll_error)}")
        
        # Try clicking "Load More" buttons
        load_more_selectors = [
            'button:text-is("Show More")',
            'button:text-is("Load More")',
            'a:text-is("Show More")',
            'a:text-is("Load More")',
            '[class*="load-more"]',
            '[class*="show-more"]'
        ]
        
        for selector in load_more_selectors:
            try:
                while True:
                    button = await page.query_selector(selector)
                    if not button or not await button.is_visible():
                        break
                    await button.click()
                    await page.wait_for_timeout(2000)
            except:
                continue
                
    except Exception as e:
        logger.error(f"Error in dynamic loading: {str(e)}")

async def handle_pagination(page, current_page: int) -> bool:
    """Handle different types of pagination including numbered buttons and arrows."""
    try:
        logger.info(f"Current URL before pagination: {page.url}")
        logger.info(f"Current page: {current_page}")

        # First try direct numbered pagination
        selectors = [
            f'[class*="pagination"] [aria-label="Page {current_page + 1}"]',
            f'[class*="pagination"] a:text("{current_page + 1}")',
            f'button:text("{current_page + 1}")',
            f'a[href*="page={current_page + 1}"]',
            '[class*="pagination"] [aria-label*="next"]',
            '[class*="pagination"] button:has-text(">")',
            '[class*="pagination"] a:has-text(">")',
            '.next a',
            'a[rel="next"]',
            '.pagination__next',
            '.pagination__item--next',
            '[class*="pagination"] button:not([disabled])',
            '[class*="pagination"] a:not([class*="disabled"])',
            'li.next a'
        ]

        # Try to find and click pagination elements
        for selector in selectors:
            try:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                except:
                    continue

                element = await page.query_selector(selector)
                if element:
                    logger.info(f"Found pagination element with selector: {selector}")
                    
                    if await element.is_visible():
                        before_url = page.url
                        before_html = await page.content()
                        
                        await element.scroll_into_view_if_needed()
                        await page.wait_for_timeout(1000)
                        
                        try:
                            await element.click(timeout=5000)
                            logger.info("Clicked pagination element")
                        except:
                            await page.evaluate('(element) => element.click()', element)
                            logger.info("Used JavaScript click fallback")
                        
                        try:
                            await page.wait_for_load_state('networkidle', timeout=5000)
                        except:
                            await page.wait_for_timeout(2000)
                        
                        after_url = page.url
                        after_html = await page.content()
                        
                        if before_url != after_url or before_html != after_html:
                            logger.info(f"Successfully navigated to next page: {after_url}")
                            return True
                
            except Exception as e:
                logger.error(f"Error with selector {selector}: {str(e)}")
                continue
        
        # If clicking didn't work, try URL modification
        try:
            current_url = page.url
            logger.info("Trying URL modification...")
            
            if 'page=' in current_url:
                next_url = re.sub(r'page=\d+', f'page={current_page + 1}', current_url)
            else:
                separator = '&' if '?' in current_url else '?'
                next_url = f"{current_url}{separator}page={current_page + 1}"
            
            logger.info(f"Attempting to navigate to: {next_url}")
            
            response = await page.goto(next_url)
            if response and response.ok():
                await page.wait_for_timeout(2000)
                return True
        
        except Exception as e:
            logger.error(f"Error during URL modification: {str(e)}")
        
        logger.warning("No more pages found")
        return False
        
    except Exception as e:
        logger.error(f"Error in pagination: {str(e)}")
        return False

import logging
import re
from typing import List, Dict
import openai

logger = logging.getLogger(__name__)

async def extract_reviews_llm(page, api_key: str) -> List[Dict]:
    """Extract reviews using LLM-based analysis with fallback to common selectors."""
    try:
        logger.info(f"Starting review extraction for page: {await page.title()}")
        
        # First try with common selectors
        logger.info("Trying extraction with common selectors...")
        reviews = await page.evaluate("""(selectors) => {
            function cleanText(text) {
                if (!text) return '';
                return text.replace(/\\s+/g, ' ')
                          .replace(/\\r?\\n/g, ' ')
                          .trim();
            }

            function extractRating(element) {
                try {
                    // Check for star elements
                    let stars = element.querySelectorAll('.spr-review-rating .spr-icon.spr-icon-star');
                    if (stars.length > 0 && stars.length <= 5) {
                        return stars.length;
                    }

                    // Check for data-rating attribute
                    const dataRating = element.querySelector('[data-rating]');
                    if (dataRating) {
                        const rating = parseFloat(dataRating.getAttribute('data-rating'));
                        if (!isNaN(rating) && rating >= 0 && rating <= 5) {
                            return rating;
                        }
                    }

                    // Check text for rating patterns
                    const text = element.textContent;
                    const ratingMatch = text.match(/([1-5]([.,]\\d)?)\s*(?:star|\/\s*5|$)/i);
                    if (ratingMatch) {
                        return parseFloat(ratingMatch[1].replace(',', '.'));
                    }

                    return null;
                } catch (error) {
                    console.error('Error extracting rating:', error);
                    return null;
                }
            }

            const reviews = [];
            const seenContent = new Set();

            // Try Shopify Product Reviews
            const reviewElements = document.querySelectorAll('.spr-review');
            reviewElements.forEach(review => {
                try {
                    const title = review.querySelector('.spr-review-header-title')?.textContent.trim() || 'Review';
                    const body = review.querySelector('.spr-review-content-body')?.textContent.trim();
                    const author = review.querySelector('.spr-review-header-byline')?.textContent.trim() || 'Anonymous';
                    const rating = extractRating(review);

                    if (body && !seenContent.has(body)) {
                        seenContent.add(body);
                        reviews.push({
                            title: title,
                            body: cleanText(body),
                            rating: rating,
                            reviewer: cleanText(author)
                        });
                    }
                } catch (e) {
                    console.error('Error processing review:', e);
                }
            });

            // If no reviews found, try alternative selectors
            if (reviews.length === 0) {
                const alternativeContainers = document.querySelectorAll('[data-review-id], [class*="review-item"], .jdgm-rev, .yotpo-review');
                alternativeContainers.forEach(container => {
                    try {
                        const contentSelectors = [
                            '[class*="review-content"]',
                            '[class*="review-body"]',
                            '[class*="review-text"]',
                            '.jdgm-rev__body',
                            '.yotpo-review-content'
                        ];

                        let body = null;
                        for (const selector of contentSelectors) {
                            const content = container.querySelector(selector)?.textContent.trim();
                            if (content) {
                                body = content;
                                break;
                            }
                        }

                        if (!body) {
                            body = container.textContent.trim();
                        }

                        if (body && !seenContent.has(body) && body.split(/\\s+/).length >= 3) {
                            const title = container.querySelector('[class*="review-title"], [class*="review-header"]')?.textContent.trim() || 'Review';
                            const author = container.querySelector('[class*="review-author"], [class*="reviewer-name"]')?.textContent.trim() || 'Anonymous';
                            const rating = extractRating(container);

                            seenContent.add(body);
                            reviews.push({
                                title: cleanText(title),
                                body: cleanText(body),
                                rating: rating,
                                reviewer: cleanText(author)
                            });
                        }
                    } catch (e) {
                        console.error('Error processing alternative container:', e);
                    }
                });
            }

            return reviews;
        }""", {})  # Pass empty object as we're not using external selectors anymore
        
        if reviews and len(reviews) > 0:
            logger.info(f"Found {len(reviews)} reviews")
            return reviews
            
        logger.warning("No reviews found using common selectors")
        return []
        
    except Exception as e:
        logger.error(f"Error in review extraction: {str(e)}")
        return []

async def scrape_reviews(url: str, api_key: str, max_reviews: int = 500) -> Dict:
    """Main review scraping function."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        all_reviews = []
        successful_pages = 0
        
        try:
            logger.info("Starting review scraping process...")
            await page.goto(url, wait_until='domcontentloaded')
            await page.wait_for_timeout(2000)
            
            page_num = 1
            consecutive_no_new_reviews = 0
            
            while len(all_reviews) < max_reviews and page_num <= 50:
                logger.info(f"Scraping page {page_num}...")
                
                await handle_dynamic_loading(page)
                
                new_reviews = await extract_reviews_llm(page, api_key)
                
                if new_reviews:
                    initial_review_count = len(all_reviews)
                    existing_contents = set(r['body'] for r in all_reviews)
                    unique_reviews = [r for r in new_reviews if r['body'] not in existing_contents]
                    all_reviews.extend(unique_reviews)
                    
                    if len(all_reviews) > initial_review_count:
                        consecutive_no_new_reviews = 0
                        successful_pages += 1
                        logger.info(f"Found {len(unique_reviews)} new unique reviews on page {page_num}")
                    else:
                        consecutive_no_new_reviews += 1
                        logger.warning(f"No new unique reviews found on page {page_num}")
                else:
                    consecutive_no_new_reviews += 1
                    logger.warning(f"No reviews found on page {page_num}")
                
                if consecutive_no_new_reviews >= 3:
                    logger.info("Stopping: No new unique reviews found for 3 consecutive pages")
                    break
                
                if len(all_reviews) < max_reviews:
                    has_next = await handle_pagination(page, page_num)
                    if not has_next:
                        logger.warning(f"No more pages found after page {page_num}")
                        break
                    page_num += 1
                else:
                    break
            
            return {
                "reviews": all_reviews,
                "reviews_count": len(all_reviews),
                "pages_with_unique_reviews": successful_pages,
                "max_reviews_limit": max_reviews,
                "url": url,
                "scrape_date": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        finally:
            await context.close()
            await browser.close()



from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
from playwright.async_api import async_playwright
import json
import time
import logging
from bs4 import BeautifulSoup



@app.route('/api/reviews', methods=['GET'])
async def get_reviews():
    """API endpoint to scrape reviews from a given URL."""
    try:
        # Get and validate URL parameter
        url = request.args.get('url')
        if not url:
            return jsonify({
                "error": "URL parameter is required",
                "status": "error"
            }), 400

        # Get and validate max_reviews parameter
        try:
            max_reviews = int(request.args.get('max_reviews', 500))
            if max_reviews < 1:
                raise ValueError("max_reviews must be positive")
        except ValueError as e:
            return jsonify({
                "error": f"Invalid max_reviews parameter: {str(e)}",
                "status": "error"
            }), 400

        logger.info(f"Starting review scraping for URL: {url}")
        
        try:
            # Initialize Playwright
            async with async_playwright() as p:
                # Launch browser with specific options
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()

                try:
                    # Navigate to URL with timeout
                    await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                    await page.wait_for_timeout(2000)

                    # Get page content
                    content = await page.content()
                    
                    # Extract reviews using your existing functions
                    reviews = await extract_reviews_llm(page, None)  # Implement this based on your backend code
                    
                    # Prepare successful response
                    result = {
                        "status": "success",
                        "reviews": reviews,
                        "reviews_count": len(reviews),
                        "pages_with_unique_reviews": 1,
                        "max_reviews_limit": max_reviews,
                        "url": url,
                        "scrape_date": time.strftime("%Y-%m-%d %H:%M:%S")
                    }

                    # Ensure the response is JSON serializable
                    return app.response_class(
                        response=json.dumps(result, ensure_ascii=False),
                        status=200,
                        mimetype='application/json'
                    )

                except Exception as e:
                    logger.error(f"Scraping error: {str(e)}")
                    return jsonify({
                        "error": f"Failed to scrape reviews: {str(e)}",
                        "status": "error"
                    }), 500

                finally:
                    # Always close browser resources
                    await context.close()
                    await browser.close()

        except Exception as e:
            logger.error(f"Browser error: {str(e)}")
            return jsonify({
                "error": f"Failed to initialize browser: {str(e)}",
                "status": "error"
            }), 500

    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({
            "error": f"Server error: {str(e)}",
            "status": "error"
        }), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)