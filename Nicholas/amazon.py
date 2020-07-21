import webview
import time

cur_page = 1
total_items_found = 0

def page_loaded():
    global cur_page
    global total_items_found
    global start_time

    full_page = webview.windows[0].evaluate_js('document.documentElement.innerHTML;')

    items_found = 0
    while full_page.find('<span class="a-size-base-plus a-color-base a-text-normal">') > -1:

        # If there are still sponsored items left on the page
        if full_page.find('<span class=\"aok-inline-block s-sponsored-label-info-icon\">') > -1:
            # If the sponsor tag comes before the next product (meaning the next product is a sponsored product)
            if full_page.find('<span class=\"aok-inline-block s-sponsored-label-info-icon\">') < full_page.find('<span class="a-size-base-plus a-color-base a-text-normal">'):
                # Skip this product
                full_page = full_page[full_page.find('<span class="a-size-base-plus a-color-base a-text-normal">') + 1:]
                continue

        # If we're here then we know the next item is not a sponsored item

        full_page = full_page[full_page.find('<span class="a-size-base-plus a-color-base a-text-normal">'):]
        full_page = full_page[full_page.find('>') + 1:]
        cur_product_name = full_page[:full_page.find('</span>')]

        if full_page.find('<span class=\"a-icon-alt\">') > -1:
            full_page = full_page[full_page.find('<span class=\"a-icon-alt\">'):]
            full_page = full_page[full_page.find('>') + 1:]
            cur_product_rating = full_page[:full_page.find('</span>')]

            if full_page.find('<span class=\"a-offscreen\">') > -1:
                full_page = full_page[full_page.find('<span class=\"a-offscreen\">'):]
                full_page = full_page[full_page.find('>') + 1:]
                cur_product_price = full_page[:full_page.find('</span>')]

                price_per_unit_index = full_page.find('<span class=\"a-size-base a-color-secondary\">')
                if price_per_unit_index != -1 and price_per_unit_index < full_page.find('</a>'):
                    full_page = full_page[full_page.find('<span class=\"a-size-base a-color-secondary\">'):]
                    full_page = full_page[full_page.find('>') + 1:]
                    cur_product_price = full_page[:full_page.find('</span>')]

                print(cur_product_name + ' = ' + cur_product_rating + ' = ' + cur_product_price)
                items_found += 1

    total_items_found += items_found
    total_time_elapsed = time.time() - start_time
    items_per_second = total_items_found / total_time_elapsed
    print('--------------------------------------------------')
    print('Found ' + str(total_items_found) + ' in ' + str(round(total_time_elapsed)) + ' seconds')
    print(str(round(items_per_second)) + ' items per second')

    if items_found == 0 and cur_page > 1:
        print('Found no items on page ' + str(cur_page))
        cur_page = 1
    else:
        cur_page += 1
    
    print('--------------------------------------------------')

    webview.windows[0].load_url('https://www.amazon.com/s?k=cheese&page=' + str(cur_page))


start_time = time.time()
webview.create_window('', 'https://www.amazon.com/s?k=cheese&page=1')
webview.windows[0].loaded += page_loaded
webview.start()