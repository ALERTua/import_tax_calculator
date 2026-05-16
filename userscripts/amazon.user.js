// ==UserScript==
// @name         Amazon Ukraine Customs Tax Calculator
// @namespace    https://www.amazon.com
// @version      1.1.1
// @description  Calculate Ukraine customs tax for Amazon products
// @author       Alexey ALERT Rubasheff
// @homepageURL  https://github.com/ALERTua/import_tax_calculator/blob/main/userscripts/amazon.user.js
// @updateURL    https://github.com/ALERTua/import_tax_calculator/raw/refs/heads/main/userscripts/amazon.user.js
// @downloadURL  https://github.com/ALERTua/import_tax_calculator/raw/refs/heads/main/userscripts/amazon.user.js
// @source       https://github.com/ALERTua/import_tax_calculator/raw/refs/heads/main/userscripts/amazon.user.js
// @match        *://www.amazon.com/*
// @match        *://www.amazon.ae/*
// @match        *://www.amazon.be/*
// @match        *://www.amazon.ca/*
// @match        *://www.amazon.cn/*
// @match        *://www.amazon.co.jp/*
// @match        *://www.amazon.co.uk/*
// @match        *://www.amazon.co.za/*
// @match        *://www.amazon.com.au/*
// @match        *://www.amazon.com.br/*
// @match        *://www.amazon.com.mx/*
// @match        *://www.amazon.com.tr/*
// @match        *://www.amazon.de/*
// @match        *://www.amazon.eg/*
// @match        *://www.amazon.es/*
// @match        *://www.amazon.fr/*
// @match        *://www.amazon.in/*
// @match        *://www.amazon.it/*
// @match        *://www.amazon.nl/*
// @match        *://www.amazon.pl/*
// @match        *://www.amazon.sa/*
// @match        *://www.amazon.se/*
// @match        *://www.amazon.sg/*
// @exclude      *://*.amazon.*/ap/signin*
// @connect      tax.alertua.pp.ua
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function () {
    'use strict';

    const API_URL = 'https://tax.alertua.pp.ua/calculate_api/';

    // Only currencies supported by the backend (EUR, USD)
    const HOST_CURRENCY = {
        'www.amazon.com': 'USD',
        'www.amazon.de': 'EUR',
        'www.amazon.fr': 'EUR',
        'www.amazon.it': 'EUR',
        'www.amazon.es': 'EUR',
        'www.amazon.nl': 'EUR',
        'www.amazon.be': 'EUR',
        'www.amazon.pl': 'EUR',
        'www.amazon.se': 'EUR',
    };

    const defaultCurrency = HOST_CURRENCY[document.location.hostname];
    if (!defaultCurrency) {
        console.info('Customs Tax Calculator: hostname not supported, skipping: ' + document.location.hostname);
        return;
    }

    // Symbols that imply a currency the backend doesn't support → skip the price
    const UNSUPPORTED_RE = /CA\$|AU\$|MX\$|HK\$|S\$|R\$|£|¥|₹|kr|zł|﷼/;

    function parsePrice(text) {
        if (UNSUPPORTED_RE.test(text)) return null;
        const numMatch = text.match(/[+-]?\d[\d,.  ]*\d|\d/);
        if (!numMatch) return null;
        let raw = numMatch[0].replace(/[  ]/g, '');
        // European format: "1.234,56" → "1234.56"; US format: "1,234.56" → "1234.56"
        raw = /,\d{1,2}$/.test(raw) ? raw.replace(/\./g, '').replace(',', '.') : raw.replace(/,/g, '');
        const price = parseFloat(raw);
        if (!isFinite(price) || price <= 0) return null;

        let currency = null;
        if (/€|\bEUR\b/i.test(text)) currency = 'EUR';
        else if (/\$|\bUSD\b/i.test(text)) currency = 'USD';
        if (!currency) currency = defaultCurrency;

        return { price: price, currency: currency };
    }

    // Cache by (price, currency) — dedupes in-flight requests too, since we store the Promise
    const cache = new Map();

    function fetchTax(price, currency) {
        const key = price + '|' + currency;
        if (cache.has(key)) return cache.get(key);

        const url = API_URL + '?price=' + encodeURIComponent(price) + '&currency=' + encodeURIComponent(currency);
        const promise = new Promise(function (resolve, reject) {
            GM_xmlhttpRequest({
                method: 'GET',
                url: url,
                headers: { 'Accept': 'application/json' },
                responseType: 'json',
                onload: function (response) {
                    if (response.status === 200) {
                        resolve(response.response);
                    } else if (response.status === 400) {
                        reject(new Error('validation: ' + JSON.stringify(response.response)));
                    } else if (response.status === 503) {
                        reject(new Error('service unavailable: backend constants not configured'));
                    } else {
                        reject(new Error('HTTP ' + response.status));
                    }
                },
                onerror: function () { reject(new Error('network error')); },
                ontimeout: function () { reject(new Error('timeout')); },
            });
        });

        // Don't cache failures — let the next retry try fresh
        promise.catch(function () { cache.delete(key); });

        cache.set(key, promise);
        return promise;
    }

    function renderLabel(container, text, title) {
        const span = document.createElement('span');
        span.className = 'customs-tax-label';
        span.style.marginLeft = '4px';
        span.style.opacity = '0.8';
        span.textContent = text;
        if (title) span.title = title;
        container.parentNode.insertBefore(span, container.nextSibling);
    }

    function processOffscreen(offscreenEl) {
        const container = offscreenEl.closest('.a-price');
        if (!container || container.dataset.taxApplied) return;
        container.dataset.taxApplied = '1';

        const parsed = parsePrice(offscreenEl.textContent.trim());
        if (!parsed) return;

        fetchTax(parsed.price, parsed.currency)
            .then(function (data) {
                renderLabel(container, ' + Tax: ' + parseFloat(data.tax).toFixed(2) + ' ' + data.currency);
            })
            .catch(function (err) {
                console.error('Customs Tax Calculator: ' + err.message);
                renderLabel(container, ' + Tax: ?', err.message);
            });
    }

    function scan(root) {
        const nodes = (root || document).querySelectorAll('.a-price span.a-offscreen');
        for (let i = 0; i < nodes.length; i++) processOffscreen(nodes[i]);
    }

    console.info('Customs Tax Calculator initialized');
    scan();

    const observer = new MutationObserver(function (mutations) {
        for (const m of mutations) {
            for (const node of m.addedNodes) {
                if (node.nodeType !== 1) continue;
                if (node.matches && node.matches('.a-price span.a-offscreen')) processOffscreen(node);
                else if (node.querySelectorAll) scan(node);
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
